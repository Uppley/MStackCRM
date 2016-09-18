from angular_flask import app

from flask_sqlalchemy import SQLAlchemy
from flask_restless import APIManager
from flask_superadmin import Admin, model
from flask.ext.security import current_user
import flask_superadmin

class MyAdminIndexView(flask_superadmin.AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated




db = SQLAlchemy(app)
admin = Admin(app=app)
# admin = Admin(app=app, index_view=MyAdminIndexView())
api_manager = APIManager(app, flask_sqlalchemy_db=db)
