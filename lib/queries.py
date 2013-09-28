# example queries
# you will need to edit these to relate to your own DB and tables

from datetime import datetime, timedelta

tstoday = {"$gte": datetime.utcnow()-timedelta(days=1) }
tsweek  = {"$gte": datetime.utcnow()-timedelta(days=7) }

query_list = {

    'test': {
        'desc': "test query",
        'q':  {'ts': tstoday },
        'proj': {"player:uid":1, "ts":1 }
    },
    
    'test-ag': {
        'desc': 'aggregation query test',
        'type': 'aggregate',
        'q': {
            'match': {"event": "cashflow", 'ts': tstoday },
            'group': {"_id": "$player:name", "total": {"$sum": "$amount"}, "count": {"$sum": 1} }
        }
    }

}
