import json
import psycopg2
from flask import Blueprint, Response, render_template

data = Blueprint('data', __name__, template_folder='templates')
TOP_X = 10

@data.route('/data/markers')
def getMarkers():
    con = psycopg2.connect(database="civisAnalytics", user="gavin", host="/tmp/")
    cur = con.cursor()

    cur.execute("SELECT id, coordinates, routes FROM Stop")

    return Response(json.dumps(cur.fetchall()), mimetype='application/json')

@data.route('/data/markers/infoWindow/<markerId>')
def getInfoWindowContent(markerId):
    con = psycopg2.connect(database="civisAnalytics", user="gavin", host="/tmp/")
    cur = con.cursor()

    cur.execute("""
        PREPARE getInfoWindowContent as 
        SELECT S.on_street, S.cross_street, S.boardings::text, S.alightings::text
        FROM Stop S 
        WHERE S.id = $1"""
    )

    cur.execute("""
        PREPARE getRoutes as 
        SELECT name::text 
        FROM Route 
        WHERE id IN 
            (SELECT unnest(routes) FROM Stop WHERE id = $1)"""  
    )

    cur.execute("EXECUTE getInfoWindowContent('{markerId}')".format(markerId=markerId))
    results = cur.fetchone()

    cur.execute("EXECUTE getRoutes('{markerId}')".format(markerId=markerId))

    routes = []
    for route in cur.fetchall():
        routes.append(route[0])    

    return render_template("infoWindowContent.html", id=markerId, on_street=results[0], cross_street=results[1], routes=", ".join(routes), boardings=results[2], alightings=results[3])

@data.route('/data/aggregates/longestRoutes')
def getLongestRoutes():
    con = psycopg2.connect(database="civisAnalytics", user="gavin", host="/tmp/")
    cur = con.cursor()

    cur.execute("""
        SELECT routes FROM Stop
        """
    )

    routes = {}
    for routeList in cur.fetchall():
        for route in routeList[0]:
            cnt = routes.get(route, 0)
            routes[route] =  cnt + 1

    cur.execute("""
        SELECT name, id FROM Route ORDER BY id
        """
    )

    for row in cur.fetchall():
        routes[row[0]] = routes.pop(row[1])

    longest = sorted(routes.items(), key=lambda x: x[1], reverse=True)[:TOP_X]

    return render_template("aggregateTable.html", x="Route Name", y="# of Stops", rows=longest)

@data.route('/data/aggregates/embeddedStops')
def getMostEmbeddedStops():
    con = psycopg2.connect(database="civisAnalytics", user="gavin", host="/tmp/")
    cur = con.cursor()

    cur.execute("""
        SELECT on_street, cross_street, array_length(routes, 1) AS numRoutes 
        FROM Stop 
        ORDER BY numRoutes DESC
        LIMIT {top_x}
        """.format(top_x=TOP_X)
    )

    embedded = []
    for row in cur.fetchall():
        stop = []
        stop.append("{on_street} and {cross}".format(on_street=row[0], cross=row[1]))
        stop.append(row[2])
        embedded.append(stop)    

    return render_template("aggregateTable.html", x="Stop Location", y="# of Routes", rows=embedded)
