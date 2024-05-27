#!/usr/bin/python3
"""Amenity crud routes."""
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage


@app_views.route('/amenities', methods=['GET'])
def all_amenities():
    """Retrieve all amenities."""
    all = storage.all('Amenity')
    result = []
    for key, value in all.items():
        result.append(value.to_dict())
    return make_response(jsonify(result))


@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def one_amenity(amenity_id):
    """Retrieve one amenity."""
    amenity = storage.get('Amenity', amenity_id)
    if amenity:
        return make_response(amenity.to_dict(), 200)
    abort(404)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    """Delete a amenity."""
    amenity = storage.get('Amenity', amenity_id)
    if amenity:
        storage.delete(amenity)
        return make_response({}, 200)
    abort(404)


@app_views.route('/amenities', methods=['POST'])
def create_amenity():
    """Create a amenity."""
    try:
        payload = request.get_json()
    except Exception as e:
        return make_response({'error': 'Not a JSON'}, 400)

    if payload and 'name' not in payload:
        return make_response({'error': 'Missing name'}, 400)

    name = payload.get('name')
    amenity = amenity(name=name)
    amenity.save()
    return make_response(amenity.to_dict(), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def update_amenity(amenity_id):
    """Update a stat."""
    amenity = storage.get('Amenity', amenity_id)
    if amenity is None:
        abort(404)
    try:
        payload = request.get_json()
    except Exception as e:
        return make_response({'error': 'Not a JSON'}, 400)
    if payload:
        for key, value in payload.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(amenity, key, value)
        amenity.save()
        return make_response(amenity.to_dict(), 200)
    return make_response({}, 200)
