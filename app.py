#!/usr/bin/python3
#-*-coding: utf-8 -*-

from flask import Flask, render_template
import sqlite3
from contextlib import closing

app = Flask(__name__)

@app.route('/')
def index():
	cntns = get_contents()
	return render_template('index.html', contents = cntns)

def get_contents():
	with closing(sqlite3.connect('./workdb.sqlite3')) as con:
		c = con.cursor()
		sql = 'select * from work order by id'
		cntnts = c.execute(sql).fetchall()
	return cntnts

if __name__ == '__main__':
	app.debug = True
	app.run(host = '0.0.0.0')
