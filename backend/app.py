from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os

app = Flask(__name__, static_folder='static')
CORS(app)  # Enable CORS for all routes

todos = []

@app.route('/todos', methods=['GET'])
def get_todos():
    return jsonify(todos)

@app.route('/todos', methods=['POST'])
def add_todo():
    data = request.get_json()
    if not data or 'title' not in data:
        return jsonify({'error': 'Title is required'}), 400
    todo = {
        'id': len(todos) + 1,
        'title': data['title'],
        'completed': data.get('completed', False)
    }
    todos.append(todo)
    return jsonify(todo), 201

@app.route('/todos/<int:id>', methods=['PUT'])
def update_todo(id):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    for todo in todos:
        if todo['id'] == id:
            if 'title' in data:
                todo['title'] = data['title']
            if 'completed' in data:
                todo['completed'] = data['completed']
            return jsonify({'message': 'Todo updated'})
    return jsonify({'error': 'Todo not found'}), 404

@app.route('/todos/<int:id>', methods=['DELETE'])
def delete_todo(id):
    global todos
    new_todos = [t for t in todos if t['id'] != id]
    if len(new_todos) == len(todos):
        return jsonify({'error': 'Todo not found'}), 404
    todos = new_todos
    return jsonify({'message': 'Todo deleted'})

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    app.run(debug=True)
