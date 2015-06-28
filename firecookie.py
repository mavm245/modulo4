#!/usr/bin/env python
"Recupera las Cookies de Firefox"

import os
from ConfigParser import RawConfigParser, NoOptionError
import sys
import sqlite3

def get_default_firefox_profile_directory():
	'Regresa el nombre del directorio del perfil por defecto'

	dir='~/.mozilla/firefox'
	profiles_dir = os.path.expanduser(dir)
	profile_path = None

	cp = RawConfigParser()
	cp.read(os.path.join(profiles_dir,"profiles.ini"))
	for section in cp.sections():
		if not cp.has_option(section, "Path"):
			continue
		
		if (not profile_path or
			(cp.has_option(section, "Default") and cp.get(section, "Default").strip() == "1")):
			profile_path = os.path.join(profiles_dir, cp.get(section,"Path").strip())
	return profile_path

def main_cookies():
	'Funcion principal para pbtener las Cookies de Firefox'

	''' Given a location to firefox cookie sqlite file
		Write its date param - expiry, last accessed,
		Creation time to a file in plain text.
		id
		baseDomain
		appId
		inBrowserElement
		name
		value
		host
		path
		expiry
		lastAccessed
		creationTime
		isSecure
		isHttpOnly
		python /home/daniel/python/cookie_viewer.py $(find /home/daniel/ -type f -name 'cookies.sqlite' | head -1) /tmp/test.txt 
	'''
	 
	 
	destfile='/tmp/cookies.txt'
	 
	# Bind to the sqlite db and execute sql statements
	firefox_profile_directory = get_default_firefox_profile_directory()
	sqldb = os.path.join(firefox_profile_directory,"cookies.sqlite")
	conn=sqlite3.connect(sqldb)
	query = '''SELECT * FROM moz_cookies;'''
	cur=conn.cursor()
	try:
		data=cur.execute(query)
	except sqlite3.Error, e:
		print 'Error {0}:'.format(e.args[0])
		sys.exit(1)
	mydata=data.fetchall()
	 
	# Dump results to a file
	with open(destfile, 'w') as fp:
		for item in mydata:
			urlname=item[1]
			urlname=item[1]
			cookie=str(item[5])
			fp.writelines(urlname + ' -- ' + cookie)
			fp.writelines('\n')
	 
	# Dump to stdout as well
	with open(destfile) as fp:
		for line in fp:
			print line

if __name__ == "__main__" :
	sys.exit (main_cookies())
