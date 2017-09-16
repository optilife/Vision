import io
from google.cloud import vision

#########################################################
############### GOOGLE vision API test ##################
#########################################################

####### Before running the program export GOOGLE_APPLICATION_CREDENTIALS=OptiLife-ab42aeb1f0a3.json

vision_client = vision.Client()
file_name = 'img/Spaghetti.jpg'

with io.open(file_name, 'rb') as image_file:
    content = image_file.read()
    image = vision_client.image(content=content)

labels = image.detect_labels()


# for _label in labels:
#     print(_label.description + ' with score {}'.format(_label.score))


#########################################################
################# Openfood API test #####################
#########################################################
import requests

BASE_URL='https://www.openfood.ch/api/v3'
KEY='6c831337bc08524347f570b7644d9a06'
ENDPOINT='/products'

url = BASE_URL + ENDPOINT

query = {
  "query": {
    "wildcard": {
      "_all_names" : "*{}*".format(labels[0].description)
    }
  }
}

headers = {
  'Authorization': "Token token=" + KEY,
  'Accept': 'application/json',
  'Content-Type': 'application/vnd.api+json',
  'Accept-Encoding': 'gzip,deflate'
}

r = requests.post(url, json=query, headers=headers)
print('Status: ' + str(r.status_code))
if r.status_code == 200:
    results = r.json()
    print('Number of products found: ' + str(results['hits']['total']))
    print('First few products...')
    for hit in results['hits']['hits']:
        print('  ' + hit['_source']['display_name_translations']['en'])
