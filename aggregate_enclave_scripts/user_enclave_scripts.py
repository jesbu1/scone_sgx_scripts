import sys
import requests
# from flask import Flask, request, Response
import json
import ast
import os

def query(query_type, e_id, aggregator_ip):
    if query_type == "sum":
    	aggregator_ip = aggregator_ip + "/add_to_query_list"
        try:
            user_data = json_data[e_id]["data"]["speeds"]
            # print(user_data)
            if user_data == []:
                data = json.dumps({'response':'none'})
                requests.post("http://" + aggregator_ip, data=data)
            else:
                data = json.dumps({'response':'yes', 'value': sum(user_data)})
                requests.post("http://" + aggregator_ip, data=data)
        except:
            data = json.dumps({'response':'none'})
            requests.post("http://" + aggregator_ip, data=data)
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
