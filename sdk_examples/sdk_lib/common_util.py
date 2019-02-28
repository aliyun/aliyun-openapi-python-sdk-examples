import json
import logging

class CommonUtil:
    @staticmethod
    def log(action, response_json):
        print("---------------------------"+action+"---------------------------")
        print(json.dumps(response_json, indent=2)+'\n')
