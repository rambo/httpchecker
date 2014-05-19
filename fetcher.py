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

    def init_time(self):
        """Initializes the timing variables"""
        self.started = time.time()
        self.tto = None
        self.tte = None
        self.ttfb = None
        self.ttlb = None

    def get(self, url):
        """Wraps get_instrumented for a bit of error handling"""
        self.httpcode = None
        try:
            self.get_instrumented(url)
        except urllib2.HTTPError, e:
            self.tte = time.time() - self.started
            self.httpcode = e.code
            return False
        else:
            return True

    def get_instrumented(self, url):
        """Gets contents of a given URL, and does a bit of instrumentation in between"""
        self.body = None
        request = urllib2.Request(url)
        self.init_time()
        resp = self.opener.open(request)
        self.tto = time.time() - self.started
        self.body = resp.read(1)
        self.ttfb = time.time() - self.started
        self.body += resp.read()
        self.ttlb = time.time() - self.started


if __name__ == '__main__':
    print "use main.py"
    sys.exit(1)
