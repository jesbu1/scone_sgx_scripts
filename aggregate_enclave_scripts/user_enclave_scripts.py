import sys
# from flask import Flask, request, Response
import json
import ast
import os
import http.client
data_path = "scone_sgx_scripts/aggregate_enclave_scripts/mock_data.json"
json_data = json.load(open(data_path))

def query(query_type, e_id, aggregator_ip, privacy_budget):
    if query_type == "sum":
        try:
            h1 = http.client.HTTPConnection(aggregator_ip)
            user_data = json_data[e_id]["data"]["speeds"]
            # print(user_data)
            if user_data == []:
                data = json.dumps({'response':'none'})
            else:
                remaining_budget = float(json_data[e_id]["privacy_budget"])
                privacy_budget = float(privacy_budget)
                if remaining_budget >= privacy_budget:
                    data = json.dumps({'response':'yes', 'value': sum(user_data)})
                    json_data[e_id]["privacy_budget"] = remaining_budget - privacy_budget
                    with open(data_path, "w") as jsonFile:
                        json.dump(json_data, jsonFile)
                else:
                    data = json.dumps({'response':'none'})
            h1.request("POST", "/add_to_query_list", data)
        except:
            data = json.dumps({'response':'none'})
            h1.request("POST", "/add_to_query_list", data)
    else:
        raise NotImplementedError

if __name__ == "__main__":
    #install('requests')
    print(sys.argv)
    query_type = sys.argv[1]
    enclave_id = sys.argv[2]
    aggregator = sys.argv[3]
    privacy_budget = sys.argv[4]
    query(query_type, enclave_id, aggregator, privacy_budget)
