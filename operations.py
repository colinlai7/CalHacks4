import io
import os
import base64image
import json
import requests
from flask import Flask

# Imports google cloud client library
from google.cloud import vision
from google.cloud.vision import types

# Instantiate client
client = vision.ImageAnnotatorClient()

# set authentication
set GOOGLE_APPLICATION_CREDENTIALS="My First Project-156aef948acc.json"

def receive(username, image):
    # encode image as base64
    image_content = image.read()
    base64image = base64.b64encode(image_content)





def fetchimages():
