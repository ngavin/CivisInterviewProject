#!/usr/bin/python

import psycopg2
import sys

con = None

try:
    con = psycopg2.connect(database="civisAnalytics", user="gavin", host="/tmp/")
    cur = con.cursor()

    cur.execute(
        "PREPARE loadData as "
        "INSERT INTO Stop VALUES"
        "($1, $2, $3, $4, $5, $6, $7, $8, $9)"
        )

    cur.execute(
        "EXECUTE loadData ('{id}', '{on_street}', '{cross_street}', '{routes}', '{boardings}', '{alightings}', '{creation}', '{daytype}', POINT'{coordinates}')".format(
        id=1, on_street="JOY", cross_street="HAGGERTY", routes="{1,3}", boardings=28.33, alightings=1.0, creation="2010-2-10", daytype="Weekday", coordinates="(20.200, -32.003)"
        ))

    con.commit()

except psycopg2.DatabaseError, e:
    print 'Database error:\n %s' % e
    sys.exit(1)

finally:
    if con:
        con.close()
    sys.exit(0)
    