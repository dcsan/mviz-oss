# example queries
# you will need to edit these to relate to your own DB and tables

from datetime import datetime, timedelta

tutorial_fields = {
    "player:uid": 1, 
    "account:age:seconds": 1, 
    "step": 1, 
    'event':1,
    'EventMajor':1,
    'EventMinor':1,
    'EventData':1
    }

tstoday = {"$gte": datetime.utcnow()-timedelta(days=1) }
tsweek  = {"$gte": datetime.utcnow()-timedelta(days=7) }

tutorial_match_day  = {'event': 'Tutorial', 'ts': tstoday }

query_list = {

    'tutorial': {
        'desc': "Tutorial query",
        'q':  {'event': 'Tutorial'},
        'proj': tutorial_fields
    },

    'tutorial-day': {
        'desc': "Daily Tutorial query",
        'q':  tutorial_match_day,
        'proj': tutorial_fields
    },

    'tutorial-day-all': {
        'desc': "Daily Tutorial query with all fields",
        'q':  tutorial_match_day,
        'proj': {}
    },

    'tutorial-day-min': {
        'desc': "Daily Tutorial query with minimal fields",
        'q':  tutorial_match_day,
        'proj': {
            # "step": 1, 
            'event':1,
            'EventMajor':1,
            'EventMinor':1,
            'EventData':1
        }

    },

    'tutorial-week': {
        'desc': "Weekly Tutorial query",
        'q':  {'event': 'Tutorial', 'ts': tsweek },
        'proj': tutorial_fields
    },

    'tutorial-all': {
        'desc': "All of the tutorials",
        'q'     :  {'event': 'Tutorial'},
        'proj'  : {},
        'limit' : 5,
        'sort'  : ['ts', -1]
    },

    'register-day': {
        'desc': "Tutorial Test",
        'q'     :  {'event': 'register', 'ts': tstoday },
        'proj'  : {},
        'limit' : 5,
        'sort'  : ['ts', -1]
    },

    'login-day': {
        'desc': "Tutorial Test",
        'q'     :  {'event': 'login', 'ts': tstoday },
        'proj'  : {},
        'limit' : 5,
        'sort'  : ['ts', -1]
    },

    'cashflow': {
        'desc': "What users are buying?",
        'q'     :  {'event': 'cashflow'},
        'proj'  : {"type": 1, "amount": 1, "ts":1, "player:id":1 },
        'limit' : 5,
        'sort'  : ['ts', -1]
    },

    'boost-day': {
        'desc': "boosts today",
        'q':  {'event': 'boost', 'ts': {"$gte": datetime.utcnow()-timedelta(days=1)}},
        'proj'  : {'ts':1, 'deck:full_pct': 1},
        'sort'  : ['ts', -1]
    }

    #'quest-not-won': {
    #    'q':  {'event': 'quest:end', 'quest:won': None},
    #    'proj': {'quest:cname': 1, 'player:username': 1, 'app:client_ver': 1}
    #}
}
