mongoviz
========
tools for working with metrics data in mongoDB

- mongoviz: mongo data vizualiser 
- mongolog: mongo data csv, json output
- [mongolog web app](#mongovweb): same output from flask app/rest api

 this outputs data from a command line or as a web app

[日本語の説明は下記に書いてま〜す！](#mongolog日本語説明)

mongolog web
============
requirements:
[virtualenv](https://pypi.python.org/pypi/virtualenv)
   
    virtualenv venv                     #create a new virtualenv
    source venv/bin/activate            # activate it
    pip install -r requirements.txt     # install the required libraries
    cp bin/setup/local.sh.example bin/setup/local.sh
    vim bin/setup/local.sh              # edit with your DB info
    source bin/setup/local.sh
    python lib/mongolog.py stag test   # run a test query against stag env.

### daily usage

    source venv/bin/activate        # activate the python virtualenv
    source bin/setup/local.sh       # setup local env vars needed for DB


mongolog command line tool
==========================

### Basic syntax

usage:

    mongolog.py [-h] [-f FORMAT] env query_name

parameters:
- **env**: the name of environment against which to execute queries (can be either dev, stag or prod) 
- **query**: the name of the query. you can add new queries in the queries.py file.
- **--format -f**: output format: tsv|csv|json

example: 
*from staging env, show tutorial events for the last day, output in JSON format*

    python lib/mongolog.py stag tutorial-daily -f json


### Adding New Queries

All queries that can be executed against environments are stored in queries.py file which contains a dictionary named query_list. The
key specifies the name of the query and it's value specifies the mongo query specs. For reference please look at these links

* http://api.mongodb.org/python/current/tutorial.html
* http://docs.mongodb.org/manual/core/read-operations/
* http://docs.mongodb.org/manual/tutorial/query-documents/

Note that since queries.py is a python code file you can use python functions etc in here, for example::

    'tutorials-weekly': {
        'q':  {'event': 'Tutorial', 'ts': {"$gte": datetime.utcnow()-timedelta(days=7)}},
        'proj': {"player:name": 1, "account:age:minutes": 1, "memTotal": 1}
    }

This sample query uses python's datetime module to get date 7 days back from now


mongovweb
-----------------
start with

    python webapp.py

then all the commands are available through the browser like:

    '$HOST/mongolog/<env>/<query_name>?key=$APIKEY&format=$FORMAT'

parameters:

| param     | explanation           |
|-----------|-----------------------|
| apikey    | your secret api key   |
| format    | json, csv             |

example:
http://localhost:5005/mongolog/stag/tutorial?key=777&format=csv


