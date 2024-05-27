#!/usr/bin/python3
"""Creating a new view for Review objects"""
from api.v1.views import app_views
from models import storage
from models.review import Review
from models.place import Place
from models.user import User
from flask import jsonify, abort, request


@app_views.get("/places/<place_id>/reviews")
def all_reviews(place_id):
    """Retrieve the list of all Review objects of a Place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify([review.to_dict() for review in place.reviews])


@app_views.get("/reviews/<review_id>")
def get_review(review_id):
    """Retrieve a Review object"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.delete("/reviews/<review_id>")
def delete_review(review_id):
    """Delete a Review object"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.post("/places/<place_id>/reviews")
def create_review(place_id):
    """Create a Review"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    review_data = request.get_json(silent=True)
    if review_data is None:
        return jsonify({"error": "Not a JSON"}), 400
    if "user_id" not in review_data:
        return jsonify({"error": "Missing user_id"}), 400
    user = storage.get(User, review_data["user_id"])
    if not user:
        abort(404)
    if "text" not in review_data:
        return jsonify({"error": "Missing text"}), 400
    review_data["place_id"] = place_id
    new_review = Review(**review_data)
    new_review.save()
    return jsonify(new_review.to_dict()), 201


@app_views.put("/reviews/<review_id>")
def update_review(review_id):
    """Update a Review object"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    review_data = request.get_json(silent=True)
    if review_data is None:
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in review_data.items():
        if key not in ["id", "user_id", "place_id", "created_at",
                                                    "updated_at"]:
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict()), 200
