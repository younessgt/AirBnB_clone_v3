#!/usr/bin/python3
""" Creating a new view for User objects that handles all default
RESTFul API actions : GET, PUT, POST and DELETE"""

from api.v1.views import app_views
from models import storage
from models.user import User
from flask import jsonify, abort, request


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """Retrieves the list of all User objects"""
    users_in_dict = storage.all(User)

    return jsonify([data_value.to_dict()
                   for data_value in users_in_dict.values()])


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_users_with_id(user_id):
    """Retrieves a User object depending on user_id """
    user_obj = storage.get(User, user_id)
    if user_obj is not None:
        return jsonify(user_obj.to_dict())
    else:
        abort(404)


@app_views.route('/users/<user_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """ deleting a specific user """
    user_obj = storage.get(User, user_id)
    if user_obj is not None:
        storage.delete(user_obj)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """ creating new user """
    data = request.get_json()
    """ data is a python dictionary """
    if not data:
        abort(400, "Not a JSON")
    if 'email' not in data:
        abort(400, "Missing email")
    if 'password' not in data:
        abort(400, "Missing password")

    user = User(**data)
    storage.new(user)
    storage.save()
    return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """ updating a specific user using user_id """
    user_obj = storage.get(User, user_id)
    if not user_obj:
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")
    for key, value in request.get_json().items():
        if key not in ["id", "email", "created_at", "updated_at"]:
            setattr(user_obj, key, value)
    storage.save()
    return jsonify(user_obj.to_dict()), 200
