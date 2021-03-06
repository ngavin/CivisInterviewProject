import psycopg2
from flask import Flask, Blueprint, render_template
from data import data

app = Flask(__name__)
app.debug = True

index = Blueprint('index', __name__, template_folder='templates')
mapHtml = Blueprint('map', __name__, template_folder='templates')
aggregates = Blueprint('aggregates', __name__, template_folder='templates')
app.register_blueprint(index)
app.register_blueprint(mapHtml)
app.register_blueprint(data)

api_key = "AIzaSyDAEWcpvx6no3lvWU26WiY4KmH3ZKGLXTc"

con = None
# def dbConnection(f):
#     def wrap(*args, **kwargs):
#         global con
#         if not con:
#             con = psycopg2.connect(database="civisAnalytics", user="gavin", host="/tmp/")
#         return con

#     return wrap



@app.route('/')
def index():
    return render_template("index.html")

@app.route('/map')
def map():
    con = psycopg2.connect(database="civisAnalytics", user="gavin", host="/tmp/")
    cur = con.cursor()

    cur.execute("SELECT DISTINCT id, name FROM Route ORDER BY name ASC")
    
    return render_template("map.html", routes=cur.fetchall())

@app.route('/aggregates')
def aggregates():
    return render_template("aggregates.html")

if __name__ == '__main__':
    app.run()
