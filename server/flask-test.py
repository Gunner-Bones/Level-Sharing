from flask import Flask, json, request
# from gevent.pywsgi import WSGIServer
# from flask import render_template, flash
# from content_management import Content

companies = [{"id": 1, "name": "Company One"}, {"id": 2, "name": "Company Two"}]

api = Flask(__name__)

@api.route('/companies', methods=['GET'])
def get_companies():
  return json.dumps(companies)

@api.route('/companies', methods=['POST'])
def post_companies():
	return json.dumps({"success": True}), 201

@api.route('/query-example')
def query_example():
    language = request.args.get('language') #if key doesn't exist, returns None

    return '''<h1>The language value is: {}</h1>'''.format(language)

@api.route('/form-example', methods=['GET', 'POST']) #allow both GET and POST requests
def form_example():
    if request.method == 'POST':  #this block is only entered when the form is submitted
        language = request.form.get('language')
        framework = request.form['framework']

        return '''<h1>The language value is: {}</h1>
                  <h1>The framework value is: {}</h1>'''.format(language, framework)

    return '''<form method="POST">
                  Language: <input type="text" name="language"><br>
                  Framework: <input type="text" name="framework"><br>
                  <input type="submit" value="Submit"><br>
              </form>'''

@api.route('/json-example', methods=['POST']) #GET requests will be blocked
def json_example():
    req_data = request.get_json()

    language = req_data['language']
    framework = req_data['framework']
    python_version = req_data['version_info']['python'] #two keys are needed because of the nested object
    example = req_data['examples'][0] #an index is needed because of the array
    boolean_test = req_data['boolean_test']

    return '''
           The language value is: {}
           The framework value is: {}
           The Python version is: {}
           The item at index 0 in the example list is: {}
           The boolean value is: {}'''.format(language, framework, python_version, example, boolean_test)

"""@app.route('/')
def homepage():
    return render_template("main.html")

@app.route('/dashboard/')
def dashboard():
    return render_template("dashboard.html", TOPIC_DICT = TOPIC_DICT)

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")"""


if __name__ == '__main__':
	api.run(threaded=True)
	""" http_server = WSGIServer(('', 5000), api)
             http_server.serve_forever()"""