import io
from google.cloud import vision
from nutritionix import Nutritionix

def get_labels_from_image(file_name):
    """
    This function will allow the user to get the labels from an image_file.
    input: file_name of the image
    output: list of labels (.description or .score of individual label)
    """

    vision_client = vision.Client()

    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()
        image = vision_client.image(content=content)

    labels = image.detect_labels()

    return labels

def nutritionix_wrapper(label):
    """
    This function will take a label and give out the weight to calories ratio
    input: label (string)
    output: weight / calories (double)
    """
    nix = Nutritionix(app_id="8dfdbdb1", api_key="66ad2fcd0f25722ca73662505e9fd492")

    nutritionix_id = nix.search(label, results="0:1").json()['hits'][0]['fields']['item_id']

    nutritionix_info = nix.item(id=nutritionix_id).json()

    weight_key = 'nf_serving_weight_grams'
    calories_key = 'nf_calories'

    weight = nutritionix_info[weight_key]
    calories = nutritionix_info[calories_key]

    if weight is not None and calories is not None:
        print('ME GOOD')
        ratio = calories / weight
        return ratio

    print('ME BAD')
    return 0

def nutritionix_calories(nutritionix_id):
    """
    This function will take an ID and return calories | Useful for the total count of calories per user
    input: id (string)
    output: calories (double)
    """
    calories_key = 'nf_calories'
    nutritionix_info = nix.item(id=nutritionix_id).json()
    calories = nutritionix_info[calories_key]
    if calories is not None:
        return calories
    else:
        return None



if __name__ == '__main__':

    file_name = 'img/Spaghetti.jpg'
    labels = get_labels_from_image(file_name)

    nutritionix_wrapper(labels[0].description)
