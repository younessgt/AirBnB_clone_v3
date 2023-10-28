#!/usr/bin/python3
""" Creating a new view for City objects that handles all default
RESTFul API actions : GET, PUT, POST and DELETE"""

from api.v1.views import app_views
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from flask import jsonify, abort, request


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """Retrieves a place object depending on place_id """
    place_obj = storage.get(Place, place_id)
    if place_obj is not None:
        return jsonify(place_obj.to_dict())
    else:
        abort(404)


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def get_all_places(city_id):
    """Retrieves a all places  """
    city_obj = storage.get(City, city_id)
    if city_obj is not None:
        return jsonify([place.to_dict() for place in city_obj.places])
    else:
        abort(404)


@app_views.route('/places/<place_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """ deleting a specific place """
    place_obj = storage.get(Place, place_id)
    if place_obj is not None:
        storage.delete(place_obj)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'], strict_slashes=False)
def create_place(city_id):
    """ creating new place """
    city_obj = storage.get(City, city_id)
    if city_obj is None:
        abort(404)
    data = request.get_json()
    """ data is a python dictionary """
    if not data:
        abort(400, "Not a JSON")
    if 'user_id' not in data:
        abort(400, "Missing user_id")

    if 'name' not in data:
        abort(400, "Missing name")

    user_obj = storage.get(User, data['user_id'])
    if not user_obj:
        abort(404)

    data['city_id'] = city_id
    place = Place(**data)
    storage.new(place)
    storage.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """ updating a specific place using city_id """
    place_obj = storage.get(Place, place_id)
    if not place_obj:
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")
    for key, value in request.get_json().items():
        if key not in ["id", "user_id", "city_id", "created_at", "updated_at"]:
            setattr(place_obj, key, value)
    storage.save()
    return jsonify(place_obj.to_dict()), 200
