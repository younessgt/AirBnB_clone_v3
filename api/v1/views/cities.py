#!/usr/bin/python3
""" Creating a new view for City objects that handles all default
RESTFul API actions : GET, PUT, POST and DELETE"""

from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State
from flask import jsonify, abort, request


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """Retrieves a city object depending on city_id """
    city_obj = storage.get(City, city_id)
    if city_obj is not None:
        return jsonify(city_obj.to_dict())
    else:
        abort(404)


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def get_all_cities(state_id):
    """Retrieves a all cities  """
    state_obj = storage.get(State, state_id)
    if state_obj is not None:
        return jsonify([city_obj.to_dict() for city_obj in state_obj.cities])
    else:
        abort(404)


@app_views.route('/cities/<city_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """ deleting a specific city """
    city_obj = storage.get(City, city_id)
    if city_obj is not None:
        storage.delete(city_obj)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/states/<state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def create_city(state_id):
    """ creating new city """
    state_obj = storage.get(State, state_id)
    if state_obj is None:
        abort(404)
    data = request.get_json()
    """ data is a python dictionary """
    if data:
        if 'name' not in data:
            abort(400, "Missing name")
        else:
            data['state_id'] = state_id
            city = City(**data)
            storage.new(city)
            storage.save()
            return jsonify(city.to_dict()), 201
    else:
        abort(400, "Not a JSON")


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """ updating a specific city using city_id """
    city_obj = storage.get(City, city_id)
    if not city_obj:
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")
    for key, value in request.get_json().items():
        if key not in ["id", "state_id", "created_at", "updated_at"]:
            setattr(city_obj, key, value)
    storage.save()
    return jsonify(city_obj.to_dict()), 200
