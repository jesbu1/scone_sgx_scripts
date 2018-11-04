import sys
from flask import Flask, request, Response
import json
app = Flask(__name__)


@app.route("/query", methods=['POST'])
def query():
    """
    1. Make sure controller is the one querying
    2. Ensure user wants to respond to this type of query
    3. Return value
    """
    if aggregate_ip != request.remote_addr:
    	return json.dumps({'response':'screw off, fake aggregator'})
    query_type = request.data
    if query_type == "sum":
    	loaded_json = json.loads(json_data)
    	user_data = loaded_json[user]['speeds']
    	if user_data == []:
    		return json.dumps({'response':'none'})
    	else:
    		return json.dumps({'response':'yes', 'data': sum(user_data)})
    else:
    	return json.dumps({'response':'no'})

if __name__ == "__main__":
	nonlocal aggregate_ip, user
	aggregate_ip = sys.argv[1]
	user = int(sys.argv[2])