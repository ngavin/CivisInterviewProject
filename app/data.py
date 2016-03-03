import json
import psycopg2
import re
from flask import Flask, Blueprint, Response

data = Blueprint('data', __name__, template_folder='templates')

@data.route('/data/markers')
def getMarkers():
    con = psycopg2.connect(database="civisAnalytics", user="gavin", host="/tmp/")
    cur = con.cursor()

    cur.execute("SELECT id, coordinates FROM Stop")
    results = cur.fetchall()

    data = []
    cleanse = re.compile(r"\(|\'|\)")
    for stop in results:
        data.append(cleanse.sub("", str(stop)).split(","))

    return Response(json.dumps(data),  mimetype='application/json')
