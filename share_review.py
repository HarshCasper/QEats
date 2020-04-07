"""Utility to trigger facebook/pinterest share api."""
import argparse
import base64
import requests


def file_path_to_img64(image_path):
    """Returns base64 encoding of the given image."""
    file_handle = open(image_path, 'rb')
    img = file_handle.read()
    file_handle.close()
    img_b64 = base64.b64encode(img)
    return img_b64


def share_review(msg, file_name):
    """Shares the given image and the message to facebook/pinterest share."""
    data = {
        'imgBase64': file_path_to_img64(file_name),
        'text': msg,
        'tags': '',
        'orderId': '',
        'share': ['Facebook']
    }
    try:
        resp = requests.post(
            data=data, url='http://localhost:8081/qeats/v1/review/share')
        print("Response Status Code: " + str(resp.status_code))
    except requests.exceptions.ConnectionError:
        print(
            '\n\nError: Could not post review. Make sure you have started the server!!!\n\n')


# Execute the file using the command below
# Sample command: python3 share_review.py --image tests/ice-cream.jpg --message 'Awesome ice-cream!'
if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='send a request to the QEats backend server')
    parser.add_argument('--image', help='image to be uploaded', required=True)
    parser.add_argument(
        '--message', help='message to be sent in the post', required=True)
    args = parser.parse_args()

    share_review(args.message, args.image)
