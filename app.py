import locale
from flask import Flask
from flask import json
from flask import request
import logging

locale.setlocale(locale.LC_TIME, locale.getlocale())

app = Flask(__name__)

logging.basicConfig()

import routes
