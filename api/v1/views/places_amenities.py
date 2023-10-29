#!/usr/bin/python3
""" Creating a new view for for the link between Place and Amenity objects
that handles all default
RESTFul API actions : GET, POST and DELETE"""

from api.v1.views import app_views
from models import storage
from models.place import Place
from models.amenity import Amenity
from flask import jsonify, abort


@app_views.route('/places/<place_id>/amenities',
                 methods=['GET'], strict_slashes=False)
def get_all_amenities(place_id):
    """Retrieves a all amenities of a place  """
    place_obj = storage.get(Place, place_id)
    if place_obj is not None:
        return jsonify([amenity.to_dict() for amenity in place_obj.amenities])
    else:
        abort(404)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_link_amenity(place_id, amenity_id):
    """ deleting a specific amenity """
    place_obj = storage.get(Place, place_id)
    if place_obj is None:
        abort(404)
    amenity_obj = storage.get(Amenity, amenity_id)
    if amenity_obj is None:
        abort(404)
    if amenity_obj not in place_obj.amenities:
        abort(404)
    storage.delete(amenity_obj)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['POST'], strict_slashes=False)
def link_amenity_toplace(place_id, amenity_id):
    """ linking  amenity to a place """
    place_obj = storage.get(Place, place_id)
    if place_obj is None:
        abort(404)

    amenity_obj = storage.get(Amenity, amenity_id)
    if amenity_obj is None:
        abort(404)

    if amenity_obj in place_obj.amenities:
        return jsonify(amenity_obj.to_dict()), 200

    place_obj.amenities.append(amenity_obj)
    storage.save()
    return jsonify(amenity_obj.to_dict()), 201
