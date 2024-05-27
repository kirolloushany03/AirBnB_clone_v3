#!/usr/bin/python3
""" this module sets to flask web application"""
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
import os


app = Flask(__name__)
app.url_map.strict_slashes = False
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    """this method call storage.close()"""
    storage.close()


@app.errorhandler(404)
def error_404(error):
    """error handeling for error 404 not found page"""
    response = jsonify({"error": "Not found"})
    response.status_code = 404
    return response


if __name__ == "__main__":
    host = os.getenv("HBNB_API_HOST", "0.0.0.0")
    port = int(os.getenv("HBNB_API_PORT", "5000"))
    app.url_map.strict_slashes = False

    app.run(host=host, port=port, threaded=True)
