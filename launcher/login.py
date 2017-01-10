#!/usr/bin/env python
# login.py
import sys
import MySQLdb as sql
import _mysql as my
# Note: Replace everything in the next statement
# with your own values
dbc = sql.connect(host='localhost',
                  user='username_here',
                  passwd='xxxxxxxx',
                  db='dbname_here')
cur = dbc.cursor()
cur.execute('SELECT handle password FROM users WHERE username="%s" AND password="%s"'%(sys.argv[1],sys.argv[2]))
if int(cur.rowcount) > 0:
    user = cur.fetchone()
else:
    user = 0

sys.exit(user)
