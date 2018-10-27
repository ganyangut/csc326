import Queue
import operator
import json
import httplib2
import requests
from backend.data_structures import UserHistoryIndex, History, UserRecentWordsIndex, RecentWords
from bottle import Bottle, route, run, template, get, post, request, static_file, redirect, app
from oauth2client.client import OAuth2WebServerFlow, flow_from_clientsecrets
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
from beaker.middleware import SessionMiddleware

# declare golbal variables
user_history_index = UserHistoryIndex()
user_recent_words_index = UserRecentWordsIndex()

current_page = 'query_page'
keywords  = ''
words_count = []

SCOPE = 'https://www.googleapis.com/auth/plus.me https://www.googleapis.com/auth/userinfo.email'
REDIRECT_URI = 'http://localhost:8081/redirect'
sessions_opts = {
    'session.type': 'file',
    'session.cookie_expires': 300,
    'session.data_dir': './data',
    'session.auto': True
}

# ask for keywords from user
@get('/')  # or @route('/')
def home():
    print "------route---home------------------------------"
    session = request.environ.get('beaker.session')
    if "user_email" in session:        
        return template('./templates/query_page.tpl', login = True, 
                user_email = session["user_email"], recent_words = user_recent_words_index.get_recent_words(session["user_email"]))
    else:
        return template('./templates/query_page.tpl', login = False)

# show search results, word count, and search history
@post('/')  # or @route('/', method='POST')
def show_results():
    # keyword from http get
    global keywords
    global words_count
    keywords = request.forms.get('keywords')

    # split keyword string into words and count them
    # store words in a dict
    words_list = keywords.split()
    words_count = {word: words_list.count(word) for word in words_list}

    # add keyword to history
    # joining words instead of the original string to avoid multiple whitespaces
    session = request.environ.get('beaker.session')
    if "user_email" in session:
        user_history_index.get_history(session["user_email"]).add_new_keywords(words_list)
        user_recent_words_index.get_recent_words(session["user_email"]).add_new_keywords(words_list)
        print "words_count: "+repr(words_count)
        return template('./templates/result_page.tpl', keywords = keywords, words_count = words_count, login = True, 
                user_email = session["user_email"], recent_words = user_recent_words_index.get_recent_words(session["user_email"]),
                history = user_history_index.get_history(session["user_email"]).get_popular())
    else:
        user_history_index.get_history("anonymous").add_new_keywords(words_list)
        return template('./templates/result_page.tpl', keywords = keywords, words_count = words_count, login = False,
                history = user_history_index.get_history("anonymous").get_popular())

#if user login in the query_page, set the current page to query_page
@route('/login', method='GET')
def query_page():
    global current_page
    current_page = 'query_page'
    google_login()
     
#if user login in the result_page, set the current page to result_page
#and then redirect to Google login
@route('/login/result', method='GET')
def result_page():
    global current_page
    current_page = 'result_page'
    google_login()

# redirect to Google login prompt for user authentication
def google_login():
    
    print "------route---login------------------------------"
    flow = flow_from_clientsecrets('client_secrets.json', scope = SCOPE, redirect_uri = REDIRECT_URI)
    uri = flow.step1_get_authorize_url()
    return redirect(str(uri))

def credentials_to_dict(credentials):
    return {'access_token': credentials.access_token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'revoke_uri': credentials.revoke_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes}

# redirect to Google logout prompt, and then redirect to the query_page
@route('/logout', method='GET')
def google_logout():
    print "------route---logout------------------------------"
    session = request.environ.get('beaker.session')
    requests.post('https://accounts.google.com/o/oauth2/revoke',
        params={'token': session["token"]},
        headers = {'content-type': 'application/x-www-form-urlencoded'})
    print "\n session: " + repr(session)
    session.delete()
    print "\n session: " + repr(session)       
    return redirect('/')

'''
If user authorizes your application server to access the Google services, an one-time code will be attached
to the query string when the browser is redirected to the redirect_uri specified in step 2. 
The one-time code can be retrieved as GET parameter:
'''
@route('/redirect')
def redirect_page():
    print "------route---redirect------------------------------"
    code = request.query.get('code', '')

    with open("client_secrets.json", 'r') as load_f:
        load_dict = json.load(load_f)
        print "\n client_secrets:"
        print load_dict
    flow = OAuth2WebServerFlow(client_id=load_dict['web']['client_id'], client_secret=load_dict['web']['client_secret'],
                                scope=SCOPE, redirect_uri=REDIRECT_URI)
    credentials = flow.step2_exchange(code)
    print credentials_to_dict(credentials)

    # acquire refresh tokens for offline access, syncing Google accounts when users are not actively logged in.
    #token = credentials.id_token['sub']
    token = credentials.access_token

    # retrieve user's data
    http = httplib2.Http()
    http = credentials.authorize(http)
    print credentials_to_dict(credentials)

    # Get user info
    users_service = build('oauth2', 'v2', http=http)
    user_document = users_service.userinfo().get().execute()
    #print "\n user_document: " + repr(user_document)
    user_email = user_document['email']    
    # maintain a session for the user
    session = request.environ.get('beaker.session')
    session["user_email"] = user_email
    session['credentials'] = credentials_to_dict(credentials)
    session["token"] = token

    session.save()
    print "\n session: " + repr(session)
    return redirect('/user')



#after user login, they will stay on the same page (query_page || result_page)
@route('/user')
def user_login():
    print "------route---user------------------------------"
    session = request.environ.get('beaker.session')
    if current_page == 'query_page':
        return template('./templates/query_page.tpl', login = True, 
            user_email = session["user_email"], recent_words = user_recent_words_index.get_recent_words(session["user_email"]))
    else:
        return template('./templates/result_page.tpl', keywords = keywords, words_count = words_count, login = True, 
            user_email = session["user_email"], recent_words = user_recent_words_index.get_recent_words(session["user_email"]),
            history = user_history_index.get_history(session["user_email"]).get_popular())

# routes of assets (css, js, images)
@route('/assets/<filename:path>')
def send_assets(filename):
    return static_file(filename, root='./assets')

# route of templates
@route('/templates/<filename:path>')
def send_templates(filename):
    return static_file(filename, root='./templates')

if __name__ == "__main__":
    app = SessionMiddleware(app(), sessions_opts)
    # run server
    run(app=app, host='localhost', port=8081, debug=True)
