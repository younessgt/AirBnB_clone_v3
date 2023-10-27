#!/usr/bin/python3
""" module for status route """

from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', methods=['GET'])
def status():
    """ returning a json with status : ok """
    return jsonify({"status": "OK"})
