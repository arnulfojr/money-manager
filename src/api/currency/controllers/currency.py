
from flask import request, make_response, jsonify
from cerberus import Validator
from sqlalchemy.exc import IntegrityError

from .. import blueprint

from lib.db import session
from lib.request import is_json

from core.currency import Currency


@blueprint.route('/', methods=['GET'])
def get_currencies():
    currencies = Currency.query()

    payload = [currency.to_dict() for currency in currencies]

    response = make_response(jsonify(payload), 200)

    return response


@blueprint.route('/', methods=['POST'])
@is_json
def save_currency():
    validator = Validator(Currency.schema)
    payload = request.get_json()

    if not validator.validate(payload):
        response = make_response(jsonify(validator.errors), 400)
        return response

    document = validator.document
    currency = Currency.from_dict(document)

    status = 201

    try:
        session.add(currency)
        session.commit()
        session.flush()
        payload = currency.to_dict()
    except IntegrityError:
        status = 400
        payload = {'code': ['Currency code already exists']}

    session.close()
    
    response = make_response(jsonify(payload), status)
    
    return response


@blueprint.route('/<code>/', methods=['GET'])
def get_currency(code):
    currency = Currency.get(code)

    if currency is None:
        response = make_response(jsonify({'message': 'Currency not found'}), 404)
        return response

    payload = currency.to_dict()

    response = make_response(jsonify(payload), 200)

    return response


@blueprint.route('/<code>/', methods=['PUT'])
@is_json
def update_currency(code):
    validator = Validator(Currency.schema)

    payload = request.get_json()

    if not validator.validate(payload):
        response = make_response(jsonify(validator.errors), 400)
        return response

    currency = Currency.get(code)
    if currency is None:
        response = make_response(jsonify({'message': 'Currency not found'}), 404)
        return response

    document = validator.document
    currency = Currency.from_dict(document, currency=currency)

    session.add(currency)
    status = 200

    try:
        session.commit()
        session.flush()

        payload = currency.to_dict()
    except IntegrityError:
        payload = {'code': ['code was already taken']}
        status = 400

    session.close()

    response = make_response(jsonify(payload), 200)

    return response


@blueprint.route('/<code>/', methods=['DELETE'])
def delete_currency(code):
    currency = Currency.get(code)

    if currency is None:
        response = make_response(jsonify({'code': ['code was not found']}), 404)
        return response

    session.delete(currency)
    session.commit()
    session.flush()

    session.close()

    payload = {'message': 'Currency {} was deleted'.format(code)}
    response = make_response(jsonify(payload), 200)

    return response

