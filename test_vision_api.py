import io
from google.cloud import vision

#########################################################
############### GOOGLE vision API test ##################
#########################################################

####### Before running the program export GOOGLE_APPLICATION_CREDENTIALS=OptiLife-ab42aeb1f0a3.json

# vision_client = vision.Client()
# file_name = 'img/Spaghetti.jpg'
#
# with io.open(file_name, 'rb') as image_file:
#     content = image_file.read()
#     image = vision_client.image(content=content)
#
# labels = image.detect_labels()


# for _label in labels:
#     print(_label.description + ' with score {}'.format(_label.score))


#########################################################
################# Openfood API test #####################
#########################################################
# import requests
#
# BASE_URL='https://www.openfood.ch/api/v3'
# KEY='6c831337bc08524347f570b7644d9a06'
# ENDPOINT='/products'
#
# url = BASE_URL + ENDPOINT
#
# query = {
#   "query": {
#     "wildcard": {
#       "_all_names" : "*toblerone*"
#     }
#   }
# }
#
# headers = {
#   'Authorization': 'Token token=' + KEY,
#   'Accept': 'application/json',
#   'Content-Type': 'application/vnd.api+json',
#   'Accept-Encoding': 'gzip,deflate'
# }
#
# r = requests.post(url, json=query, headers=headers)
# print('Status: ' + str(r.status_code))
# if r.status_code == 200:
#     results = r.json()
#     print('Number of products found: ' + str(results['hits']['total']))
#     print('First few products...')
#     for hit in results['hits']['hits']:
#         print('  ' + hit['_source']['display_name_translations']['en'])


# NOT WORKING

#########################################################
################# Nutritionix API test ##################
#########################################################
from nutritionix import Nutritionix
import pprint

nix = Nutritionix(app_id="8dfdbdb1", api_key="66ad2fcd0f25722ca73662505e9fd492")

kebab = nix.search("kebab", results="0:1")

# We are able to get the item_id which will allow us to access to the item Nutritional values
results = kebab.json()
# print(results.keys())
hits = results['hits'][0]
pprint.pprint(hits.keys())
item_id = hits['fields']['item_id']
# print(item_id)
# print(results.hits.fields.item_id)

# pprint.pprint(results)

# pprint.pprint(nix.item(id="5626b8fd477f7be969a06338").json())

item_full_file = nix.item(id=item_id).json()

# pprint.pprint(item_full_file)

weight_key = 'nf_serving_weight_grams'
calories_key = 'nf_calories'

weight = item_full_file[weight_key]
calories = item_full_file[calories_key]

ratio = calories / weight
print('{} / {} = {} '.format(calories, weight, ratio))
