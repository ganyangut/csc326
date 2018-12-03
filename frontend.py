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
SCOPE = StaticVar.SCOPE
REDIRECT_URI = StaticVar.REDIRECT_URI
sessions_opts = StaticVar.sessions_opts
database_file = 'backend/'+StaticVar.database_file
num_per_page = StaticVar.num_per_page

# lab3 only
history = History()

@get('/')  # or @route('/')
def home():
    print "------route---home------------------------------"
    return template('./templates/query_page.tpl', login=False, history=history)

# show search results, word count, and search history
@post('/')  # or @route('/', method='POST')
def show_results():
    # keyword from http get
    keyword = request.forms.get('keywords')
    redirect('/keyword/' + keyword + '/page_no/1')

# pagination for urls found
@route('/keyword/<keyword>/page_no/<page_no>')
def search_first_word(keyword, page_no):
    # split keyword string into words and count them
    # store words in a dict
    keyword_list = keyword.split()
    words_count = {word: keyword_list.count(word) for word in keyword_list}

    if not keyword_list:
        return template('./templates/result_page.tpl', keywords=keyword, words_count=words_count,
                    login=False, history=history, document=[], cur_page_num=page_no,
                    num_per_page=num_per_page, page_num_counts=0)

    # connect to database
    db_conn = lite.connect(database_file)
    myDB = MyDatabase(db_conn)

    # get word ids and crawler ids from lexicon
    word_id_list = myDB.select_word_id_from_lexicon(keyword_list)
    # get document ids and crawler ids from inverted index
    sorted_document_id = myDB.select_document_id_from_InvertedIndex(word_id_list)    
    
    # sort document ids and crawler ids by their rank score
    #sorted_document_id = myDB.select_document_id_from_PageRank(document_id)
    
    # get document ids and crawler ids based on page number
    url_counts = len(sorted_document_id)    
    page_num_counts = pagination(url_counts)
    cur_page_num = int(page_no)
    if cur_page_num > 0:
        cur_page_num = cur_page_num -1
    start_num = cur_page_num * num_per_page
    end_num = start_num + num_per_page   
    document = myDB.select_document_from_DocumentIndex(sorted_document_id[start_num:end_num])

    db_conn.close()


    return template('./templates/result_page.tpl', keywords=keyword, words_count=words_count,
                    login=False, history=history, document=document, cur_page_num=page_no,
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
