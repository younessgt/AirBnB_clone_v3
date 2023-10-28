#!/usr/bin/python3
""" Creating a new view for Review objects that handles all default
RESTFul API actions : GET, PUT, POST and DELETE"""

from api.v1.views import app_views
from models import storage
from models.place import Place
from models.review import Review
from models.user import User
from flask import jsonify, abort, request


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """Retrieves a review object depending on review_id """
    review_obj = storage.get(Review, review_id)
    if review_obj is not None:
        return jsonify(review_obj.to_dict())
    else:
        abort(404)


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET'], strict_slashes=False)
def get_all_reviews(place_id):
    """Retrieves a all reviews  """
    place_obj = storage.get(Place, place_id)
    if place_obj is not None:
        return jsonify([review.to_dict() for review in place_obj.reviews])
    else:
        abort(404)


@app_views.route('/reviews/<review_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_review(review_id):
    """ deleting a specific review """
    review_obj = storage.get(Review, review_id)
    if review_obj is not None:
        storage.delete(review_obj)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/places/<place_id>/reviews',
                 methods=['POST'], strict_slashes=False)
def create_review(place_id):
    """ creating new review """
    place_obj = storage.get(Place, place_id)
    if place_obj is None:
        abort(404)
    data = request.get_json()
    """ data is a python dictionary """
    if not data:
        abort(400, "Not a JSON")
    if 'user_id' not in data:
        abort(400, "Missing user_id")

    if 'text' not in data:
        abort(400, "Missing text")

    user_obj = storage.get(User, data['user_id'])
    if not user_obj:
        abort(404)

    data['place_id'] = place_id
    review = Review(**data)
    storage.new(review)
    storage.save()
    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """ updating a specific review using review_id """
    review_obj = storage.get(Review, review_id)
    if not review_obj:
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")
    for key, value in request.get_json().items():
        if key not in ["id", "user_id", "place_id",
                       "created_at", "updated_at"]:
            setattr(review_obj, key, value)
    storage.save()
    return jsonify(review_obj.to_dict()), 200
