#!/usr/bin/python3
"""General API routes."""
from api.v1.views import app_views
from models import storage


@app_views.route('/status', strict_slashes=False)
def status():
    """Status of the api."""
    return {"status": "OK"}


@app_views.route('/stats', strict_slashes=False)
def stats():
    """Get the counts of objects in the storage."""
    data = {
        "amenities": storage.count('Amenity'),
        "cities": storage.count('City'),
        "places": storage.count('Place'),
        "reviews": storage.count('Review'),
        "states": storage.count('State'),
        "users": storage.count('User'),
    }
    return data
