#!/usr/bin/python3
""" Creating a new view for Amenity objects that handles all default
RESTFul API actions : GET, PUT, POST and DELETE"""

from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from flask import jsonify, abort, request


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """Retrieves the list of all Amenity objects"""
    amenities_in_dict = storage.all(Amenity)

    return jsonify([data_value.to_dict()
                   for data_value in amenities_in_dict.values()])


@app_views.route('/amenities/<amenity_id>',
                 methods=['GET'], strict_slashes=False)
def get_amenities_with_id(amenity_id):
    """Retrieves a Amenity object depending on amenity_id """
    amenity_obj = storage.get(Amenity, amenity_id)
    if amenity_obj is not None:
        return jsonify(amenity_obj.to_dict())
    else:
        abort(404)


@app_views.route('/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_amenity(amenity_id):
    """ deleting a specific amenity """
    amenity_obj = storage.get(Amenity, amenity_id)
    if amenity_obj is not None:
        storage.delete(amenity_obj)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """ creating new amenity """
    data = request.get_json()
    """ data is a python dictionary """
    if data:
        if 'name' not in data:
            abort(400, "Missing name")
        else:
            amenity = Amenity(**data)
            storage.new(amenity)
            storage.save()
            return jsonify(amenity.to_dict()), 201
    else:
        abort(400, "Not a JSON")


@app_views.route('/amenities/<amenity_id>',
                 methods=['PUT'], strict_slashes=False)
def update_amenity(amenity_id):
    """ updating a specific amenity using amenity_id """
    amenity_obj = storage.get(Amenity, amenity_id)
    if not amenity_obj:
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")
    for key, value in request.get_json().items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(amenity_obj, key, value)
    storage.save()
    return jsonify(amenity_obj.to_dict()), 200
