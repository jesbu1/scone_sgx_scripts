import sys
import requests
from flask import Flask, request, Response
import json
import uuid
import threading
import abc
import numpy as np

app = Flask(__name__)

class Query(abc.ABC):
    """
    ABC is an abstract base class to define an interface for all queries
    """
    @abc.abstractmethod
    def run_query(self, data):
        pass

    @abc.abstractmethod
    def generate_noise(self, data):
        pass

    @abc.abstractmethod
    def __repr__(self):
        pass

class Sum(Query):
    def __init__(self):
        self.id = uuid.uuid4()

    def run_query(self, data):
        self.amount_of_noise = 0
        total = 0
        for enclave in data.keys():
            try:
                value = float(data[enclave])
            except:
                continue
            total += value
            self.amount_of_noise += 1
        return total

    def generate_noise(self, data):
        sensitivity = 1
        epsilon = 0.5
        n = len(data)
        return np.random.laplace(scale=(n * sensitivity)/epsilon)


    def __repr__(self):
        return "sum"

@app.route('/start_query', methods=['POST'])
def start_query():
    """
    1. Ask all servers stored in file/argument if they wanna respond to query
    2. Store who wants to respond to query
    3. Run query according to the query object passed in
    4. Generate noise according to the query object passed in and add to query val
    5. Return the noise
    """
    query_mapping = {'sum' : Sum()} #TODO: Fill in query mapping from string to object
    enclaves_in_query = {}
    query_object = query_mapping[request.data.decode("utf-8")]

    list_of_enclaves = ["18f729d9838a4e8ab66c3a6aac2ecdb0", "28f729d9838a4e8ab66c3a6aac2ecdb0", "38f729d9838a4e8ab66c3a6aac2ecdb0"] #open('FILE FOR ALL USER ENCLAVES AND ADDRESSES')
    def send_requests_async(enclave):
        try:
            user_data = json_data[enclave]
            if user_data != []:
                r = requests.post("http://" + user_data['ip'] + ':' + user_data['port'] + "/query",
                 data=str([json.dumps(user_data), str(query_object)]))
                r = json.loads(r.text)
                if r['response'] != 'no':
                    enclaves_in_query[enclave] = r['data']
        except:
            return
    threads = []
    for enclave in list_of_enclaves:
        thread = threading.Thread(target=send_requests_async(enclave))
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()
    print(enclaves_in_query)
    value = query_object.run_query(enclaves_in_query)
    noise = query_object.generate_noise(enclaves_in_query)
    return str(value + noise)
# @app.route("/send_data", methods=['POST'])
# def send_data():
#     """
#     Mock Controller

#     Parse mock json data and send data to the user enclaves.
#     """
#     query_type = request.data.decode("utf-8")
#     print(query_type)
#     if query_type == "sum":
#         user_data = json_data["18f729d9838a4e8ab66c3a6aac2ecdb0"]
#         print(user_data)
#         if user_data == []:
#             return json.dumps({'response':'none'})
#         else:
#             #return json.dumps({'response':'yes', 'data': sum(user_data)})
#             requests.post("http://127.0.0.1:8010/query", data=str([json.dumps(user_data), query_type]))
#     else:
#     	return json.dumps({'response':'no'})

if __name__ == "__main__":
    json_data = json.load(open("mock_data.json"))
    #print(json_data["18f729d9838a4e8ab66c3a6aac2ecdb0"]["data"]["speeds"])
    app.run(debug=True, port=8010) # Different port than the agg script.