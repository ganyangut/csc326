import Queue
import operator
from backend.data_structures import history
from bottle import Bottle, route, run, template, get, post, request,static_file


# declare golbal variables
history = history()

# ask for keywords from user 
@get('/') # or @route('/')
def submit_form():
    return template('./templates/query_page.tpl')

@route('/assets/image/<filename:path>')
def send_images(filename):
    return static_file(filename, root='./assets/image')

@route('/assets/css/<filename:path>')
def send_assets(filename):
    return static_file(filename, root='./assets/css')

@route('/templates/<filename:path>')
def send_templates(filename):
    return static_file(filename, root='./templates')

# show search results, word count, and search history
@post('/') # or @route('/', method='POST')
def show_results():
    # keyword from http get
    keywords = request.forms.get('keywords')    
    
    # split keyword string into words and count them
    # store words in a dict
    words_list = keywords.split()
    words_count = {word:words_list.count(word) for word in words_list}

    # add keyword to history
    # joining words instead of the original string to avoid multiple whitespaces
    history.add_new_keywords(words_list)
    print "words_count: "+repr(words_count)
    return template('./templates/result_page.tpl', keywords=keywords, words_count=words_count, history=history.get_popular())

# run server
run(host='localhost', port=8081, debug=True)


