#!/usr/bin/python3
""" Creating a new view for State objects that handles all default
RESTFul API actions : GET, PUT, POST and DELETE"""

from api.v1.views import app_views
from models import storage
from models.state import State
from flask import jsonify, abort, request


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """Retrieves the list of all State objects"""
    states_in_dict = storage.all(State)

    return jsonify([data_value.to_dict()
                   for data_value in states_in_dict.values()])


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_states_with_id(state_id):
    """Retrieves a State object depending on state_id """
    state_obj = storage.get(State, state_id)
    if state_obj is not None:
        data_dict = state_obj.to_dict()
        return jsonify(data_dict)
    else:
        abort(404)


@app_views.route('/states/<state_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """ deleting a specific state """
    state_obj = storage.get(State, state_id)
    if state_obj is not None:
        storage.delete(state_obj)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """ creating new state """
    data = request.get_json()
    """ data is a python dictionary """
    if data:
        if 'name' not in data:
            abort(404, "Missing name")
        else:
            state = State(**data)
            storage.new(state)
            storage.save()
            return jsonify(state.to_dict()), 201
    else:
        abort(404, "Not a JSON")


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """ updating a specific state using state_id """
    state_obj = storage.get(State, state_id)
    if not state_obj:
        abort(404)
    if not request.get_json():
        abort(404, "Not a JSON")
    for key, value in request.get_json():
        if key not in ["id", "state_id", "created_at", "updated_at"]:
            setattr(state_obj, key, value)
    storage.save()
    return jsonify(state_obj.to_dict()), 200
