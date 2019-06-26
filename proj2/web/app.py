from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route("/")
@app.route("/index")
def hello():
    return render_template("trivia.html")

##ERROR PAGES
##http://flask.pocoo.org/docs/1.0/patterns/errorpages/ 


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404

@app.errorhandler(403)
def page_forbidden(e):
    # note that we set the 403 status explicitly
    return render_template('403.html'), 403

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')
