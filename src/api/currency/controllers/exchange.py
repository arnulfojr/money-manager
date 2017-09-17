
from flask import make_response, request, jsonify
from cerberus import Validator
from sqlalchemy.exc import IntegrityError

from .. import blueprint
from lib.db import session
from lib.request import is_json

from core.currency import ExchangeRate


@blueprint.route('/<currency_code>/rate/', methods=['GET'])
def get_rates_for(currency_code):
    latest = request.args.get('latest', 'true') == 'true'
    historic = request.args.get('historic', 'false') == 'true'

    to = request.args.get('to', None)

    if to is None:
        response = make_response(jsonify({'to':['Please give a target currency']}), 400)
        return response

    if not historic and latest:
        rate = ExchangeRate.latest(currency_code, to)
        payload = rate.to_dict()
    else:
        rates = ExchangeRate.history(from_code=currency_code, to_code=to)
        payload = [rate.to_dict() for rate in rates]

    response = make_response(jsonify(payload), 200)

    return response


@blueprint.route('/<currency_code>/rate/', methods=['POST'])
@is_json
def save_rate(currency_code):

    validator = Validator(ExchangeRate.schema)

    payload = request.get_json()

    if not validator.validate(payload):
        response = make_response(jsonify(validator.errors), 400)
        return response

    document = validator.document

    rate = ExchangeRate.from_dict(document, from_code=currency_code)

    session.add(rate)

    try:
        session.commit()
        session.flush()
        response = make_response(jsonify(rate.to_dict()), 201)
    except IntegrityError as exc:
        session.rollback()
        response = make_response(jsonify({'message': exc.message}), 400)

    session.close()

    return response


@blueprint.route('/<currency_code>/rate/<rate_code>/', methods=['DELETE'])
def delete_rate(currency_code, rate_code):
    rate = ExchangeRate.get(rate_code)

    if rate is None:
        response = make_response(jsonify({'code': ['Rate was not found']}), 404)
        return response

    session.delete(rate)

    session.commit()
    session.flush()

    response = make_response(jsonify({'message': 'Rate was deleted'}), 200)

    return response

