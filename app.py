from flask import Flask, render_template, request, redirect, url_for
from database import db_manager  # Assuming your Database class is in database.py
import os
import json

app = Flask(__name__)
db_manager = db_manager.DatabaseManager()

@app.route('/')
def home():
    if not os.path.exists('databases'):
        os.makedirs('databases')
    dbs = [f[:-5] for f in os.listdir('databases') if f.endswith('.json')]
    return render_template('home.html', databases=dbs)

@app.route('/create_db', methods=['POST'])
def create_db():
    db_name = request.form['db_name']
    db_path = os.path.join('databases', f'{db_name}.json')
    if not os.path.exists(db_path):
        with open(db_path, 'w') as f:
            json.dump({}, f)
    return redirect(url_for('home'))

@app.route('/delete_db/<db_name>', methods=['POST'])
def delete_db(db_name):
    db_path = os.path.join('databases', f'{db_name}.json')
    if os.path.exists(db_path):
        os.remove(db_path)
    return redirect(url_for('home'))



@app.route('/<db_name>/tables')
def list_tables(db_name):
    try:
        tables = db_manager.list_tables(db_name)
    except Exception as e:
        return str(e)
    return render_template('list_tables.html', db_name=db_name, tables=tables)

@app.route('/view_database/<db_name>')
def view_database(db_name):
    db_path = os.path.join("databases", f"{db_name}.json")
    if not os.path.exists(db_path):
        return f"Database '{db_name}' not found.", 404

    with open(db_path, 'r') as f:
        db_data = json.load(f)

    tables = list(db_data.keys())
    return render_template('view_database.html', db_name=db_name, tables=tables)

@app.route('/delete_table/<db_name>/<table_name>', methods=['POST'])
def delete_table(db_name, table_name):
    db_path = os.path.join("databases", f"{db_name}.json")
    with open(db_path, 'r') as f:
        db_data = json.load(f)
    if table_name in db_data:
        del db_data[table_name]
    with open(db_path, 'w') as f:
        json.dump(db_data, f)
    return redirect(url_for('view_database', db_name=db_name))


@app.route('/view_table/<db_name>/<table_name>')
def view_table(db_name, table_name):
    db_path = os.path.join("databases", f"{db_name}.json")
    with open(db_path, 'r') as f:
        db_data = json.load(f)
    table = db_data.get(table_name, [])
    return render_template('view_table.html', db_name=db_name, table_name=table_name, records=table)

@app.route('/insert_row/<db_name>/<table_name>', methods=['POST'])
def insert_row(db_name, table_name):
    db_path = os.path.join("databases", f"{db_name}.json")
    with open(db_path, 'r') as f:
        db_data = json.load(f)

    new_record = request.form.to_dict()
    db_data[table_name].append(new_record)

    with open(db_path, 'w') as f:
        json.dump(db_data, f)

    return redirect(url_for('view_table', db_name=db_name, table_name=table_name))

@app.route('/delete_row/<db_name>/<table_name>/<int:row_index>', methods=['POST'])
def delete_row(db_name, table_name, row_index):
    db_path = os.path.join("databases", f"{db_name}.json")
    with open(db_path, 'r') as f:
        db_data = json.load(f)

    if 0 <= row_index < len(db_data[table_name]):
        db_data[table_name].pop(row_index)

    with open(db_path, 'w') as f:
        json.dump(db_data, f)

    return redirect(url_for('view_table', db_name=db_name, table_name=table_name))

@app.route('/create_table/<db_name>', methods=['GET', 'POST'])
def create_table(db_name):
    columns = None
    table_name = None
    if request.method == 'POST':
        action = request.form.get('action')  # Get the action (set_columns or create_table)
        
        if action == 'set_columns':
            # Check if 'num_columns' is in the form and is a valid number
            num_columns = request.form.get('num_columns')
            if num_columns is not None:
                try:
                    columns = int(num_columns)  # Make sure it's an integer
                    table_name = request.form.get('table_name')  # Get the table name
                except ValueError:
                    columns = None  # If the value is invalid, set columns to None
            else:
                columns = None  # If num_columns isn't in the form, set columns to None
        elif action == 'create_table' and columns is not None:
            # Handle table creation with columns and their names
            col_names = [request.form.get(f'col{i}') for i in range(columns)]
            # Add logic here for creating the table using col_names and table_name
            # Save the table to your database or data structure
            
            return redirect(url_for('show_db', db_name=db_name))  # Redirect to the DB view after creation

    return render_template('create_table.html', db_name=db_name, columns=columns, table_name=table_name)



if __name__ == '__main__':
    app.run(debug=True)
