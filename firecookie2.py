#!/usr/bin/env python
 
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
 
import sys
import os
from datetime import datetime
import sqlite3
 
def Usage():
    print "{0} cookie-fullpath output-file".format(sys.argv[0])
    sys.exit(1)
 
if len(sys.argv)<3:
    Usage()
 
sqldb=sys.argv[1]
destfile=sys.argv[2]
# Some dates in the cookies file might not be valid, or too big
MAXDATE=2049840000
 
# cookies file must be there, most often file name is cookies.sqlite
if not os.path.isfile(sqldb):
    Usage()
 
# Bind to the sqlite db and execute sql statements
conn=sqlite3.connect(sqldb)
cur=conn.cursor()
try:
    data=cur.execute('select * from moz_cookies')
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
