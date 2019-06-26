# Laptop Service
from flask import Flask, Flask, jsonify, redirect, g,url_for, request, render_template, abort, Response, json, session
from flask_restful import Resource, Api
from flask_login import UserMixin, login_user, LoginManager, login_required, login_required, current_user, logout_user, confirm_login, fresh_login_required
from flask_wtf.csrf import CSRFProtect
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Length
import flask
from pymongo import MongoClient
import pymongo

import os


from passlib.apps import custom_app_context as pwd_context
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth
from pymongo import MongoClient
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)

from werkzeug.utils import redirect


# Instantiate the app
app = Flask(__name__)
api = Api(app)
csrf = CSRFProtect(app)
csrf.init_app(app)
app.config['SECRET_KEY'] = 'cnwelckwnelweknwelcneelckn'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

db = SQLAlchemy(app)
auth = HTTPBasicAuth()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

client = MongoClient('db', 27017)
db_todo = client.tododb



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True)
    password_hash = db.Column(db.String(64))

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration=600):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None    # valid token, but expired
        except BadSignature:
            return None    # invalid token
        user = User.query.get(data['id'])
        return user

@app.route('/')
def index():
	return redirect('/login')

class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired('A username is required!'), Length(min=3, max=10,
                                                                                                    message='Must be between 3 and 10 characters.')])
    password = PasswordField('password', validators=[InputRequired('Password is required!')])
    remember = BooleanField('Remember me')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return render_template('logined.html')

    form = LoginForm()
    session['next'] = request.args.get('next')
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if user.verify_password(form.password.data):
                flask.flash('Logged in successfully.')
                login_user(user, remember=form.remember.data)
                return render_template('logined.html')
            else:
                return ' <h1> Wrong user/password! </h1>'

        return '<h1> No such user </h1>'

    return flask.render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template('logout.html')


@auth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    user = User.verify_auth_token(username_or_token)
    if not user:
        # try to authenticate with username/password
        user = User.query.filter_by(username=username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True


class RegisterForm(FlaskForm):
    username = StringField('username', validators=[InputRequired('A username is required!'), Length(min=3, max=10,
                                                                                                    message='Must be between 3 and 10 characters.')])
    password = PasswordField('password', validators=[InputRequired('Password is required!')])




@app.route('/api/register', methods=['POST'])
def register():
	app.logger.debug("In register")
	if not request.json:
		app.logger.debug("No json")
		accName = request.form['username']
		app.logger.debug(accName)
		password = request.form['pass']
		app.logger.debug(password)
	else:
		app.logger.debug("No Form")
		accName = request.json['username']
		app.logger.debug(accName)
		password = request.json['password']
		app.logger.debug(password)

	if accName is '' or password is '':
		abort(400)  # missing arguments
	if User.query.filter_by(username=accName).first() is not None:
	 	abort(400)  # existing user
	
	user = User(username=accName)
	user.hash_password(password)
    
	db.session.add(user)
	db.session.flush() 


	userJSON = ({'username': user.username})
	js = json.dumps(userJSON)
	resp = Response(js, status=201, mimetype='application/json')
	resp.headers['location'] = '/api/users/{}'.format(user.id)
	db.session.commit()
	return resp
	



@app.route('/register', methods=['GET', 'POST'])
def register_user():
    form = RegisterForm()
    if form.validate_on_submit():
        # register and validate the user.
        # user should be an instance of your `User` class
        # login_user(user)
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            return '<h1> User exists! </h1>'
        else:
            user = User(username=form.username.data)
            user.hash_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            return render_template('registerAccess.html')
    return flask.render_template('register.html', form=form)

@app.route('/register_page')
def register_page():
    form = RegisterForm()
    return render_template('register.html' , form=form)



@app.route('/api/token')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token(600)
    return jsonify({'token': token.decode('ascii'), 'duration': 600})

@app.route('/api/resource')
@auth.login_required
def get_resource():
    return render_template('index.php')
	
	
	

class listAll(Resource): 
	def get(self):
		_items = db_todo.tododb.find().sort([('open_time',pymongo.ASCENDING), ('close_time',pymongo.ASCENDING)])
	
		items = [item for item in _items]
		open_times = []
		close_times = []
		for item in items:
			open_times.append(item['open_time'])
			close_times.append(item['close_time'])

		JSONdict = {}			
		JSONdict['open_time'] = open_times
		JSONdict['close_time'] = close_times
	
		return JSONdict


class listAllJSON(Resource):
	def get(self):
		_items = db_todo.tododb.find().sort([('open_time',pymongo.ASCENDING), ('close_time',pymongo.ASCENDING)])
		items = [item for item in _items]		
		
		open_times = []
		close_times = []		
			
		for item in items:
			open_times.append(item['open_time'])
			close_times.append(item['close_time'])		
		
		JSONdict = {}
		JSONdict['open_time'] = open_times
		JSONdict['close_time'] = close_times
		return JSONdict


class listAllCSV(Resource):
	def get(self):
		_items = db_todo.tododb.find().sort([('open_time',pymongo.ASCENDING), ('close_time',pymongo.ASCENDING)])
	
		items = [item for item in _items]
	
		csv_string = ""
		for item in items:
			csv_string += item['open_time'] + ", "
			csv_string += item['close_time'] + ", "
		return csv_string


class listOpenOnlyJSON(Resource):
	def get(self):
		top = request.args.get('top')
		if (top == None):
			top = 20
		_items = db_todo.tododb.find().sort('open_time', pymongo.ASCENDING).limit(int(top))
		items = [item for item in _items]
		open_times = []	
		for item in items:
			open_times.append(item['open_time'])		
	
		JSONdict = {}
		JSONdict['open_time'] = open_times
		return JSONdict


class listOpenOnlyCSV(Resource):
	def get(self):
		top = request.args.get('top')
		if (top == None): 
			top = 20
		_items = db_todo.tododb.find().sort('open_time', pymongo.ASCENDING).limit(int(top))
		items = [item for item in _items]
	
		csv_string = ""
		for item in items:
			csv_string += item['open_time'] + ", "
		return csv_string


class listCloseOnlyJSON(Resource):
	def get(self):
		top = request.args.get('top')
		if (top == None):
			top = 20
		_items = db_todo.tododb.find().sort('close_time', pymongo.ASCENDING).limit(int(top))
		items = [item for item in _items]
		close_times = []		
		for item in items:
			close_times.append(item['close_time'])		

		JSONdict = {}
		JSONdict['close_time'] = close_times
		return JSONdict


class listCloseOnlyCSV(Resource):
	def get(self):
		top = request.args.get('top')
		if (top == None):
			top = 20
		_items = db_todo.tododb.find().sort('close_time', pymongo.ASCENDING).limit(int(top))
		items = [item for item in _items]
		csv_string = ""
		for item in items:
			csv_string += item['close_time'] + ", "
		return csv_string

class listOpenOnly(Resource):
	def get(self):
		top = request.args.get('top')
		if (top == None):
			top = 20
		_items = db_todo.tododb.find().sort([('open_time',pymongo.ASCENDING)]).limit(int(top))
		items = [item for item in _items]
		open_times = []
		for item in items:
			open_times.append(item['open_time'])

		JSONdict = {}
		JSONdict['open_time'] = open_times
		return JSONdict

class listCloseOnly(Resource):
	def get(self):
		top = request.args.get('top')
		if (top == None):
			top = 20
		_items = db_todo.tododb.find().sort([('close_time',pymongo.ASCENDING)]).limit(int(top))
		items = [item for item in _items]
		close_times = []
		for item in items:
			close_times.append(item['close_time'])

		JSONdict = {}
		JSONdict['close_time'] = close_times
		return JSONdict




		

# Create routes
# Another way, without decorators
api.add_resource(listAll, '/listAll')
api.add_resource(listAllJSON, '/listAll/json')
api.add_resource(listAllCSV, '/listAll/csv')
api.add_resource(listOpenOnlyJSON, '/listOpenOnly/json')
api.add_resource(listOpenOnlyCSV, '/listOpenOnly/csv')
api.add_resource(listCloseOnlyJSON, '/listCloseOnly/json')
api.add_resource(listCloseOnlyCSV, '/listCloseOnly/csv')
api.add_resource(listOpenOnly, '/listOpenOnly')
api.add_resource(listCloseOnly, '/listCloseOnly')

# Run the application
if __name__ == '__main__':
    if not os.path.exists('db.sqlite'):

        db.create_all()
    app.run(host='0.0.0', port=80, debug=True)
