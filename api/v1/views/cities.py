#!/usr/bin/python3
"""City crud routes."""
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET'])
def all_cities(state_id):
    """Retrieve all cities."""
    state = storage.get('State', state_id)
    if state is None:
        abort(404)
    cities = state.cities
    result = []
    for city in cities:
        result.append(city.to_dict())
    return make_response(jsonify(result))


@app_views.route('/cities/<city_id>', methods=['GET'])
def one_city(city_id):
    """Retrieve one state."""
    city = storage.get('City', city_id)
    if city is None:
        abort(404)
    return make_response(city.to_dict(), 200)


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    """Delete a city."""
    city = storage.get('City', city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    return make_response({}, 200)


@app_views.route('/states/<state_id>/cities', methods=['POST'])
def create_city(state_id):
    """Create a city."""
    try:
        payload = request.get_json()
    except Exception as e:
        return make_response({'error': 'Not a JSON'}, 400)

    if payload and 'name' not in payload:
        return make_response({'error': 'Missing name'}, 400)

    name = payload.get('name')
    state = storage.get('State', state_id)
    if state is None:
        abort(404)

    city = City(name=name, state_id=state_id)
    city.save()
    return make_response(city.to_dict(), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'])
def update_city(city_id):
    """Update a City."""
    city = storage.get('City', city_id)
    if city is None:
        abort(404)
    try:
        payload = request.get_json()
    except Exception as e:
        return make_response({'error': 'Not a JSON'}, 400)
    if payload:
        for key, value in payload.items():
            if key not in ['id', 'created_at', 'updated_at', 'state_id']:
                setattr(city, key, value)
        city.save()
        return make_response(city.to_dict(), 200)
    return make_response({}, 200)
