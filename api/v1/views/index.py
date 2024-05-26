#!/usr/bin/python3
"""setup routes for the blueprint"""
from flask import jsonify
from api.v1.views import app_views


@app_views.route("/status")
def status():
    """an this return json data to check the status"""
    return jsonify({"status": "OK"})


@app_views.route("/stats")
def stats():
    """return the count of all classes"""
    from models import storage
    from models.state import State
    from models.city import City
    from models.user import User
    from models.place import Place
    from models.review import Review
    from models.amenity import Amenity

    classes = {"amenities": Amenity,
               "cities": City,
               "places": Place,
               "reviews": Review,
               "states": State,
               "users": User}
    return jsonify({
        key: storage.count(value) for key, value in classes.items()
    })
