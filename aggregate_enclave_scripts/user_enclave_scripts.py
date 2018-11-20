import sys
import requests
# from flask import Flask, request, Response
import json
import ast
import os


"""
app = Flask(__name__)


@app.route("/query", methods=['POST'])
def query():
    #1. Make sure controller is the one querying
    #2. Ensure user wants to respond to this type of query
    #3. Return value
    # if aggregate_ip != request.remote_addr:
    # 	return json.dumps({'response':'screw off, fake aggregator'})
    # query_type = request.data.decode("utf-8")
    # print(q)
    input_list = request.data.decode("utf-8")
    input_list = ast.literal_eval(input_list)
    json_data, query_type = str(input_list[0]), input_list[1]
    print(json_data)
    print(query_type)
    if query_type == "sum":
        loaded_json = json.loads(json_data)
        user_data = loaded_json["data"]["speeds"]
        if user_data == []:
            return json.dumps({'response':'none'})
        else:
            print(sum(user_data))
            return json.dumps({'response':'yes', 'data': str(sum(user_data))})
    else:
        return json.dumps({'response':'no'})

if __name__ == "__main__":
    user = sys.argv[1]
    port = int(sys.argv[2])
    app.run(debug=False, port=port) # Different port than the agg script.
"""

import pip

def install(package):
    if hasattr(pip, 'main'):
        pip.main(['install', package])
    else:
        pip._internal.main(['install', package])


def query(query_type, e_id, aggregator_ip):
    if query_type == "sum":
    	aggregator_ip = aggregator_ip + "/add_to_query_list"
        try:
            user_data = json_data[e_id]["data"]["speeds"]
            # print(user_data)
            if user_data == []:
                data = json.dumps({'response':'none'})
                requests.push(aggregator_ip, data=data)
            else:
                data = json.dumps({'response':'yes', 'value': sum(user_data)})
                requests.push(aggregator_ip, data=data)
        except:
            data = json.dumps({'response':'none'})
            requests.push(aggregator_ip, data=data)
    else:
        raise NotImplementedError
if __name__ == "__main__":
    #install('requests')
    print(sys.argv)
    json_data = json.load(open("mock_data.json"))
    query_type = sys.argv[1]
    enclave_id = sys.argv[2]
    aggregator = sys.argv[3]
    query(query_type, enclave_id, aggregator)
