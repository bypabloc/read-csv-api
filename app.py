import locale
from flask import Flask, request
from flask import json
from flask import request
from flask_cors import CORS

import logging

locale.setlocale(locale.LC_TIME, locale.getlocale())

app = Flask(__name__)
CORS(
    app=app,
    resources={r"/api/*": {"origins": "*"}},
    origins=['*'],
    methods=['GET', 'POST'],
    allow_headers=['*'],
    expose_headers=['*'],
    supports_credentials=True,
)

logging.basicConfig()

import routes
