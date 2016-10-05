from __future__ import print_function
# The location where the main functions will reside. These include:
# Get

from angular_flask import models
from angular_flask.core import db
from flask.ext.security import utils
import threading
import sys
import uuid


import threading
import time


class ThreadingExample(object):
    """ Threading example class
    The run() method will be started and it will run in the background
    until the application exits.
    """

    def __init__(self, client, cf_id, interval=1):
        """ Constructor
        :type interval: int
        :param interval: Check interval, in seconds
        """
        self.interval = interval

        thread = threading.Thread(target=self.run, args=(client, cf_id))
        thread.daemon = True                            # Daemonize thread
        thread.start()                                  # Start the execution

    # Where you'd run the image recognition part
    def run(self, client, cf_id):
        """ Method that runs forever """
        while True:
            #() Do something
            print('Doing something imporant in the background', file=sys.stderr)
            # Activate the file opener here
            # Add cf_id and person_id/person_group_id here
            # db.session.commit()

            time.sleep(self.interval)



def new_user(user_email, user_password):
    user = models.user_datastore.create_user(email=user_email, password=user_password)
    db.session.commit()


# def log_user(username, password):
#     # models.user_datastore.login

def new_client(**kwargs):
    if kwargs is not None:
        client = models.Client(**kwargs)
        db.session.add(client)
        db.session.commit()
        return client
    else:
        return False


def get_clients(**kwargs):
    clients = models.Client.query.filter_by(**kwargs).all()
    return clients


# Activates a frame that gets 10 images to scan a users face_trainer
# Params: Client ID
# Results
def trainFace(client_id, **kwargs):
    # Get a user model here. Find the first item using the id
    the_client = models.Client.query.filter_by(id=client_id).first()
    # Create a UUID that we'll find the user information by.
    cf_id = str(uuid.uuid1())
    example = ThreadingExample(the_client, cf_id)
    return {'message': 'Training the face data right now. I guess you can call it a facial'}
    # Save that inside of CF.create_person() instead of the name
    # cf_id used to get user information on the fly
    # Create an internal function that will run on background thread -- doing
        # Activate train data function
        # Get person_group_id and person_id
        # On complete save person_id and group_id for user
        # Check to see if clientId is added
    pass

def login(**kwargs):
    # Make sure username and password are there

    if((kwargs['email'] is not None) and (kwargs['password'] is not None)):
        user = models.User.query.filter_by(email=kwargs['email']).first()
        if(user.password == kwargs['password']):
            # Sweet, this is some right shit!!
            utils.login_user(user, remember=None)
            return {"success": True, "user": {"email": kwargs['email']}}
        else:
            return {"success": False}
    return {}
