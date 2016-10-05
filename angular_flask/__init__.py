import os
import json




from angular_flask.makecelery import make_celery
import dofunc as do
from flask import Flask, request, Response
from flask import render_template, send_from_directory, url_for

app = Flask(__name__)

app.config.from_object('angular_flask.settings')

app.url_map.strict_slashes = False

app.config.update(
    WTF_CSRF_ENABLED = False,
    CELERY_BROKER_URL='redis://localhost:6379',
    CELERY_RESULT_BACKEND='redis://localhost:6379'
)
celery = make_celery(app)

@celery.task()
def create_wordpress(name, company_name, ssh_key):
    do.create_wordpress(name, company_name, ssh_key)

import angular_flask.core
import angular_flask.models
import angular_flask.controllers
import angular_flask.fabcomm
import angular_flask.dofunc
