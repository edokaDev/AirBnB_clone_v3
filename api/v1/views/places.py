#!/usr/bin/python3
"""place crud routes."""
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage


@app_views.route('/places', methods=['GET'])
def all_places():
    """Retrieve all places."""
    all = storage.all('Place')
    result = []
    for key, value in all.items():
        result.append(value.to_dict())
    return make_response(jsonify(result))


@app_views.route('/places/<place_id>', methods=['GET'])
def one_place(place_id):
    """Retrieve one place."""
    place = storage.get('Place', place_id)
    if place:
        return make_response(place.to_dict(), 200)
    abort(404)


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    """Delete a place."""
    place = storage.get('Place', place_id)
    if place:
        storage.delete(place)
        return make_response({}, 200)
    abort(404)


@app_views.route('/places', methods=['POST'])
def create_place():
    """Create a place."""
    try:
        payload = request.get_json()
    except Exception as e:
        return make_response({'error': 'Not a JSON'}, 400)

    if 'user_id' not in payload:
        return make_response({'error': 'Missing user_id'}, 400)
    if 'name' not in payload:
        return make_response({'error': 'Missing name'}, 400)

    user_id = payload.get('user_id')
    user = storage.get('User', user_id)
    if user is None:
        abort(404)

    if 'email' not in payload:
        return make_response({'error': 'Missing email'}, 400)

    place = place(**payload)
    place.save()
    return make_response(place.to_dict(), 201)


@app_views.route('/places/<place_id>', methods=['PUT'])
def update_place(place_id):
    """Update a Place."""
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    try:
        payload = request.get_json()
    except Exception as e:
        return make_response({'error': 'Not a JSON'}, 400)
    if payload:
        for key, value in payload.items():
            if key not in ['id',
                           'user_id',
                           'city_id',
                           'created_at',
                           'updated_at']:
                setattr(place, key, value)
        place.save()
        return make_response(place.to_dict(), 200)
    return make_response({}, 200)
