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

you need to setup your environment with the correct DB config variables
copy the example file:

    cp conf/install.example conf/install

and edit it to add your own DB variables.
that will take care of running the app on heroku, but to run the web app locally, you also need these env variables.
We recommend using [foreman](http://blog.daviddollar.org/2011/05/06/introducing-foreman.html) which is installed by default with heroku's toolbelt. it will read a .env file in the app root.
copy the example:

    cp conf/env.example .env

and edit the new .env file. 

you can run the app with:

    bin/run



mongolog command line tool
==========================

### install/first time only
check you have [virtualenv](https://pypi.python.org/pypi/virtualenv) installed

create a new virtualenv:

    virtualenv venv

activate the virtual env:

    source venv/bin/activate

install the required libraries:

    pip install -r requirements.txt

if you want to connect to a different mongoDB instance, add the login info for that to the file in
`mongolog/mongolog.conf`

### daily usage

you need to activate the python "virtual env" to run the tool.

    source venv/bin/activate

after that just run the queries!


### Basic syntax

usage:

    mongolog.py [-h] [-f FORMAT] env query_name

parameters:
- **env**: the name of environment against which to execute queries (can be either dev, stag or prod) 
- **query**: the name of the query. you can add new queries in the queries.py file.
- **--format -f**: output format: tsv|csv|json

example: 
*from staging env, show tutorial events for the last day, output in JSON format*

    python mongolog.py stag tutorial-daily -f json


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

mongolog日本語説明
-----------------

### インストール

仮想環境の設定
参考： https://pypi.python.org/pypi/virtualenv

    virtualenv venv

仮想環境を起動：

    source venv/bin/activate

ライブラリーをインストールする：

    pip install -r requirements.txt


### usage:

    mongolog.py [-h] [-f FORMAT] env query_name

- **env** 実行環境サーバー  dev | stag | prod
新規環境は.confで追加できます

- **query** クエリの名前
- **-f --format** 書き出す形式　tsv|csv|json　(optional) 

事例:
staging環境から一日分のチュートリアルデーター(`tutorial-daily`のクエリー)をcsv形式で書き出す

    python mongolog/mongolog.py stag tutorial-daily -f csv

### queriesを追加するには

queries.pyファイルの中でクエリを定義することができます。
例えば：

    'cashflow': {
        'q':  {'event': 'cashflow'},
        'proj': {"type": 1, "amount": 1, "ts":1, "player:id":1 }
    }

- **q**: query to match
- **proj**: fields to include in output (projection)

参考：http://docs.mongodb.org/manual/core/read-operations/

簡単pythonですので、このようにも書けることが出来ます：

    'tutorial-daily': {
        'q':  {'event': 'Tutorial', 'ts': {"$gte": datetime.utcnow()-timedelta(days=1)}},
        'proj': tutorial_fields
    },

