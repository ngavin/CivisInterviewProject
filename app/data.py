import json
import psycopg2
import re
from flask import Blueprint, Response, render_template

data = Blueprint('data', __name__, template_folder='templates')

@data.route('/data/markers')
def getMarkers():
    con = psycopg2.connect(database="civisAnalytics", user="gavin", host="/tmp/")
    cur = con.cursor()

    cur.execute("SELECT id, coordinates, routes FROM Stop")
    results = cur.fetchall()

    return Response(json.dumps(results), mimetype='application/json')

@data.route('/data/markers/infoWindow/<markerId>')
def getInfoWindowContent(markerId):
    con = psycopg2.connect(database="civisAnalytics", user="gavin", host="/tmp/")
    cur = con.cursor()

    cur.execute(
        "PREPARE getInfoWindowContent as "
        "SELECT S.on_street, S.cross_street, S.boardings::text, S.alightings::text "
        "FROM Stop S "
        "WHERE S.id = $1"
    )

    cur.execute(
        "PREPARE getRoutes as "
        "SELECT name::text "
        "FROM Route "
        "WHERE id IN "
            "(SELECT unnest(routes) FROM Stop WHERE id = $1)"  
    )

    cur.execute("EXECUTE getInfoWindowContent('{markerId}')".format(markerId=markerId))
    results = cur.fetchone()

    cur.execute("EXECUTE getRoutes('{markerId}')".format(markerId=markerId))
    routeResults = cur.fetchall()

    routes = []
    for route in routeResults:
        routes.append(route[0])    

    return render_template("infoWindowContent.html", id=markerId, on_street=results[0], cross_street=results[1], routes=", ".join(routes), boardings=results[2], alightings=results[3])
