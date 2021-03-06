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


def _execute_find_query(db, query):
    q = query['q']
    proj = query.get('proj', None)
    proj['_id'] = 0

    s = query.get('sort', ['ts', -1])
    limit = query.get('limit', 1000)

    cursor = db.metrics.find(q, proj)

    if s:
        cursor.sort(*s)

    if limit:
        cursor.limit(limit)

    data = [r for r in cursor]
    return data


def _execute_aggregate_query(db, query):
    """
        'desc': 'Soft currency per player',
        'type': 'aggregate',
        'q': {
            'match': {"event": "cashflow", "currency": "HARD"},
            'group': {"_id": "$username", "total": {"$sum": "$amount"}}
        }
    """

    q = query['q']
    result = db.metrics.aggregate([
        {"$match": q['match']},
        {"$group": q['group']}
    ])

    #print(cursor)

    #s = query.get('sort', ['ts', -1])
    #if s:
    #    cursor.sort(*s)

    #limit = query.get('limit', 1000)
    #if limit:
    #    cursor.limit(limit)

    return result['result']


def execute_query(db, qname):
    #TODO: Aggregate support. Example:
    # db.players.aggregate( { $match: {"deck:max_slots": 4}}, {$group: {_id: "$username", total: { $sum: "$wallet:SOFT"}}})
    query = query_list[qname]
    # so = query['sort']
    # print "so", type(so)
    query_type = query.get('type', 'find')

    if 'find' == query_type:
        return _execute_find_query(db, query)
    elif 'aggregate' == query_type:
        return _execute_aggregate_query(db, query)


def json_encoder(obj):
    if hasattr(obj, 'isoformat'):
        return obj.isoformat().split('.')[0]


# Might be better to use proj to get keys, that way it's always consistent
# As it's written, the output will only have the set of all columns
# that are present.
def get_all_keys(data):
    """Get all keys from json data file"""
    all_keys = set(data[0].keys())
    for row in data:
        all_keys = set.union(all_keys, set(row.keys()))
    return list(all_keys)


def to_csv(data, delim=","):
    """docstring for to_csv"""
    output = csv.writer(sys.stdout, delimiter=delim)
    allKeys = get_all_keys(data)
    output.writerow(allKeys)
    for row in data:
        vs = []
        for k in allKeys:
            vs.append(row.get(k, None))
        output.writerow(vs)



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

