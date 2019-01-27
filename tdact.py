import os
import json
import logging
import requests
from flask_restful import Api, Resource
from flask import Flask, render_template, request, send_from_directory
from flask import jsonify
from flask_wtf.csrf import CsrfProtect
from xml.etree import ElementTree as ET

from models import db

application = Flask(__name__, template_folder="templates", static_url_path='/static')
application._static_folder = os.path.abspath("static/")
api = Api(application)
csrf = CsrfProtect(application)

@application.route('/css/<path:filename>')
def serve_static_css(filename):
    root_dir = os.path.dirname(os.getcwd())
    return send_from_directory(os.path.join(root_dir, 'static', 'css'), filename)


@application.route('/js/<path:filename>')
def serve_static_js(filename):
    root_dir = os.path.dirname(os.getcwd())
    return send_from_directory(os.path.join(root_dir, 'static', 'js'),
filename)


@application.route("/")
def hello():
    return render_template('index.html')
    #return "<h1 style='color:blue'>Hello There, my stupid friends!</h1>"


@application.route("/plot1")
def plot_one():
    return render_template('plot1.html')
    #return "<h1 style='color:blue'>Hello There, my stupid friends!</h1>"


@application.route("/plot2")
def plot_two():
    return render_template('plot2.html')

@application.route("/plot3")
def plot_three():
    return render_template('plot3.html')


@application.route("/plot4")
def plot_four():
    return render_template('plot4.html')


@application.route("/plot5")
def plot_five():
    return render_template('plot5.html')


@csrf.exempt
@application.route("/react")
def react_view():
    return render_template('reactive.html')


@application.route('/parseapi', methods=['POST', 'GET'])
def my_test_endpoint(url):
    # force=True, above, is necessary if another developer 
    # forgot to set the MIME type to 'application/json'
    try:
        logging.info("call with "+url)
        #r = requests.get("http://"+url)
        #jsonify(url=url, status=200, response=str(r.text))
    except Exception as ex:
        return jsonify(url=url, status=400, error=str(ex))


@api.resource('/parseapi/')
class UrlAPI(Resource):
    def get(self):
        pass

    def post(self):
        return jsonify(result="", status=200)
  
   
   
@api.resource('/plotapi')
class API(Resource):
    def post(self):
        return jsonify(result="true")

    def get(self):
        json_val = """
    {"indexes": ["one", "two", "three", "four"],
    "values":[
       [
        [0.8345658418026087, "text1"],
        [2.16990473059691, "text2"],
        [0.11225498002657552, "text3"],
        [1.17486306808582253, "text4"]
       ],
       [
        [1.3345658418026087, "text-1"],
        [1.76990473059691, "text-2"],
        [0.7225498002657552, "text-3"],
        [1.57486306808582253, "text-4"]
       ]
    ],
    "values1": [
    {
        "0": 0.8345658418026087,
        "1": 2.16990473059691,
        "2": 0.11225498002657552,
        "3": 0.17486306808582253,
        "name": "zero"
    },
    {
        "0": 0.4547571633367139,
        "1": 2.293639687510199,
        "2": 0.11257016829714184,
        "3": 0.2298141045051727,
        "name": "one"
    }
    ]
    }
               """
        return jsonify(dict(json.loads(json_val)))    


POSTGRES = {
    'user': 'psqluser',
    'pw': 'psqluser',
    'db': 'tdactdb',
    'host': 'localhost',
    'port': '5432',
}

@application.route('/linkapi', methods=["GET","POST"])
def url_process():
    try:
        url = request.args.get('url')
        response = requests.get(url)
        tree = ET.fromstring(response.content)
        parsed = ET.tostring(tree).decode()
        return jsonify(url=url, response=parsed, status=200)
    except Exception as ex:
        return jsonify(url=url, response=str(ex), status=400)


application.config['DEBUG'] = True
application.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
db.init_app(application)
#@application.route('/', defaults={'path': ''})
#@application.route('/<path:path>')
#def catch_all(path):
#    return render_template("index.html")

if __name__ == "__main__":
    application.run(debug=True)
