import requests
import sys
def query(query_type):
	"""
	input_list = request.data.decode("utf-8")
    input_list = ast.literal_eval(input_list)
    json_data, query_type = str(input_list[0]), input_list[1]
    """
    print(json_data)
    print(query_type)
    if query_type == "sum":
        loaded_json = json.loads(json_data)
        user_data = loaded_json["data"]["speeds"]
        if user_data == []:
            return json.dumps({'response':'none'})
        else:
            return json.dumps({'response':'yes', 'data': str(sum(user_data))})
    else:
        return json.dumps({'response':'no'})

if __name__ == "__main__":
    query_type = sys.argv[1]
    aggregator_ip = sys.argv[2]
    query(query_type, aggregator_ip)