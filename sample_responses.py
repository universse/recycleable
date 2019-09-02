import json
from base64 import b64encode

from helpers import send_request, determine_trash

with open('./sample_images/bottle.png', 'rb') as image:
  image_json = {
      'content': b64encode(image.read()).decode('UTF-8')
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

request_json = json.dumps(request)
responses = send_request(request_json)
trash = determine_trash(responses)
print(responses)
print(trash)

# bottle.png
# [
#     {
#         'mid': '/m/038hg',
#         'description': 'green',
#         'score': 0.9650598,
#         'topicality': 0.9650598
#     },
#     {
#         'mid': '/m/02n3pb',
#         'description': 'product',
#         'score': 0.86215013,
#         'topicality': 0.86215013
#     },
#     {
#         'mid': '/m/01jwgf',
#         'description': 'product',
#         'score': 0.80363667,
#         'topicality': 0.80363667
#     },
#     {
#         'mid': '/m/04dr76w',
#         'description': 'bottle',
#         'score': 0.7108251,
#         'topicality': 0.7108251
#     },
#     {
#         'mid': '/m/03y18t',
#         'description': 'product design',
#         'score': 0.6457513,
#         'topicality': 0.6457513
#     },
#     {
#         'mid': '/m/05z87',
#         'description': 'plastic',
#         'score': 0.5758755,
#         'topicality': 0.5758755
#     }
# ]

# can.png
# [
#     {
#         'mid': '/m/02jnhm',
#         'description': 'tin can',
#         'score': 0.7008034,
#         'topicality': 0.7008034
#     },
#     {
#         'mid': '/m/01jwgf',
#         'description': 'product',
#         'score': 0.6340035,
#         'topicality': 0.6340035
#     },
#     {
#         'mid': '/m/0271t',
#         'description': 'drink',
#         'score': 0.61301833,
#         'topicality': 0.61301833
#     },
#     {
#         'mid': '/m/03y18t',
#         'description': 'product design',
#         'score': 0.6045963,
#         'topicality': 0.6045963
#     },
#     {
#         'mid': '/m/0gjbv4m',
#         'description': 'aluminum can',
#         'score': 0.5664499,
#         'topicality': 0.5664499
#     },
#     {
#         'mid': '/m/03h_4m',
#         'description': 'cylinder',
#         'score': 0.5478548,
#         'topicality': 0.5478548
#     }
# ]
