# api/routes.py

from flask import Blueprint, request, jsonify
from database.db_manager import Database

api = Blueprint('api', __name__)
dbm = Database()

# --- DATABASE LEVEL ---

@api.route('/databases', methods=['GET'])
def list_databases():
    return jsonify({"databases": dbm.list_databases()})

@api.route('/databases', methods=['POST'])
def create_database():
    data = request.json
    db_name = data['name']
    dbm.create_database(db_name)
    return jsonify({"message": f"Database '{db_name}' created."})

@api.route('/databases/<db_name>', methods=['DELETE'])
def delete_database(db_name):
    dbm.delete_database(db_name)
    return jsonify({"message": f"Database '{db_name}' deleted."})

# --- TABLE LEVEL ---

@api.route('/databases/<db_name>/tables', methods=['GET'])
def list_tables(db_name):
    return jsonify({"tables": dbm.list_tables(db_name)})

@api.route('/databases/<db_name>/tables', methods=['POST'])
def create_table(db_name):
    data = request.json
    table_name = data['name']
    columns = data['columns']  # e.g. [{"name": "id", "type": "int"}, {"name": "name", "type": "str"}]
    dbm.create_table(db_name, table_name, columns)
    return jsonify({"message": f"Table '{table_name}' created in database '{db_name}'."})

@api.route('/databases/<db_name>/tables/<table_name>', methods=['DELETE'])
def delete_table(db_name, table_name):
    dbm.delete_table(db_name, table_name)
    return jsonify({"message": f"Table '{table_name}' deleted from database '{db_name}'."})

# --- RECORD LEVEL ---

@api.route('/databases/<db_name>/tables/<table_name>/records', methods=['GET'])
def get_all_records(db_name, table_name):
    return jsonify(dbm.get_table(db_name, table_name).all_records())

@api.route('/databases/<db_name>/tables/<table_name>/records', methods=['POST'])
def insert_record(db_name, table_name):
    data = request.json  # full record
    dbm.get_table(db_name, table_name).insert(data)
    return jsonify({"message": "Record inserted."})

@api.route('/databases/<db_name>/tables/<table_name>/records/<record_id>', methods=['DELETE'])
def delete_record(db_name, table_name, record_id):
    dbm.get_table(db_name, table_name).delete(record_id)
    return jsonify({"message": "Record deleted."})

@api.route('/databases/<db_name>/tables/<table_name>/records/<record_id>', methods=['PUT'])
def update_record(db_name, table_name, record_id):
    new_data = request.json
    dbm.get_table(db_name, table_name).update(record_id, new_data)
    return jsonify({"message": "Record updated."})

# --- SEARCH / RANGE ---

@api.route('/databases/<db_name>/tables/<table_name>/search', methods=['POST'])
def search_records(db_name, table_name):
    query = request.json  # e.g., {"name": "John"}
    result = dbm.get_table(db_name, table_name).search(query)
    return jsonify(result)

@api.route('/databases/<db_name>/tables/<table_name>/range', methods=['POST'])
def range_query(db_name, table_name):
    data = request.json  # e.g., {"field": "age", "min": 18, "max": 25}
    result = dbm.get_table(db_name, table_name).range_query(data['field'], data['min'], data['max'])
    return jsonify(result)