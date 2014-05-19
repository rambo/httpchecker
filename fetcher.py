#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from exceptions import NotImplementedError,RuntimeError
import urllib2
import time

class fetcher():
    def __init__(self):
        # Make a custom opener so we can time the response times
        self.opener = urllib2.build_opener()
        # Make sure the variables are initialized correctly
        self.init_time()
        self.started = None
        self.httpcode = None
        self.body = None
        self.ioerrno = None

    def init_time(self):
        """Initializes the timing variables"""
        self.started = time.time()
        self.tto = None
        self.tte = None
        self.ttfb = None
        self.ttlb = None

    def get(self, url):
        """Wraps get_instrumented for a bit of error handling, returns 1 for success, 0 for failure and -1 for I/O error"""
        self.httpcode = None
        self.ioerrno = None
        try:
            self.get_instrumented(url)
        except urllib2.HTTPError, e:
            self.tte = (time.time() - self.started) * 1000
            self.httpcode = e.code
            return 0
        except urllib2.URLError, e:
            self.tte = (time.time() - self.started) * 1000
            self.ioerrno = e.reason.errno
            return -1
        else:
            return 1

    def get_instrumented(self, url):
        """Gets contents of a given URL, and does a bit of instrumentation in between"""
        self.body = None
        request = urllib2.Request(url)
        self.init_time()
        resp = self.opener.open(request)
        self.tto = (time.time() - self.started) * 1000
        self.body = resp.read(1)
        self.ttfb = (time.time() - self.started) * 1000
        self.httpcode = resp.getcode()
        self.body += resp.read()
        self.ttlb = (time.time() - self.started) * 1000


if __name__ == '__main__':
    print "use main.py"
    sys.exit(1)
