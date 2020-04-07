from django.test import Client
from django.urls import resolve
import json
import pytest
import cv2
import os
import requests



import restaurants.facebook_post
class FacebookTestUtil:
    def __init__(self):
        pass

    def get_user_feed(self):
        page_id = get_access_token('FACEBOOK_PAGE_ID')
        page_access_token = get_access_token('FACEBOOK_PAGE_ACCESS_TOKEN')
        url = 'https://graph.facebook.com/{}/feed?access_token={}&fields=id,message,attachments'.format(page_id, page_access_token)
        print('Get user feed url = ', url)
        response = requests.get(url)
        data = response.json()
        return data

    def check_whether_message_is_published(self, message, image_path):
        user_feeds = self.get_user_feed()
        for feed in user_feeds['data']:
            if 'attachments' in feed:
                if feed['message'] == message:
                    return True
                    print(json.dumps(feed, indent=4))
                    url = feed['attachments']['data'][0]['media']['image']['src']
                    download_file('sneakpeak.jpg', url)
                    result = binary_image_compare('sneakpeak.jpg', image_path)
                    print('[Result = {}\n'.format(result))
                    return result
        return False

