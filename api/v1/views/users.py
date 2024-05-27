#!/usr/bin/python3
"""user crud routes."""
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage


@app_views.route('/users', methods=['GET'])
def all_users():
    """Retrieve all users."""
    all = storage.all('User')
    result = []
    for key, value in all.items():
        result.append(value.to_dict())
    return make_response(jsonify(result))


@app_views.route('/users/<user_id>', methods=['GET'])
def one_user(user_id):
    """Retrieve one user."""
    user = storage.get('User', user_id)
    if user:
        return make_response(user.to_dict(), 200)
    abort(404)


@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Delete a user."""
    user = storage.get('User', user_id)
    if user:
        storage.delete(user)
        return make_response({}, 200)
    abort(404)


@app_views.route('/users', methods=['POST'])
def create_user():
    """Create a user."""
    try:
        payload = request.get_json()
    except Exception as e:
        return make_response({'error': 'Not a JSON'}, 400)

    if 'password' not in payload:
        return make_response({'error': 'Missing password'}, 400)
    if 'email' not in payload:
        return make_response({'error': 'Missing email'}, 400)

    name = payload.get('name')
    user = user(name=name)
    user.save()
    return make_response(user.to_dict(), 201)


@app_views.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    """Update a stat."""
    user = storage.get('User', user_id)
    if user is None:
        abort(404)
    try:
        payload = request.get_json()
    except Exception as e:
        return make_response({'error': 'Not a JSON'}, 400)
    if payload:
        for key, value in payload.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(user, key, value)
        user.save()
        return make_response(user.to_dict(), 200)
    return make_response({}, 200)
