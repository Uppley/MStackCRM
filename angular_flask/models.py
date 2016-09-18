from datetime import datetime

from angular_flask.core import db, admin
from angular_flask import app
from flask.ext.security import Security, SQLAlchemyUserDatastore, \
    UserMixin, RoleMixin, login_required, current_user


# TODO switch the database from SQLite Postgresql
#

roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))


class Activity(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    poster_id = db.Column(db.Integer, db.ForeignKey('user.id'))


# Should really be a product
#
class Project(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))
    hour_number = db.Column(db.Integer())
    estimate_hours = db.Column(db.Integer())
    progress = db.Column(db.String(80))
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))

class Client(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    first_name = db.Column(db.String(80))
    middle_name = db.Column(db.String(80), nullable=True)
    last_name = db.Column(db.String(80))
    email = db.Column(db.String(255), unique=True)
    street1 = db.Column(db.String(255))
    street2 = db.Column(db.String(255), nullable=True)
    city = db.Column(db.String(255))
    state = db.Column(db.String(255))
    person_id = db.Column(db.String(255), nullable=True)
    person_group_id = db.Column(db.String(255), nullable=True)
    cf_id = db.Column(db.String(255), nullable=True)
    phone = db.Column(db.String(80))
    ipfs_key = db.Column(db.String(255)) # can be used to store the photo
    description = db.Column(db.String(255), nullable=True)
    stripeid = db.Column(db.String(255), nullable=True)
    projects = db.relationship('Project', backref='client',
                                lazy='dynamic')


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))




class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    body = db.Column(db.Text)
    pub_date = db.Column(db.DateTime)

    def __init__(self, title, body, pub_date=None):
        self.title = title
        self.body = body
        if pub_date is None:
            pub_date = datetime.utcnow()
        self.pub_date = pub_date

    def __repr__(self):
        return '<Post %r>' % self.title


class Server(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    company_name = db.Column(db.Text)
    ip = db.Column(db.Text)
    doid = db.Column(db.Text)
    active = db.Column(db.Boolean)

    def __init__(self, name, company_name, ip, doid, active=None):
        self.name = name
        self.company_name = company_name
        self.ip = ip
        self.doid = doid
        if active is None:
            active = True
        self.active = active

    def __repr__(self):
        return '<Server %r>' % self.name


user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)
admin.register(User, session=db.session)
admin.register(Role, session=db.session)
admin.register(Post, session=db.session)
admin.register(Server, session=db.session)
admin.register(Activity, session=db.session)
admin.register(Project, session=db.session)
admin.register(Client, session=db.session)





# models for which we want to create API endpoints
app.config['API_MODELS'] = {'post': Post, 'server': Server, 'client': Client, 'project': Project}

# models for which we want to create CRUD-style URL endpoints,
# and pass the routing onto our AngularJS application
app.config['CRUD_URL_MODELS'] = {'post': Post, 'server': Server, 'client': Client, 'project': Project}
