#!/usr/bin/python

import json
import psycopg2
import sys

with open("sql/data.json") as data_file:
    
    con = None
    try:
        con = psycopg2.connect(database="civisAnalytics", user="gavin", host="/tmp/")
        cur = con.cursor()

        cur.execute(
            "PREPARE loadData as "
            "INSERT INTO Stop VALUES"
            "($1, $2, $3, $4, $5, $6, $7, $8, $9)"
            )

        data = json.load(data_file)
        for stop in data["data"]:
            tmp = "EXECUTE loadData ('{id}', '{on_street}', '{cross_street}', ARRAY[{routes}], '{boardings}', '{alightings}', '{creation}', '{daytype}', POINT'({x},{y})')".format(id=stop[8], on_street=stop[9], cross_street=stop[10], routes=stop[11], boardings=stop[12], alightings=stop[13], creation=stop[14], daytype=stop[15], x=stop[16][1], y=stop[16][2])
            print tmp;
            cur.execute(
                tmp)
            con.commit()
            break

        con.commit()

    except psycopg2.DatabaseError, e:
        print 'Database error:\n %s' % e
        sys.exit(1)

    finally:
        if con:
            con.close()
        sys.exit(0)
