#!/usr/bin/python3
#-*-coding:utf-8-*-

import sqlite3
from contextlib import closing

def cretbl(dbfile):
	with closing(sqlite3.connect(dbfile)) as con:
		s = con.cursor()
		sql = '''
CREATE TABLE work (id vachar(30),会社名 vachar(100),仕事内容 varchar(500),対象となる方 varchar(500),勤務地 varchar(500),勤務時間 varchar(500),雇用形態 varchar(500),給与 varchar(500),待遇・福利厚生 varchar(500),休日・休暇 varchar(500))
'''
		s.execute(sql)
		con.commit()

if __name__ == '__main__':
	cretbl('./workdb.sqlite3')
