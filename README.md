# URL checker

Reads a YAML config file for urls to check against given rules, then checks them periodically and logs the results to sqlite database/logfile.

# Installing

  1. Prepare and activate a new virtualenv
  3. unpack the archive
  2. pip install -r requirements.txt

# running

  ./main.py example.yml [check_interval]

The process will keep in foreground until interrupted by appropriate signal, check_interval is in seconds, the default is 15.

# Configuration format

This is YAML file, the first level must be a dictionary. Second level can be either list (just plain URLs) or dictionary (URLs with content checks), if the second level is dictionary the third level must be a list of regular expressions to test against the fetched source.

# Log format

The log is sqlite database (for especially read/search performance reasons) with the following tables

## sessions

The main entry point, everything else depends on this

### sessions.time

Millisecond accuracy timestamp.

### sessions.groupkey

The grouping key from the configuration file

### sessions.url

The URL this session refers to (in case the same URL has for example multiple content checks)

### sessions.allok

High-level view whether this session was fine or not.

## status

The general status table, shows response times, http/io error codes and if there were any issues with content checks

### status.sessionid

Foreign key to the sessions table (to get url and group)

### status.time

A separate timestamp for the status entry, to avoid JOINs if we want to just do some time-based analysis on these.

### status.responsetime

Response time in milliseconds 

### status.ioerror

If there was an IO error the code is stored here, NULL if not applicable.

### status.httpstatus

HTTP status code, NULL if not applicable (In case of IOError for example)

## status.contentstatus

Boolean value indicating whether all of the content checks were ok, NULL if not applicable (no content-checks defined, or we did not get a body to check against)

## contenterror

This just list the regexes that failed.

### contenterror.time

A separate timestamp for the contenterror entry, to avoid JOINs if we want to just do some time-based analysis on these.

### contenterror.sessionid

Foreign key to the sessions table (to get url and group)

### contenterror.testregex

The regex from config file that failed.

## contenthistory

Contains the HTML snapshot of the site during the check time.

### contenthistory.time

A separate timestamp for the contenterror entry, to avoid JOINs if we want to just do some time-based analysis on these.

### contenthistory.sessionid

Foreign key to the sessions table (to get url and group)

### contenthistory.html

The source HTML.

