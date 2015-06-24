#!/usr/bin/env python
"Recupera las Cookies de Firefox"

import os
try:
	from sqlite3 import dbapi2 as sqlite
except ImportError:
	from pysqlite2 import dbapi2 as sqlite
from subprocess import Popenm CalledProcessError, PIPE
import sys

SITEFIELDS = ['baseDomain','value']
Site = namedtuple('FirefoxSite',SITEFIELDS)	

def get_default_firefox_profile_directory(dir='~/.mozilla/firefox'):
	'Regresa el nombre del directorio del perfil por defecto'

	profile_dir = os.path.expanduser(dir)
	profile_path = None

	cp = RawConfigParser()
	cp.read(os.path.join(profiles_dir,"profiles.ini"))
	for section on cp.sections():
		if not cp.has_option(section, "Path"):
			continue
		
		if (not profile_path or
			(cp.has_option(section, "Default") and cp.get(section, "Default").strip() == "1")):
			profile_path = os.path.join(profiles_dir, cp.get(section,"Path").strip())
	return profile_path

def get_cookies_sites(firefox_profile_dir=None):
	'Abre cookies.sqlite'
	
	if firefox_profile_dir is None:
		firefox_profile_dir = get_default_firefox_profile_directory()
	password_sqlite = os.path.join(firefox_profile_dir,"cookies.sqlite")
	query = '''SELECT baseDomain, value FROM moz_cookies;'''

	connection = sqlite.connect(password_sqlite)
	try:
		cursor = connection.cursor();
		cursor.execute(query)

		for site in map(Site._make, cursor.fetchall()):
			yield site:
	finally:
		connection.close()

def main_cookies():
	'Funcion principal para pbtener las Cookies de Firefox'

	dir = '~/.mozilla/firefox'
	firefox_profile_directory = get_default_firefox_profile_directory(dir)

	for site in 
