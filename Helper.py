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


    nutritionix_id = nutritionix_ID(label)

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

def nutritionix_ID(label):
    """
    This function will give the first product ID for a specific label
    input: label (string)
    output: ID (string)
    """
    nix = Nutritionix(app_id="8dfdbdb1", api_key="66ad2fcd0f25722ca73662505e9fd492")

    return nix.search(label, results="0:1").json()['hits'][0]['fields']['item_id']

def nutritionix_calories(nutritionix_id):
    """
    This function will take an ID and return calories | Useful for the total count of calories per user
    input: id (string)
    output: calories
    """
    nix = Nutritionix(app_id="8dfdbdb1", api_key="66ad2fcd0f25722ca73662505e9fd492")

    calories_key = 'nf_calories'

    nutritionix_info = nix.item(id=nutritionix_id).json()
    calories = nutritionix_info[calories_key]
    if calories is not None:
        return calories
    else:
        return None

def health_score(**options):
    """
    This function will return a health score based on multiple informations concerning the user
    input: weigth, height, age, gender, total_calories_day (in DB)
    output: health_score
    """
    BMI = options['weight'] / options['height']
    if BMI < 18.5:
        BMI_weight = 1
    elif BMI >= 18.5 and BMI < 25:
        BMI_weight = 0
    elif BMI >= 25 and BMI < 30:
        BMI_weight = 1
    elif BMI >= 30 and BMI < 40:
        BMI_weight = 2
    else:
        BMI_weight = 3

    if options['total_calories_day']:
        calories = options['total_calories_day']
        if options['gender'] == 'male':
            BMR=66.47+ (13.75 x options['weight']) + (5.0 x options['height']) - (6.75 x options['age'])
        elif options['gender'] == 'female':
            BMR=65.09 + (9.56 x options['weight']) + (1.84 x options['height']) - (4.67 x options['age'])
        ratio = BMR / calories
        if ratio > 1:
            return 80 - BMI_weight * 20 + 20 * (BMR / total_calories_day)
        else:
            return 60 - BMI_weight * 20 + 40 * (BMR / total_calories_day)
    return 100 - BMI_weight * 20


if __name__ == '__main__':

    file_name = 'img/Spaghetti.jpg'
    labels = get_labels_from_image(file_name)

    nutritionix_wrapper(labels[0].description)
