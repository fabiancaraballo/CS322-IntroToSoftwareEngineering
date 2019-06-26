import os
from flask import Flask, redirect, url_for, request, render_template, jsonify
from pymongo import MongoClient
import arrow
import acp_times
import config
import logging

app = Flask(__name__)
CONFIG = config.configuration()
app.secret_key = CONFIG.SECRET_KEY

#Step 1: Create a client object
#The environment variable DB_PORT_27017_TCP_ADDR
client = MongoClient('db', 27017)

#Connect to the DB
db = client.tododb

db.tododb.delete_many({})  #This will help clear the database from the last time it was ran so you don't get conflicting times 


@app.route('/')
@app.route('/index')
def index():
    app.logger.debug("Main page entry")
    return render_template('calc.html')

#app.errorhandler(404)
#def page_not_found(error):
#    app.logger.debug("Page not found")
#    #flask.session['linkback'] = flask.url_for("index")
#    return render_template('404.html'), 404



##############
#
# This is where we implement our logic for proj5
#
##############

#Added from proj4-brevets
@app.route("/_calc_times")
def _calc_times():
    """
    Calculates open/close times from miles, using rules
    described at https://rusa.org/octime_alg.html.
    Expects one URL-encoded argument, the number of miles.
    """
    app.logger.debug("Got a JSON request")
    km = request.args.get('km', 999, type=float)
    brevet_dist= request.args.get('brev_dis', 999, type=float)
    start_time = request.args.get('start_t', 999, type=str)
    start_date = request.args.get('start_d', 999, type=str)
    time_str = "{}T{}".format(start_date, start_time)
    time = arrow.get(time_str)

    app.logger.debug("start time = {}".format(start_time))
    app.logger.debug("start date = {}".format(start_date))
    app.logger.debug("km={}".format(km))
    app.logger.debug("request.args: {}".format(request.args))


    # FIXME: These probably aren't the right open and close times
    # and brevets may be longer than 200km

    open_time = acp_times.open_time(km, brevet_dist, time.isoformat())

    close_time = acp_times.close_time(km, brevet_dist, time.isoformat())

    rslt = {"open": open_time, "close": close_time}
   
    print("\n".join("{}\t{}".format(k, v) for k, v in rslt.items()))
    #for key in rslt.keys():
    #    for value in rslt[key]:
    #        print(key,value)
 
    return jsonify(result=rslt)

#This is where we implement our own logic 
@app.route('/todo', methods=['POST'])
def todo():
    _items = db.tododb.find()
    items = [item for item in _items]

    #if the database is empty and "Display" is pressed than it will return an error page
    #else it will send the items to the database
    if items == []:
        return render_template('empty.html')
    else:
        return render_template('todo.html', items=items)

@app.route('/empty')
def empty():
    return render_template('empty.html')


@app.route('/new', methods=['POST'])
def new():
    open_data = request.form.getlist("open")
    close_data = request.form.getlist("close")
    km_data = request.form.getlist("km")

    open_times = [x for x in open_data if x != '']
    close_times = [x for x in close_data if x != '']
    km_lens = [x for x in km_data if x != '']

    print("Open data: ")
    print(' '.join(open_times))
    print()

    print("Close data: ")
    print(' '.join(close_times))
    print()

    print("KM data: ")
    print(' '.join(km_lens))
    print()
    
    list_length = len(open_times)
    
    for i in range(list_length):
        item_doc = {
            'km' : km_lens[i],
            'open_time': open_times[i],
            'close_time': close_times[i]
        }
        db.tododb.insert_one(item_doc)

     #This is used to find all the items in the database so we can check for error
     #Taken from todo()
    _items = db.tododb.find()
    items = [item for item in _items]
    
    #if the database is empty and "Submit" is pressed than it will return an error page
    #else it will send the items to the database
    if items == []:
        return redirect(url_for('empty'))
    else:
        return redirect(url_for('index'))



#############

#Added from proj4-brevets
app.debug = CONFIG.DEBUG
if app.debug:
    app.logger.setLevel(logging.DEBUG)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
