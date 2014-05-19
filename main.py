#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import with_statement
from exceptions import NotImplementedError,RuntimeError
import sys,os,signal
import yaml
import re
import logger, fetcher

DEBUG = True

class main:
    def __init__(self, configfile):
        self.config_file_path = configfile
        if not self.load_config():
            raise RuntimeError("Could not load config file %s" % configfile)
        self.regexes = {}
        self.precompile_regexes()
        self.hook_signals()
        self.logger = logger.logger_wrapper(configfile.replace('.yml', '') + ".db")
        self.fetcher = fetcher.fetcher()

    def hook_signals(self):
        """Hooks common UNIX signals to corresponding handlers"""
        signal.signal(signal.SIGTERM, self.quit)
        signal.signal(signal.SIGQUIT, self.quit)
        signal.signal(signal.SIGHUP, self.reload)

    def run(self):
        """Starts the mainloop"""
        # We have no mainloop yet, iterate once...
        self.iterate()

    def quit(self):
        """Quits the mainloop"""
        NotImplementedError("No mainloop yet")
        #self.mainloop.quit()

    def iterate(self):
        """Runs one iteration, eg all the checks once"""
        self.check_all()

    def check_all(self):
        """Checks all urls in all groups"""
        for group in self.config.keys():
            self.check_group(group)

    def check_group(self, groupkey):
        """Checks all urls in given group"""
        group = self.config[groupkey]
        for url in group:
            self.check_one(groupkey, url)

    def check_one(self, groupkey, urlkey):
        """Checks specific url in given group"""
        self.logger.new_session(groupkey, urlkey)
        group = self.config[groupkey]
        content_ok = None
        f = self.fetcher
        if f.get(urlkey):
            body = f.body
            if DEBUG:
                print "Fetched %s ok" % urlkey
            # The group is dict, so the url has content checks, do them.
            if isinstance(group, dict):
                content_ok = True
                for regex in group[urlkey]:
                    if not self.regexes.has_key(regex):
                        if DEBUG:
                            print "Skipped not precompiled (probably invalid) regex %s" % regex
                        continue
                    if not self.regexes[regex].search(body):
                        content_ok = False
                        self.logger.log_error(regex)
            self.logger.log_status(int(f.ttfb), f.httpcode, content_ok)
        else:
            if DEBUG:
                print "Fetching %s failed, code %d" % (urlkey, f.httpcode)
            self.logger.log_status(int(f.tte), f.httpcode, content_ok)

    def reload(self):
        """Used to reload the config (and if we have """
        if self.load_config():
            self.precompile_regexes()
        else:
            # PONDER: report the error somehow ?
            pass

    def precompile_regexes(self):
        """Precompiles the test regexes"""
        self.regexes = {}
        for group in self.config.keys():
            # The group might just contain list of urls...
            if not isinstance(self.config[group], dict):
#                if DEBUG:
#                    print "Group %s looks to contain only urls, value %s" % (group, repr(self.config[group]))
                continue
            for url in self.config[group].keys():
                for regex in self.config[group][url]:
                    try:
                        self.regexes[regex] = re.compile(regex)
                    except re.error, e:
                        # Log the error but don't choke
                        print "Failed to compile regex %s, error: %s" % (regex, e)
                        pass
#        if DEBUG:
#            print "self.regexes=%s" % repr(self.regexes)

    def load_config(self):
        """Loads (or reloads) the configuration file"""
        if not self.config_file_path:
            return False
        with open(self.config_file_path) as f:
            self.config = yaml.load(f)
        return True


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "usage\n  main.py configfile\n"
        sys.exit(1)
    m = main(sys.argv[1])
    try:
        m.run()
    except KeyboardInterrupt:
        m.quit()
