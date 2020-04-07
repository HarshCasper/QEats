import base64
import json
import requests
import os

class Pinterest:
    @staticmethod
    def get_access_token(token_name):
        access_token=os.getenv('PWD')+'/access_tokens.sh'
        f = open(access_token,'r+')
        lines = f.readlines()
        for line in lines:
            tokens = line.strip().split('=')
            if tokens[0] == token_name:
                return tokens[1].strip()

        return 'Not found'

    def __init__(self):
        self.board_id = Pinterest.get_access_token('PINTEREST_BOARD_ID')
        self.access_token = Pinterest.get_access_token('PINTEREST_ACCESS_TOKEN')
#TODO: CRIO_TASK_MODULE_PINTEREST_SHARE
# As part of this module you are expected to complete the publish_photo_msg function
# Tasks:
# 1) You need to register as pinterest developer to obtain app_id & app_secret
# 2) Obtain an access token using Postman method and store it in access_tokens.sh
# 3) Obtain Pinterest board ID by creating a Pinterest Board using the Pinterest Create Board API
#    (https://developers.pinterest.com/docs/api/boards/) and store it in access_tokens.sh
# 4) Enter board_id & access_token in access_tokens.sh - IMPORTANT step
#    PINTEREST_BOARD_ID=board_id
#    PINTEREST_ACCESS_TOKEN=access_token
# 5) Complete the publish_photo_msg() function. This function should publish a pin with
#    the given message and photo. The post should be published to the board you have created
#    in the earlier step
# 6) Manually verify the pin created and submit the code
#
# NOTE: The Pinterest API has a rate limit of 10 requests/hour. If you exceed
#       this limit, you can either wait until the rate counter resets or create
#       a new board and use it to test your implementation.

# Args:
#   1) message   -> string message to be posted
#   2) image_url -> publicly accessible url of the image to be posted

# write your code below
    def publish_photo_msg(self, message, image_url):
        apiurl = 'https://api.pinterest.com/v1/pins/'
        data = {
            'board' : self.board_id,
            'image_url' : image_url,
            'access_token' : self.access_token,
            'note' : message
        }
        res=requests.post(url=apiurl,data=data)
        print(res.status_code)
        return None

if __name__ == '__main__':

    pinterest = Pinterest()
   
    message = "bharath liked this chocolate and vanilla icecream"
    image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e7/Stracciatella_gelato.jpg/800px-Stracciatella_gelato.jpg"

    pinterest.publish_photo_msg(message, image_url)
