from bottle import route, run, template, get, post, request

@get('/') # or @route('/')
def submit_form():
    return '''
        <form action="/" method="post">
            <input name="keyword_string" type="keyword" />            
            <input value="Search" type="submit" />
        </form>
    '''

@post('/') # or @route('/', method='POST')
def show_results():
    keyword_string = request.forms.get('keyword_string')
    if keyword_string == "qwerty": 
        return "<p>You searched the right thing.</p>"
    else:
        return "<p>Fucking stupid.</p>"

run(host='localhost', port=8080, debug=True)
