#!/usr/bin/env python

#import logging
import os
import sys
import json
import csv
# import io
# from pprint import pprint
import argparse
import pymongo
from queries import query_list
import ConfigParser

#log = logging.getLogger(__name__)
from conf import load_config


def get_config(k):
    try:
        v = os.environ[k]
    except:
        v = ""

    print "config %s is %s" % (k, v)
    return v

def get_mongo_db(env_name):

    db = None
    db_param = "MONGOVIZ_" + env_name.upper() + "_MONGO_URI"
    db_uri = get_config(db_param)

    # config = load_config()
    # db_uri = config.get('app:main', db_param)

    try:
        client = pymongo.MongoClient(db_uri)
        db_name = db_uri.split('/')[-1]
        db = client[db_name]
    except ConfigParser.NoOptionError:
        raise RuntimeError("Unrecognized environment")

    return db


def execute_query(db, qname):
    query = query_list[qname]
    # so = query['sort']
    # print "so", type(so)

    q = query['q']
    proj = query.get('proj', None)
    proj['_id'] = 0
    #if proj:   # add some other defaults only if something is set, otherwise everything
    #    proj['_id'] = 0
    #    proj['event'] = 1
    #    proj['ts'] = 1
    #    proj['app:client_ver'] = 1

    s = query.get('sort', ['ts', -1])
    limit = query.get('limit', 1000)

    cursor = db.metrics.find(q, proj)

    if s:
        cursor.sort(*s)

    if limit:
        cursor.limit(limit)

    data = [r for r in cursor]
    return data


def json_encoder(obj):
    if hasattr(obj, 'isoformat'):
        return obj.isoformat().split('.')[0]


def to_csv(data, delim=",", output=sys.stdout):
    writer = csv.writer(output, delimiter=delim)

    writer.writerow(data[0].keys())
    for row in data:
        # print row.keys()
        # print row.values()
        # if c == 0:
        #     # first row
        #     output.writerow(row.keys() )
        #     c += 1
        writer.writerow(row.values())
    # out.writerow(data)
    # print(json.dumps(data, default=json_encoder, sort_keys=True, indent=4, separators=(',', ': ')))
    return output


def to_json(data):
    jdata = (json.dumps(data, default=json_encoder, sort_keys=True, indent=4, separators=(',', ': ')))
    return jdata


if '__main__' == __name__:

    if len(sys.argv) > 1 and sys.argv[1] in ["-l", "--list"]:
        print("Supported queries")
        for q in sorted(query_list.keys()):
            print("    {q} - {desc}".format(q=q, desc=query_list[q]['desc']))

        sys.exit()

    parser = argparse.ArgumentParser()
    parser.add_argument("env", help="environment: dev|stag|prod|test")
    parser.add_argument("query_name")
    parser.add_argument("-f", "--format", help="format: json|csv")
    # adding argument here just to make it display in help
    parser.add_argument("-l", "--list", action='store_true', help="display list of currently supported queries")
    args = parser.parse_args()

    if args.query_name not in query_list:
        raise RuntimeError("Unrecognized query name")

    db = get_mongo_db(args.env)
    #print(db)
    #print(db.collection_names())
    #print(db.metrics)

    data = execute_query(db, args.query_name)

    if args.format == "csv":
        out = to_csv(data)
    elif args.format == "tsv":
        out = to_csv(data, "\t")
    else:
        jdata = to_json(data)
        print(jdata)

