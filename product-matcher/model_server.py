import torch
import numpy as np
from flask import Flask, request
from flask_cors import cross_origin
import json
import flask
import threading
import time
import requests
import traceback
import logging

# Create the Flask app
application = Flask(__name__)

@application.route('/price-assist/api/product_matcher')
def matcher():
    pass

# Run app using localhost
if __name__ == '__main__':
    application.run(host='0.0.0.0', port=5004, threaded=True, debug=False)
