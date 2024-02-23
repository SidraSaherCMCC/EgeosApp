import json
import requests
from django.urls import reverse

class TotalFlow:
    def __init__(self):
        # API URLs
        self.create_features_url = "http://127.0.0.1:8000/egeos-adaptor/load_create_features_object/"
        self.run_forecast_url = "http://127.0.0.1:8000/egeos-adaptor/run_forecast_modelling"
        self.convert_event_to_request_payload = "http://127.0.0.1:8000/egeos-adaptor/convert_event_to_request_payload/"

    def load_create_features_object(self, file_id):
        # Call the load_create_features_object API
        response = requests.get(f"{self.create_features_url}{file_id}/")
        return response.json()

    def run_forecast_modelling(self, request_body):
        # Prepare the request payload
        print("here")
        payload = {
            "request_body": json.dumps(request_body),
        }
        print(payload)
        # Call the run_forecast_modelling API
        response = requests.post(self.run_forecast_url, json=payload)

        return response.json()
    

    def createpayloadforSSA(self,event_object):
        #url = reverse('convert_event_to_request_payload')
        payload = {
            "feature_collection": json.dumps(event_object)
        }
        print("created payload")
        response = requests.post(self.convert_event_to_request_payload, json=payload)

        if response.status_code == 200:
            print("API call successful")
            # Additional handling based on the API response
        else:
            print("API call failed")
        return response

    def run_total_flow(self, file_id):
        # Step 1: Load features object
        print("load_create_features_object")
        features_object = self.load_create_features_object(file_id)
        print("features object")
        #print(features_object['content'])
        # Step 2: Run forecast modelling
        feature_collection=features_object['content']
        response = self.createpayloadforSSA(feature_collection)
        print(response)
        #response = self.run_forecast_modelling(feature_collection)


        return response

