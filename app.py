# app.py
from flask import Flask, render_template, request, redirect, url_for, jsonify
from database.db_manager import DatabaseManager  # your B+ tree logic integration
import os

app = Flask(__name__)

# Simulated in-memory DB (replace with actual B+Tree logic)
db = DatabaseManager()

@app.route('/')
def home():
    databases = db.list_databases()
    return render_template('index.html', databases=databases)

@app.route('/database/<db_name>')
def show_tables(db_name):
    tables = db.list_tables(db_name)
    return render_template('tables.html', db_name=db_name, tables=tables)

@app.route('/database/<db_name>/table/<table_name>')
def show_records(db_name, table_name):
    records = db.get_records(db_name, table_name)
    return render_template('records.html', db_name=db_name, table_name=table_name, records=records)

@app.route('/create_database', methods=['POST'])
def create_database():
    name = request.form['db_name']
    db.create_database(name)
    return redirect(url_for('home'))

@app.route('/create_table/<db_name>', methods=['POST'])
def create_table(db_name):
    name = request.form['table_name']
    db.create_table(db_name, name)
    return redirect(url_for('show_tables', db_name=db_name))

@app.route('/add_record/<db_name>/<table_name>', methods=['POST'])
def add_record(db_name, table_name):
    key = request.form['key']
    value = request.form['value']
    db.insert_record(db_name, table_name, key, value)
    return redirect(url_for('show_records', db_name=db_name, table_name=table_name))

@app.route('/search/<db_name>/<table_name>', methods=['POST'])
def search(db_name, table_name):
    key = request.form['search_key']
    result = db.search(db_name, table_name, key)
    return jsonify(result)

@app.route('/range/<db_name>/<table_name>', methods=['POST'])
def range_query(db_name, table_name):
    start = request.form['start_key']
    end = request.form['end_key']
    result = db.range_query(db_name, table_name, start, end)
    return jsonify(result)

if __name__ == '__main__':
    if not os.path.exists('static'): os.mkdir('static')
    if not os.path.exists('templates'): os.mkdir('templates')
    app.run(debug=True)