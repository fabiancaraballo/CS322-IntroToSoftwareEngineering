"""
Replacement for RUSA ACP brevet time calculator
(see https://rusa.org/octime_acp.html)

"""

import flask
from flask import request
from flask import jsonify
import json
import arrow  # Replacement for datetime, based on moment.js
import acp_times  # Brevet time calculations
import config

import logging

###
# Globals
###
app = flask.Flask(__name__)
CONFIG = config.configuration()
app.secret_key = CONFIG.SECRET_KEY

###
# Pages
###


@app.route("/")
@app.route("/index")
def index():
    app.logger.debug("Main page entry")
    return flask.render_template('calc.html')


@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("Page not found")
    flask.session['linkback'] = flask.url_for("index")
    return flask.render_template('404.html'), 404


###############
#
# AJAX request handlers
#   These return JSON, rather than rendering pages.
#
###############
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
 
    return flask.jsonify(result=rslt)


#############

app.debug = CONFIG.DEBUG
if app.debug:
    app.logger.setLevel(logging.DEBUG)

if __name__ == "__main__":
    print("Opening for global access on port {}".format(CONFIG.PORT))
    app.run(port=CONFIG.PORT, host="0.0.0.0")
