
from .. import blueprint

from flask import request, make_response, jsonify
from cerberus import Validator

from core.users import User
from lib.db import session


@blueprint.route('/', methods=['GET'])
def get_users():
    """Returns all the users"""
    users = User.query()

    payload = [user.to_dict() for user in users]

    response = make_response(jsonify(payload))

    return response


@blueprint.route('/<uuid:user_code>/', methods=['GET'])
def get_user(user_code):
    """Returns the user with the given code"""
    user = User.get(user_code)

    if user is None:
        return make_response('User was not found', 404)

    payload = user.to_dict()
    
    response = make_response(jsonify(payload), 200)

    return response


@blueprint.route('/', methods=['POST'])
def save_user():
    """Saves the incoming user profile"""
    schema = User.schema

    validator = Validator(schema)

    if validator.validate(request.get_json()):
        user = User.from_dict(validator.document)

        session.add(user)
        session.commit()
        
        payload = user.to_dict()
        status = 200

    else:

        status = 400
        payload = validator.errors

    response = make_response(jsonify(payload), status)

    session.flush()

    return response


@blueprint.route('/<user_code>/', methods=['PUT'])
def update_user(user_code):
    """Updates the user with the given code"""
    schema = User.schema

    validator = Validator(schema)

    if not validator.validate(request.get_json()):
        response = make_response(jsonify(validator.errors), 400)
        return response

    user = User.get(user_code)

    if user is None:
        response = make_response('No user found', 404)
        return response

    user = User.from_dict(validator.document, user)

    session.commit()
    session.flush()

    response = make_response('User was updated', 204)

    return response

