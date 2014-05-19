#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import with_statement
import sys,os,signal
import yaml
from exceptions import NotImplementedError,RuntimeError

class main:
    def __init__(self, configfile):
        self.config_file_path = configfile
        self.load_config()
        self.hook_signals()

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
        NotImplementedError()

    def check_group(self):
        """Checks all urls in given group"""
        NotImplementedError()

    def check_one(self, group, urlkey):
        """Checks specific url in given group"""
        NotImplementedError()

    def reload(self):
        """Used to reload the config (and if we have """
        self.load_config()

    def load_config(self):
        """Loads (or reloads) the configuration file"""
        if not self.config_file_path:
            return False
        with open(self.config_file_path) as f:
            self.config = yaml.load(f)
        print self.config
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
