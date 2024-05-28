#!/usr/bin/python3
"""review crud routes."""
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.review import Review


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def all_reviews(place_id):
    """Retrieve all reviews."""
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    reviews = place.reviews
    result = []
    for review in reviews:
        result.append(review.to_dict())
    return make_response(jsonify(result))


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def one_review(review_id):
    """Retrieve one review."""
    review = storage.get('review', review_id)
    if review:
        return make_response(review.to_dict(), 200)
    abort(404)


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """Delete a review."""
    review = storage.get('review', review_id)
    if review:
        storage.delete(review)
        storage.save()
        return make_response({}, 200)
    abort(404)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """Create a review."""
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    try:
        payload = request.get_json()
    except Exception as e:
        return make_response({'error': 'Not a JSON'}, 400)

    if 'user_id' not in payload:
        return make_response({'error': 'Missing user_id'}, 400)
    if 'text' not in payload:
        return make_response({'error': 'Missing text'}, 400)

    user_id = payload.get('user_id')
    user = storage.get('User', user_id)
    if user is None:
        abort(404)

    if 'email' not in payload:
        return make_response({'error': 'Missing email'}, 400)

    review = Review(**payload)
    review.place_id = place_id
    review.save()
    return make_response(review.to_dict(), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def update_review(review_id):
    """Update a review."""
    review = storage.get('review', review_id)
    if review is None:
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
                setattr(review, key, value)
        review.save()
        return make_response(review.to_dict(), 200)
    return make_response({}, 200)
