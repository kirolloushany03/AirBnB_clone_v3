#!/usr/bin/python3
"""setup blueprint for flaskk"""
from flask import Blueprint

app_views = Blueprint("views_blue", __name__, url_prefix="/api/v1")

from api.v1.views.index import *
from api.v1.views import states
from api.v1.views import cities
