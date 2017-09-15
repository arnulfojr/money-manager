
from .. import blueprint

from flask import request, make_response, jsonify
from sqlalchemy.exc import IntegrityError
from cerberus import Validator

from core.users import User
from core.users import load_user
from lib.db import session


@blueprint.route('/', methods=['GET'])
def get_users():
    """Returns all the users"""
    users = User.query()

    payload = [user.to_dict() for user in users]

    response = make_response(jsonify(payload))

    return response


@blueprint.route('/<uuid:user_code>/', methods=['GET'])
@load_user
def get_user(user_code, user):
    """Returns the user with the given code"""

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

        try:
            session.add(user)
            session.commit()

            payload = user.to_dict()
            status = 200
        except IntegrityError:
            status = 400
            payload = {'username': ['Username already exists']}
        
    else:

        status = 400
        payload = validator.errors

    response = make_response(jsonify(payload), status)

    session.flush()
    session.close()

    return response


@blueprint.route('/<user_code>/', methods=['PUT'])
@load_user
def update_user(user_code, user):
    """Updates the user with the given code"""
    schema = User.schema

    validator = Validator(schema)

    if not validator.validate(request.get_json()):
        response = make_response(jsonify(validator.errors), 400)
        return response

    if user is None:
        response = make_response('No user found', 404)
        return response

    user = User.from_dict(validator.document, user)

    session.commit()
    session.flush()
    session.close()

    response = make_response('User was updated', 204)

    return response


@blueprint.route('/<user_code>/', methods=['DELETE'])
@load_user
def delete_user(user_code, user):
    """Deletes the user"""
    if user is None:
        response = make_response('No user found with code {}'.format(user_code), 404)
        return response

    session.delete(user)
    session.commit()
    session.flush()

    session.close()

    response = make_response('User was deleted', 200)

    return response

