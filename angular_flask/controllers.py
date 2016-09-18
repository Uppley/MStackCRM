import os
from flask import Flask, request, Response, jsonify
from flask import render_template, url_for, redirect, send_from_directory
from flask import send_file, make_response, abort
from angular_flask import app, create_wordpress

# routing for API endpoints, generated from the models designated as API_MODELS
from angular_flask.core import api_manager, db
from angular_flask.models import *
import angular_flask.core_funcs as c_funcs

for model_name in app.config['API_MODELS']:
    model_class = app.config['API_MODELS'][model_name]
    api_manager.create_api(model_class, methods=['GET', 'POST', 'PATCH'])

session = api_manager.session


#
# routing for basic pages (pass routing onto the Angular app)
@app.route('/')
@app.route('/about')
@app.route('/register')
@app.route('/userLogin')
@app.route('/blog')
@app.route('/servers')
@app.route("/login")
@app.route("/products")
@app.route("/clients")
def basic_pages(**kwargs):
    return make_response(open('angular_flask/templates/index.html').read())


@app.route('/api/login', methods=['POST'])
def basic_login():
    if request.method == 'POST':
        req_json = request.get_json()

        if(req_json is not None):
            return jsonify(c_funcs.login(email=req_json['email'],
                                         password=req_json['password']
                                         )
                           )

        # # Get the ssh_key later
        # name = str(req_json['name'])
        # company = str(req_json['company'])
        # create_wordpress.delay( name.replace(" ", "-") , company.replace(" ", "-"), "ThinkP")
        return "Service Login Started"
    else:
        # Return a flash here
        return make_response(open('angular_flask/templates/index.html').read())


@app.route('/api/client/train', methods=['POST'])
def face_trainer():
    if request.method == 'POST':
        # Expect to get the client information
        req_json = request.get_json()

        if(req_json is not None):
            c_funcs.trainFace(req_json['id'])
            return jsonify(req_json)
        return jsonify({'message': 'Face Training api goes here. Make sure to add the clientID as well'})
    else:
        # Return a flash here
        return make_response(open('angular_flask/templates/index.html').read())


# routing for CRUD-style endpoints
# passes routing onto the angular frontend if the requested resource exists
from sqlalchemy.sql import exists

crud_url_models = app.config['CRUD_URL_MODELS']


@app.route('/<model_name>/')
@app.route('/<model_name>/<item_id>')
def rest_pages(model_name, item_id=None):
    if model_name in crud_url_models:
        model_class = crud_url_models[model_name]
        if item_id is None or session.query(exists().where(
                model_class.id == item_id)).scalar():
            return make_response(open(
                'angular_flask/templates/index.html').read())
    abort(404)


@app.route('/api/addserver', methods=['GET', 'POST'])
def add_server():
    if request.method == 'POST':
        req_json = request.get_json()
        print req_json
        # Get the ssh_key later
        name = str(req_json['name'])
        company = str(req_json['company'])
        create_wordpress.delay(name.replace(" ", "-"),
                               company.replace(" ", "-"), "ThinkP")
        return "Server creation started"
    else:
        # print "Send something else back"
        return "You should bbe so done"


@app.route('/api/removeserver', methods=['GET', 'POST'])
def remove_server():
    return "Removing the server with the given id"

# TODO: Create a remove server command in API


def register_user():
    # Register the user here
    return "The user was registered"

# TODO: Create basic Login API


def login_user():
    return "The User was "

# Login ... login a user

# Register ... register the user
# email password

# TODO: Create Stripe API here
#

# Register Card Info Here

# Activate Stripe recurring payment here

# special file handlers and error handlers


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'img/favicon.ico')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
