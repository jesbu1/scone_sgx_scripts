from flask import Flask, request, Response
import requests
import numpy as np
import abc

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

app = Flask(__name__)

@app.route("/")
def hello():
    return "Jack sucks!"

@app.route('/start_query', methods=['POST'])
def start_query():
	"""
	1. Ask all servers stored in file/argument if they wanna respond to query
	2. Store who wants to respond to query
	3. Run query according to the query object passed in
	4. Generate noise according to the query object passed in and add to query val
	5. Return the noise
	"""
	query_mapping = {} #TODO: Fill in query mapping from string to object
	enclaves_in_query = {}
	query_object = query_mapping[request.data]

	list_of_enclaves = open('FILE FOR ALL USER ENCLAVES AND ADDRESSES')
	for enclave in list_of_enclaves:
		r = requests.post(enclave, data='Would you like to respond to this query?')
		if r.text != "NO":
			enclaves_in_query[enclave] = r

	value = query_object.run_query(enclaves_in_query) + query_object.generate_noise(enclaves_in_query)
	return str(value)


@app.route('/query-example', methods=['POST'])
def query_example():
    data = int(request.data)
    print(data)
    sensitivity = 1
    epsilon = 0.5
    n = 1
    return str(np.random.laplace(scale=(n * sensitivity)/epsilon) + data)



if __name__ == "__main__":
	app.run(debug=True, port='8080')