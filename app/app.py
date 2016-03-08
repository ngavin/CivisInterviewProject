import psycopg2
from flask import Flask, Blueprint, render_template
from data import data

app = Flask(__name__)
app.debug = True

index = Blueprint('index', __name__, template_folder='templates')
app.register_blueprint(index)
app.register_blueprint(data)

api_key = "AIzaSyDAEWcpvx6no3lvWU26WiY4KmH3ZKGLXTc"

@app.route('/')
def index():
    con = psycopg2.connect(database="civisAnalytics", user="gavin", host="/tmp/")
    cur = con.cursor()

    cur.execute("SELECT DISTINCT id, name FROM Route ORDER BY name ASC")
    
    return render_template("index.html", routes=cur.fetchall())

if __name__ == '__main__':
    app.run()
