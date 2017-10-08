import io
import os
import base64
import json
# import cv2
# import requests
import sys
import argparse

from flask import Flask

# Imports google cloud client library
from google.cloud import vision
from google.cloud.vision import types


# Instantiate client
client = vision.ImageAnnotatorClient()

# set authentication
# GOOGLE_APPLICATION_CREDENTIALS = "My First Project-156aef948acc.json"

# def implicit():
#     from google.cloud import storage
#     storage_client = storage.Client()
#     buckets = list(storage_cleint.list_buckets())
#     print(buckets)

def explicit():
    from google.cloud import storage
    storage_client = storage.Client.from_service_account_json('My First Project-156aef948acc.json')
    buckets = list(storage_client.list_buckets())
    print(buckets)

def receive(username, image):
    # encode image as base64
    image_content = image.read()
    base64image = base64.b64encode(image_content)

    image = client.image(image_content = image_content)
    labels = image.detect_labels()
    for label in labels:
        print(label.description, label.score)

# def fetchimages():

def main(input_file):
    # explicit()
    # testfile = cv2.imread('demo-image.jpg')
    receive("test", input_file)

if __name__ == "__main__":
    # inFile = Image.open(sys.argv[1])
    main()
