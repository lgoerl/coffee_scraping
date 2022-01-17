import os
import pickle

api_responses = dict()
rel_dir = "./src/dags/resources/api_clients/responses"
for p in [pkl for pkl in os.listdir(rel_dir) if ".pickle" in pkl]:
    with open(f"{rel_dir}/{p}", "rb") as f:
        response = pickle.load(f)
        api_responses[response.url] = response
