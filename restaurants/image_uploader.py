import base64
import os
import requests


#  curl --location --request POST "https://api.imgur.com/3/image" \
#   --header "Authorization: Client-ID {{clientId}}" \
#   --form "image=R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7"


def upload(img_b64):

    list_of_app_ids = ['f7bce5ff873c8f8']

    for app_id in list_of_app_ids:

        request_body = {
            'image': img_b64,
            'name': 'numbers.jpg',
            'type': 'base64',
            'title': 'Biryani',
            'description': 'Awesome Briyani 5 Stars -- Fun!!!'
        }

        url = "https://api.imgur.com/3/upload"
        headers = {
            'Authorization': 'Client-ID ' + app_id
        }

        response = requests.post(url, data=request_body, headers=headers)
        resp = response.json()

        image_url = 'https://i.imgur.com/kE2T5uv.jpg'

        if response.status_code == 200:
            image_url = resp['data']['link']

        # return image url if even if the response is not 200
        if 'data' in resp and 'link' in resp['data'] and resp['data']['link'] != None:
            return resp['data']['link']

        # default return Briyani
        return image_url

def file_path_to_img64(image_path):
    file_handle = open(image_path, 'rb')
    img = file_handle.read()
    file_handle.close()
    img_b64 = base64.b64encode(img)
    return img_b64

if __name__ == '__main__':
    image_path = os.getenv('PWD') + '/tests/ice-cream.jpg'
    image_url = upload(file_path_to_img64(image_path))
    #print(image_url)
