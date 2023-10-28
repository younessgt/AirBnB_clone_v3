#!/usr/bin/python3
""" create a flask app """
from flask import Flask
from flask_cors import CORS
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def close_session(exception):
    """ method to remove the current SQLAlchemy session """
    storage.close()


@app.errorhandler(404)
def error_handler(e):
    return {"error": "Not found"}, 404


app.register_blueprint(app_views)

if __name__ == "__main__":
    host = getenv("HBNB_API_HOST", "0.0.0.0")
    port = getenv("HBNB_API_PORT", 5000)
    app.run(host=host, port=port, threaded=True)
