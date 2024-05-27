#!/usr/bin/python3
""" this module initializes the Flask web application"""
from flask import Flask, jsonify
from flask_cors import CORS
from models import storage
from api.v1.views import app_views
import os


app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})

app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    """this method calls storage.close() when the Flask app is done"""
    storage.close()


@app.errorhandler(404)
def error_404(error):
    """error handeling for error 404 not found page"""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = os.getenv("HBNB_API_HOST", "0.0.0.0")
    port = int(os.getenv("HBNB_API_PORT", "5000"))

    app.run(host=host, port=port, threaded=True)
