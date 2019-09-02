from base64 import b64encode
import requests 
import json

API_KEY = "AIzaSyBRcVPi1HMQBQeffz4wIn92kdBNNZ0wXpM"
URL = "https://vision.googleapis.com/v1/images:annotate?key={}".format(API_KEY)

def make_request_json(buffer):
    image_json = {
        'content': b64encode(buffer).decode('UTF-8')
    }

    feature_json = {
        "type": "LABEL_DETECTION",
        "maxResults": "10"
    }

    request = {
        "requests": {
            "image": image_json,
            "features": feature_json
        }
    }

    return json.dumps(request)

def send_request(request_json):
    response = requests.post(url=URL,
                             data=request_json,
                             headers={"Content-Type": "application/json"})    
    response_dict = json.loads(response.text)

    return response_dict["responses"][0]["labelAnnotations"]

def determine_trash(labelAnnotations):
    for labelAnnotation in labelAnnotations:
        description = labelAnnotation["description"]
        if "bottle" in description or "plastic" in description:
            return "bottle"
        elif "can" in description:
            return "can"
