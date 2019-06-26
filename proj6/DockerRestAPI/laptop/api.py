# Laptop Service

from flask import Flask, request
from flask_restful import Resource, Api
import flask
from pymongo import MongoClient
import pymongo
import os

# Instantiate the app
app = Flask(__name__)
api = Api(app)

client = MongoClient('db', 27017)
db = client.tododb

class listAll(Resource): 
	def get(self):
		_items = db.tododb.find().sort([('open_time',pymongo.ASCENDING), ('close_time',pymongo.ASCENDING)])
		
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
		_items = db.tododb.find().sort([('open_time',pymongo.ASCENDING), ('close_time',pymongo.ASCENDING)])
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
		_items = db.tododb.find().sort([('open_time',pymongo.ASCENDING), ('close_time',pymongo.ASCENDING)])
		
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
		_items = db.tododb.find().sort('open_time', pymongo.ASCENDING).limit(int(top))
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
		_items = db.tododb.find().sort('open_time', pymongo.ASCENDING).limit(int(top))
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
		_items = db.tododb.find().sort('close_time', pymongo.ASCENDING).limit(int(top))
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
		_items = db.tododb.find().sort('close_time', pymongo.ASCENDING).limit(int(top))
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
		_items = db.tododb.find().sort([('open_time',pymongo.ASCENDING)]).limit(int(top))
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
		_items = db.tododb.find().sort([('close_time',pymongo.ASCENDING)]).limit(int(top))
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
    app.run(host='0.0.0.0', port=80, debug=True)
