import sys
import requests
from flask import Flask, request, Response
import json
import uuid
import threading
import abc
import numpy as np

app = Flask(__name__)
query_list = []

class RequestThread(threading.Thread):
    def __init__(self, controller, enclaves_in_query, query_object):
        threading.Thread.__init__(self)
        self.enclaves_in_query = enclaves_in_query
        self.controller = controller
        self.query_object = query_object

    def run(self):
        # for controller in controllers:
        r = requests.post("http://127.0.0.1:2000/request_query", data=str(self.query_object))
        # print(r.text)
        # r = json.loads(r.text)
        # for enclave in r:
        #     if enclave['response'] != 'no':
        #         self.enclaves_in_query[self.enclave] = r['Finished']

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
        #self.amount_of_noise = 0
        total = 0
        for value in data:
            total += int(value)
            # try:
            #     value = float(data[enclave])
            # except:
            #     continue
            #self.amount_of_noise += 1
        return total

    def generate_noise(self, data):
        sensitivity = 1
        epsilon = 0.5
        n = len(data)
        return np.random.laplace(scale=(n * sensitivity)/epsilon)


    def __repr__(self):
        return "sum"
@app.route('/')
def test():
    return "hello"

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

    #open('FILE FOR ALL USER ENCLAVES AND ADDRESSES')
    controller_map = {'35.236.79.116:2000': ["18f729d9838a4e8ab66c3a6aac2ecdb0", "28f729d9838a4e8ab66c3a6aac2ecdb0", "38f729d9838a4e8ab66c3a6aac2ecdb0"]}
    threads = []
    for controller, list_of_enclaves in controller_map.items():
        thread = RequestThread(controller, enclaves_in_query, query_object)
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()
    #print(enclaves_in_query)
    value = query_object.run_query(query_list)
    noise = query_object.generate_noise(query_list)
    clear_query_list()
    return str(value + noise)

@app.route('/add_to_query_list', methods=['POST'])
def add_to_query_list():
    data = json.loads(request.data)
    if data['response'] == 'yes':
        query_list.append(data['value'])

def clear_query_list():
    query_list = []

if __name__ == "__main__":
    json_data = json.load(open("mock_data.json"))
    #print(json_data["18f729d9838a4e8ab66c3a6aac2ecdb0"]["data"]["speeds"])
    app.run(host='0.0.0.0', port=80) # Different port than the agg script.
