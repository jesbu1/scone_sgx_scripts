import sys
# from flask import Flask, request, Response
import json
import ast
import os
import http.client

def query(query_type, e_id, aggregator_ip):
    if query_type == "sum":
        try:
            h1 = http.client.HTTPConnection(aggregator_ip)
            user_data = json_data[e_id]["data"]["speeds"]
            # print(user_data)
            if user_data == []:
                data = json.dumps({'response':'none'})
                h1.request("POST", "/add_to_query_list", data) 
            else:
                data = json.dumps({'response':'yes', 'value': sum(user_data)})
                h1.request("POST", "/add_to_query_list", data)
        except:
            data = json.dumps({'response':'none'})
            h1.request("POST", "/add_to_query_list", data)
    else:
        raise NotImplementedError

if __name__ == "__main__":
    #install('requests')
    print(sys.argv)
    json_data = json.load(open("scone_sgx_scripts/aggregate_enclave_scripts/mock_data.json"))
    query_type = sys.argv[1]
    enclave_id = sys.argv[2]
    aggregator = sys.argv[3]
    query(query_type, enclave_id, aggregator)
