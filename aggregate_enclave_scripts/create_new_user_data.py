import sys
import json

def create_new_user_data(n):
	json_str = "{"
	for i in range(1, n+1):
		json_str += '"a' + str(i) + '"' + ': {"ip": "127.0.0.1", "local_tunnel": "https://friendly-dog-0.localtunnel.me", "port": "8040", "data": {"end_ts": 1500982957, "sensed_mode": 2, "start_stop": {"$oid": "59780c0388f6630e9e15fb64"}, "duration": 181, "speeds": [0.0, 1.5, 1.0, 1.0, 2.0, 0.5, 0.0, 0.0], "distances": [0.0, 59.09202714889158, 34.17619592486318, 27.72127007665632, 53.23523225567902, 7.583539411079733, 4.904789652679724, 0.16229358259470306], "start_fmt_time": "2017-07-25T08:39:36-03:00", "start_loc": {"type": "Point", "coordinates": [-46.70812, -23.5720217]}, "distance": 186.87534805244425, "end_loc": {"type": "Point", "coordinates": [-46.7091967, -23.57178]}, "start_ts": 1500982776, "source": "SmoothedHighConfidenceMotion", "end_fmt_time": "2017-07-25T08:42:37-03:00", "trip_id": {"$oid": "59780c0388f6630e9e15fb53"}}, "_id": {"$oid": "59780c0388f6630e9e15fb5b"}, "privacy_budget": 10.0, "metadata": {"write_fmt_time": "2017-07-25T20:26:59.207442-07:00", "write_ts": 1501039619.207442, "time_zone": "America/Los_Angeles"}}, '
	json_str = json_str[:len(json_str)-2] + "}"
	with open("exp_data.json", "w") as jsonFile:
		json.dump(json.loads(json_str), jsonFile)
	return "Completed!"

if __name__ == "__main__":
    print(create_new_user_data(int(sys.argv[1])))

