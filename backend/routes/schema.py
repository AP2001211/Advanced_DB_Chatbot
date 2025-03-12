from flask import Blueprint, jsonify
from db_schema import get_db_schema

schema_blueprint = Blueprint('schema', __name__)

@schema_blueprint.route('/', methods=['GET'])
def get_schema():
    schema = get_db_schema()
    return jsonify(schema)
