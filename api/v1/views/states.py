#!/usr/bin/python3
"""State crud routes."""
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'])
def all_states():
    """Retrieve all states."""
    all = storage.all('State')
    result = []
    for key, value in all.items():
        result.append(value.to_dict())
    return make_response(jsonify(result))


@app_views.route('/states/<state_id>', methods=['GET'])
def one_state(state_id):
    """Retrieve one state."""
    state = storage.get('State', state_id)
    if state:
        return make_response(state.to_dict(), 200)
    abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """Delete a state."""
    state = storage.get('State', state_id)
    if state:
        storage.delete(state)
        return make_response({}, 200)
    abort(404)


@app_views.route('/states', methods=['POST'])
def create_state():
    """Create a state."""
    try:
        payload = request.get_json()
    except Exception as e:
        return make_response({'error': 'Not a JSON'}, 400)

    if payload and 'name' not in payload:
        return make_response({'error': 'Missing name'}, 400)

    name = payload.get('name')
    state = State(name=name)
    state.save()
    return make_response(state.to_dict(), 201)


@app_views.route('/states/<state_id>', methods=['PUT'])
def update_state(state_id):
    """Update a stat."""
    state = storage.get('State', state_id)
    if state is None:
        abort(404)
    try:
        payload = request.get_json()
    except Exception as e:
        return make_response({'error': 'Not a JSON'}, 400)
    if payload:
        for key, value in payload.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(state, key, value)
        state.save()
        return make_response(state.to_dict(), 200)
    return make_response({}, 200)
