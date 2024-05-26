#!/usr/bin/python3
"""setup routes for the blueprint"""
from flask import jsonify
from api.v1.views import app_views


@app_views.route("/status")
def status():
    """an this return json data to check the status"""
    return jsonify({"status": "OK"})
