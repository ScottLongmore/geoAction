# coding: utf-8
""" Filename:  __init__.py """

from flask import Flask

# Create Flask App
app = Flask(__name__)

# Import configuration
app.config.from_object('config')

# Import polyAction module
import geoAction.polygonAction
