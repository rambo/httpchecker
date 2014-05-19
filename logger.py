#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys,os
from exceptions import NotImplementedError,RuntimeError
import sqlite3
# Decimal recipe from http://stackoverflow.com/questions/6319409/how-to-convert-python-decimal-to-sqlite-numeric
import decimal
# Register the adapter
sqlite3.register_adapter(decimal.Decimal, lambda d: str(d))
# Register the converter
sqlite3.register_converter("NUMERIC", lambda s: decimal.Decimal(s))
# Register converter&adapter for datetime in the same way
import datetime
sqlite3.register_adapter(datetime.datetime, lambda dt: dt.strftime("%Y-%m-%d %H:%M:%S.%f")[:23])
# The type on SQLite is "TIMESTAMP" even if we specified "DATETIME" in table creation...
sqlite3.register_converter("TIMESTAMP", lambda s: datetime.datetime.strptime(s.ljust(26,"0"), "%Y-%m-%d %H:%M:%S.%f"))

class logger:
    def __init__(self, logfilename):
        call_init_db = False
        if not os.path.exists(logfilename):
            call_init_db = True
        self.connection = sqlite3.connect(logfilename, detect_types=sqlite3.PARSE_DECLTYPES)
        self.cursor = self.connection.cursor()
        if call_init_db:
            self.init_db()     

    def init_db(self):
        """Initializes the database schema"""
        self.cursor.execute("CREATE TABLE sessions (id INTEGER PRIMARY KEY ASC, time TIMESTAMP DATETIME DEFAULT(STRFTIME('%Y-%m-%d %H:%M:%f', 'NOW')), groupkey TEXT, url TEXT);")
        # The timestamps on these tables are basically denormalized just in case we wish to do optimized time based searches in them.
        self.cursor.execute("CREATE TABLE status (sessionid INTEGER NOT NULL, time TIMESTAMP DATETIME DEFAULT(STRFTIME('%Y-%m-%d %H:%M:%f', 'NOW')), responsetime INTEGER, httpstatus INTEGER, contentstatus BOOLEAN, FOREIGN KEY(sessionid) REFERENCES sessions(id));")
        self.cursor.execute("CREATE TABLE contenterror (sessionid INTEGER NOT NULL, time TIMESTAMP DATETIME DEFAULT(STRFTIME('%Y-%m-%d %H:%M:%f', 'NOW')), testregex TEXT, FOREIGN KEY(sessionid) REFERENCES sessions(id));")
        self.cursor.execute("CREATE TABLE contenthistory (sessionid INTEGER NOT NULL, time TIMESTAMP DATETIME DEFAULT(STRFTIME('%Y-%m-%d %H:%M:%f', 'NOW')), html TEXT, FOREIGN KEY(sessionid) REFERENCES sessions(id));")
        self.connection.commit()

    def new_session(self, groupname, url):
        """Inserts a new session (combination of group and url in time) to the db and returns the ID"""
        self.cursor.execute("INSERT INTO sessions (groupkey, url) VALUES (?,?);", (groupname, url))
        self.connection.commit()
        return self.cursor.lastrowid

    def log_status(self, sessionid, responsetime, httpstatus, contentstatus):
        """Log the general status for a given URL in a given session"""
        self.cursor.execute("INSERT INTO status (sessionid, responsetime, httpstatus, contentstatus) VALUES (?,?,?,?);", (sessionid, responsetime, httpstatus, contentstatus))
        self.connection.commit()

    def log_content(self, sessionid, html):
        """Logs HTML content of session (ie url in time)"""
        self.cursor.execute("INSERT INTO contenthistory (sessionid, html) VALUES (?,?);", (sessionid, html))
        self.connection.commit()

    def log_error(self, sessionid, testregex):
        """Logs a content check error, basically just to tell us which of the content check failed"""
        self.cursor.execute("INSERT INTO contenterror (sessionid, testregex) VALUES (?,?);", (sessionid, testregex))
        self.connection.commit()
        


if __name__ == '__main__':
    print "use main.py"
    sys.exit(1)
