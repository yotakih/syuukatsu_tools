#!/usr/bin/python3
#-*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import codecs
from contextlib import closing
import glob
from urllib.request import urlopen
import os
import re
import sqlite3
import sys

def url2utf8file(url):
	t = ''
	with urlopen(url) as r:
		t = r.read()
	t = t.decode('cp932')
	t = t.replace('\r','')
	fn = re.search(r'.*jid=(\d*)&?.*', url).group(1)
	fn = fn + '.html'
	with open(fn, 'wb') as f:
		f.write(t.encode('utf-8'))

	return fn

def htmlparse(filename):
	t = ''
	with open(filename, 'r') as f:
		t = f.read()
	s = BeautifulSoup(t, 'html.parser')

	cnts = []
	cnts += [(
		'id'
		, os.path.splitext(
				os.path.basename(filename)
			)[0]
	)]
	cnts += [(
		'会社名'
		, s.select('li.current')[0].text
	)]

	for th in s.select('.tblDetail01 th'):
		h = th.text.replace('\t','').replace('\n','')
		v = th.find_next_sibling('td').select('p')
		v = ''.join([ repr(c) for c in v ])
		cnts += [(h,v)]

	cnts += [(
		'所在地',
		schComInf(s,'所在地')
	)]
	cnts += [(
		'従業員数',
		schComInf(s,'従業員数')
	)]

	return cnts

def schComInf(src,inf):
	if inf == '':
		return '';
	for th in src.select('.modDetail04 dt'):
		tmpInf = th.text.replace('\t','').replace('\n','')
		if inf == tmpInf:
			dd = th.find_next_sibling('dd')
			return dd.text

def add_cnts_fordb(cnts):
	with closing(sqlite3.connect('./workdb.sqlite3')) as con:
		cs = con.cursor()
		sql = 'insert into work({}) values({})'.format(
			','.join([ c[0] for c in cnts ])
			, ','.join([ "'{}'".format(c[1]) for c in cnts ])
		)
		cs.execute(sql)
		con.commit()

def ana_cnts(cnts):
	for c in cnts:
		print('%s : %s' % (c[0], c[1]))

def main():
	if len(sys.argv) < 2:
		print('arg error')
		sys.exit()
	arg = sys.argv[1]
	#url
	if re.match(r'http[s]*://', arg):
		arg = url2utf8file(arg)
	for fn in glob.iglob(arg):
		cnts = htmlparse(os.path.abspath(fn))
		add_cnts_fordb(cnts)

if __name__ == '__main__':
	main()
