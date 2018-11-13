import Queue
import operator
import json
import httplib2
import requests
import os
import sqlite3 as lite
from backend.static_variables import StaticVar
from backend.data_structures import UserHistoryIndex, History, UserRecentWordsIndex, RecentWords
from backend.database import MyDatabase

from bottle import Bottle, route, run, template, get, post, request, static_file, redirect, app, error
from oauth2client.client import OAuth2WebServerFlow, flow_from_clientsecrets
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
from beaker.middleware import SessionMiddleware

# declare golbal variables
user_history_index = UserHistoryIndex()
user_recent_words_index = UserRecentWordsIndex()

current_page = 'query_page'
keywords = ''
words_count = []
SCOPE = StaticVar.SCOPE
REDIRECT_URI = StaticVar.REDIRECT_URI
sessions_opts = StaticVar.sessions_opts
database_file = 'backend/'+StaticVar.database_file
num_per_page = StaticVar.num_per_page

# lab3 only
history = History()

# lab3 witout log in
#myDB = MyDatabase()

@get('/')  # or @route('/')
def home():
    print "------route---home------------------------------"
    return template('./templates/query_page.tpl', login=False, history=history)

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

    first_word = words_list[0]
    # lowercase first keyword
    first_word = first_word.lower()
    print "first_word: "+repr(first_word)+"\n"
    redirect('/keyword/'+first_word+'/page_no/1')

# pagination for urls found
@route('/keyword/<keyword>/page_no/<page_no>')
def search_first_word(keyword,page_no):
    first_word=keyword
    db_conn = lite.connect(database_file)
    #global myDB
    myDB = MyDatabase(db_conn)

    word_id = myDB.select_word_id_from_lexicon(first_word)

    document_id = myDB.select_document_id_from_InvertedIndex(word_id)

    # sort document id by their rank score
    sorted_document_id = myDB.select_document_id_from_PageRank(document_id)

    url_counts = len(sorted_document_id)

    page_num_counts = pagination(url_counts)
    cur_page_num=int(page_no)
    if cur_page_num > 0:
        cur_page_num = cur_page_num -1
    start_num = cur_page_num*num_per_page
    end_num = start_num + num_per_page  

    document = myDB.select_document_from_DocumentIndex(sorted_document_id[start_num:end_num])

    db_conn.commit()
    db_conn.close()

    return template('./templates/result_page.tpl', keywords=keywords, words_count=words_count,
                    login=False, history=history, first_word=first_word, document=document, cur_page_num=cur_page_num,
                    num_per_page=num_per_page, page_num_counts=page_num_counts)

def pagination(url_counts):
    # q for quotient, r for remainder
    q, r = divmod(url_counts, num_per_page)
    if r != 0:
        page_num_counts = q+1
    else:
        page_num_counts = q
    return page_num_counts

@error(404)
def error404(error):
    return template('./templates/error_page.tpl',error=error)

'''
# LAB2 with google log in

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

@route('/login', method='GET')
def query_page():
    global current_page
    current_page = 'query_page'
    google_login()

# if user login in the result_page, set the current page to result_page
# and then redirect to Google login
@route('/login/result', method='GET')
def result_page():
    global current_page
    current_page = 'result_page'
    google_login()

# redirect to Google login prompt for user authentication
def google_login():

    print "------route---login------------------------------"
    flow = flow_from_clientsecrets(
        'client_secrets.json', scope=SCOPE, redirect_uri=REDIRECT_URI)
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


#If user authorizes your application server to access the Google services, an one-time code will be attached
#to the query string when the browser is redirected to the redirect_uri specified in step 2. 
#The one-time code can be retrieved as GET parameter:

@route('/redirect')
def redirect_page():
    print "------route---redirect------------------------------"
    code = request.query.get('code', '')

    print "1\n"
    with open("client_secrets.json", 'r') as load_f:
        load_dict = json.load(load_f)
        print "\n client_secrets:"
        print load_dict
    print "2\n"
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
    if "name" in user_document.keys():
        session['user_name'] = user_document['name']
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
'''

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
    run(app=app, host='0.0.0.0', port=80, debug=True)
