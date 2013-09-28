from lib import mongolog
from flask import Flask, request, abort, jsonify, json, Response  # , render_template
# from lib.conf import load_config
import StringIO


app = Flask(__name__)
# config = load_config()

#from rest_resources import home

@app.route("/")
def hello():
    return "mongov is ready."

@app.route('/env')
def get_env():
    vars = {}
    for k in ['MONGOVIZ_PORT', 'MONGOVIZ_HOST']:
        vars[k] = mongolog.get_config(k)
    return "env: %s" % json.dumps(vars)

@app.route('/mongolog/<env>/<query_name>')
def mongolog_resource(env, query_name):
    #?format=json&key=XXXX
    fmt = request.args.get('format', 'json')
    test_key = request.args.get('key', None)
    real_key = mongolog.get_config('MONGOVIZ_API_KEY')
    if not test_key or test_key != real_key:
        print "failed key: %s != %s" % (test_key, real_key)
        abort(403)

    db = mongolog.get_mongo_db(env)
    data = mongolog.execute_query(db, query_name)

    if 'json' == fmt:
        return mongolog.to_json(data)
    elif 'csv' == fmt:
        output = StringIO.StringIO()
        data = mongolog.to_csv(data, output=output).getvalue()
        resp = Response(data, mimetype='text/csv')
        resp.headers['Content-Disposition'] = 'attachment; filename=' + env + '-' + query_name + '.csv'
        return resp

    return ''


## this doesnt get called by heroku foreman
if '__main__' == __name__:
    host=mongolog.get_config('MONGOVIZ_HOST')
    port = 5010
    # port=int(mongolog.get_config('port'))    
    print ("starting on port: %s" % port)
    print ("MONGOVIZ_API_KEY: %s" % mongolog.get_config('MONGOVIZ_API_KEY') )
    # app.run(host=config.get('server:main', 'host'), port=int(config.get('server:main', 'port')), debug=True)
    app.run(host=host, port=port, debug=True)

