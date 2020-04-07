import os
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status

import restaurants.image_uploader
import restaurants.facebook_post
import restaurants.pinterest_post
import restaurants.clarifai_tag_suggestions

# Create your views here.
def get_access_token(token_name):
        access_token = os.getenv('PWD') + '/access_tokens.sh'
        f = open(access_token, 'r+')
        lines = f.readlines()
        for line in lines:
            tokens = line.strip().split('=')
            if tokens[0] == token_name:
                return tokens[1].strip()

        return 'Not found'

class GetRestaurants(ListAPIView):
    #serializer_class = RestaurantSerializer
    def list(self, request, *args, **kwargs):
        restaurants = {
            "restaurants": [
                {
                    "restaurantId": "10",
                    "name": "A2B",
                    "city": "Btm Layout",
                    "imageUrl": "www.google.com",
                    "latitude": 20.027,
                    "longitude": 30.0,
                    "opensAt": "18:00",
                    "closesAt": "23:00",
                    "attributes": [
                            "Tamil",
                            "South Indian"
                    ]
                },
                {
                    "restaurantId": "11",
                    "name": "A2B",
                    "city": "Hsr Layout",
                    "imageUrl": "www.google.com",
                    "latitude": 20.027,
                    "longitude": 30.0,
                    "opensAt": "18:00",
                    "closesAt": "23:00",
                    "attributes": [
                            "Tamil",
                            "South Indian"
                    ]
                }
            ]
        }

        return Response(restaurants)


class MenuApiView(ListAPIView):
    def list(self, request, *args, **kwargs):
        menu_response = {
            "menu": {
                "items": [
                        {
                            "attributes": [
                                "South Indian"
                            ],
                            "id": "1",
                            "imageUrl": "www.google.com",
                            "itemId": "10",
                            "name": "Idly",
                            "price": 45
                        },
                    {
                            "attributes": [
                                "South Indian"
                            ],
                            "id": "2",
                            "imageUrl": "www.google.com",
                            "itemId": "10",
                            "name": "Vadai",
                            "price": 30
                            },
                    {
                            "attributes": [
                                "South Indian"
                            ],
                            "id": "1",
                            "imageUrl": "www.google.com",
                            "itemId": "10",
                            "name": "Masala Dosai",
                            "price": 90
                            }
                ],
                "restaurantId": "11"
            }
        }

        return Response(menu_response)


class OrderListView(ListAPIView):
    def list(self, request, *args, **kwargs):
        order_lists = [
            {
                "id": "1",
                "items": [
                    {
                        "attributes": [
                            "South Indian"
                        ],
                        "id": "1",
                        "imageUrl": "www.google.com",
                        "itemId": "10",
                        "name": "Idly",
                        "price": 45
                    }
                ],
                "restaurantId": "11",
                "timePlaced": "",
                "total": 45,
                "userId": "string"
            },
            {
                "id": "10",
                "items": [
                    {
                        "attributes": [
                            "South Indian"
                        ],
                        "id": "1",
                        "imageUrl": "www.google.com",
                        "itemId": "10",
                        "name": "Idly",
                        "price": 45
                    }
                ],
                "restaurantId": "11",
                "timePlaced": "",
                "total": 45,
                "userId": "string"
            },
            {
                "id": "102",
                "items": [
                    {
                        "attributes": [
                            "South Indian"
                        ],
                        "id": "1",
                        "imageUrl": "www.google.com",
                        "itemId": "10",
                        "name": "Idly",
                        "price": 45
                    }
                ],
                "restaurantId": "11",
                "timePlaced": "",
                "total": 45,
                "userId": "string"
            }
        ]
        return JsonResponse(order_lists, safe=False)


class GetSocial(ListAPIView):
    #serializer_class = RestaurantSerializer
    def list(self, request, *args, **kwargs):
        tags = ['Facebook', 'Pinterest']
        return JsonResponse(tags, safe=False)


class GetCart(ListAPIView):
    #serializer_class = RestaurantSerializer
    def list(self, request, *args, **kwargs):
        cart = {}
        return Response(cart)


# @POST
# ENDPOINT 'qeats/v1/tags'
# request body = {
#        'img_base64' : '<BASE 64 IMAGE CONTENT>',
# }

#response = ['tag1', 'tag2']
class GetTags(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        tags = []
        body = request.data
        assert set(['imgBase64']) == set(sorted(list(body.keys())))
        img_b64 = body['imgBase64']
        image_url = restaurants.image_uploader.upload(img_b64)

        # TODO: CRIO_TASK_MODULE_TAG_SUGGESTION
        # Add call to clarifai api here.
        # Refer todo in qeats/restaurants/clarifai_tag_suggestions.py for instructions
        tags = restaurants.clarifai_tag_suggestions.get_tags_suggestions('f8768c06f0a64dfca8a4d62e81b802ad',image_url)
        return JsonResponse(tags, safe=False)

# @POST
# ENDPOINT 'qeats/v1/reviews/share'
# {
#     'imgBase64' : '',
#     'text' : 'Great Food!',
#     'orderId' : '0x12312',
#     'tags' : ['Briyani'],
#     'share' : ['Facebook', 'Pinterest']
# }
class ShareReview(ListAPIView):
    def post(self, request, *args, **kwargs):
        body = request.data
        assert set(['imgBase64', 'orderId', 'share', 'tags', 'text']
                   ) == set(sorted(list(body.keys())))
        message = body['text'] + ' ' + \
            ''.join(['#' + tag + ' ' for tag in body['tags']])
        image_base64 = body['imgBase64']
        image_url = restaurants.image_uploader.upload(image_base64)

        if 'Facebook' in body['share']:
            facebook = restaurants.facebook_post.Facebook()
            facebook.publish_photo_msg(message, image_url)

        #TODO: CRIO_TASK_MODULE_PINTEREST_SHARE
        # add support to share a review to a Pinterest board
        # check if you get Pinterest in body['share']
        if 'Pinterest' in body['share']:
            pinterest = restaurants.pinterest_post.Pinterest()
            pinterest.publish_photo_msg(message, image_url)

        response_data = {
            "reviewId": body['orderId'],
            "responseType": 1
        }

        return Response(response_data)
