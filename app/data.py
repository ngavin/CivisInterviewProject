import json
import psycopg2
import re
from flask import Blueprint, Response, render_template

data = Blueprint('data', __name__, template_folder='templates')

@data.route('/data/markers')
def getMarkers():
    con = psycopg2.connect(database="civisAnalytics", user="gavin", host="/tmp/")
    cur = con.cursor()

    cur.execute("SELECT id, coordinates FROM Stop")
    results = cur.fetchall()

    data = []
    cleanse = re.compile(r"\(|\'|\)|\s")
    for stop in results:
        data.append(cleanse.sub("", str(stop)).split(","))

    return Response(json.dumps(data), mimetype='application/json')

@data.route('/data/markers/infoWindow/<markerId>')
def getInfoWindowContent(markerId):
    con = psycopg2.connect(database="civisAnalytics", user="gavin", host="/tmp/")
    cur = con.cursor()

    cur.execute(
        "PREPARE getInfoWindowContent as "
        "SELECT on_street, cross_street, routes, boardings::text, alightings::text "
        "FROM Stop "
        "WHERE id = $1"
    )

    cur.execute("EXECUTE getInfoWindowContent('{markerId}')".format(markerId=markerId))
    results = cur.fetchone()

    return render_template("infoWindowContent.html", id=markerId, on_street=results[0], cross_street=results[1], routes=", ".join(results[2]), boardings=results[3], alightings=results[4])
