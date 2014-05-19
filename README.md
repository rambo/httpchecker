# URL checker

Reads a YAML config file for urls to check against given rules, then checks them periodically and logs the results to sqlite database/logfile.

# Installing

  1. Prepare a new virtualenv
  3. unpack the archive
  2. pip install -r requirements.txt

# running

  python main.py config.yml

The process will keep in foreground until interrupted by appropriate signal.
