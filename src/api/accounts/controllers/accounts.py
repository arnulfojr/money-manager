
from .. import blueprint

from flask import request, make_response, jsonify
from cerberus import Validator

from lib.db import session
from lib.request import is_json
from core.accounts import Account


@blueprint.route('/', methods=['GET'])
def get_accounts():
    """Returns all the accounts registered"""
    accounts = Account.query()

    payload = [account.to_dict() for account in accounts]

    response = make_response(jsonify(payload), 200)

    return response


@blueprint.route('/', methods=['POST'])
@is_json
def save_account():
    payload = request.get_json()

    validator = Validator(Account.schema)

    if not validator.validate(payload):
        response = make_response(jsonify(validator.errors), 400)
        return response

    document = validator.document

    account = Account.from_dict(document)

    session.add(account)

    session.commit(account)
    session.flush()

    session.close()

    response = make_response(jsonify({}), 201)

    return response


@blueprint.route('/<code>/', methods=['GET'])
def get_account(code):
    account = Account.get(code)

    if account is None:
        response = make_response(jsonify({'message': 'No Account was found'}), 404)
        return response

    payload = account.to_dict()

    response = make_response(jsonify(payload), 200)

    return response


@blueprint.route('/<code>/', methods=['PUT'])
@is_json
def update_account(code):
    account = Account.get(code)

    if account is None:
        response = make_response(jsonify({'message': 'No Account was found'}), 404)
        return response

    validator = Validator(Account.schema)

    payload = request.get_json()

    if not validator.validate(payload):
        response = make_response(jsonify(validator.errors), 400)
        return response

    account = Account.from_dict(validator.document)

    payload = account.to_dict()

    response = make_response(jsonify(payload), 200)

    return response

