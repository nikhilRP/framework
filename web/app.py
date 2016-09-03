import json
import logging
import os
import requests
import time

from config import BaseConfig
from flask import Flask, render_template, g, jsonify, request
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(BaseConfig)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

cors = CORS(app, resources={r"/*": {"origins": "*"}})
db = SQLAlchemy(app)


@app.route('/', methods=['GET'])
@cross_origin(origin='*', headers=['Content- Type', 'Authorization'])
def index():
    return render_template("index.html")


@app.route('/element/<name>', methods=['GET'])
@cross_origin(origin='*', headers=['Content- Type', 'Authorization'])
def elements(name=None):
    pollutant = name.upper()
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "data", "element.json")
    data = json.load(open(json_url))
    results = {}
    for element in data['elements']:
        if element['symbol'] == pollutant:
            results = element
    if request.args.get('format', None) == 'json':
        return jsonify(**results)
    return render_template("element.html", results=results)


@app.route('/measurements', methods=['GET'])
@cross_origin(origin='*', headers=['Content- Type', 'Authorization'])
def measurements():
    coordinates = request.args.get('coordinates')
    r = requests.get(
        "https://api.openaq.org/v1/measurements?limit=1&coordinates=" + coordinates)
    results = r.json()
    return jsonify(results)


@app.route('/locations', methods=['GET'])
@cross_origin(origin='*', headers=['Content- Type', 'Authorization'])
def locations():
    r = requests.get("https://api.openaq.org/v1/locations")
    results = r.json()
    data = {'results': []}
    for result in results['results']:
        if 'coordinates' not in result:
            continue
        if result['coordinates']['latitude'] is None:
            continue
        if result['coordinates']['longitude'] is None:
            continue
        result['lat'] = result['coordinates']['latitude']
        result['lon'] = result['coordinates']['longitude']
        data['results'].append(result)
    if request.args.get('format', None) == 'json':
        return jsonify(data)
    return render_template("locations.html", data=data)


@app.before_first_request
def setup_logging():
    """
    Setups logging for each request seperatley
    """
    app.logger.setLevel(logging.INFO)


@app.before_request
def before_request():
    g.request_start_time = time.time()
    g.request_time = lambda: "%.5fs" % (time.time() - g.request_start_time)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(403)
def forbidden_page(error):
    return render_template("errors/forbidden_page.html"), 403


@app.errorhandler(404)
def page_not_found(error):
    return render_template("errors/page_not_found.html"), 404


@app.errorhandler(500)
def server_error_page(error):
    return render_template("errors/server_error.html"), 500


if __name__ == '__main__':
    app.run()
