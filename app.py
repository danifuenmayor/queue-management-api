from flask import Flask, jsonify, request, render_template
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_cors import CORS
from models import db
from myqueue import MyQueue

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['ENV'] = 'development'
app.config['SQLALCHEMY_DATABASE_ URI'] =  'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
CORS(app)
Migrate(app, db)

manager = Manager(app)
manager.add_command("db", MigrateCommand)

my_queue = MyQueue()

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/all')
def index():
    users = my_queue.get_queue()
    return jsonify(users), 200

@app.route('/new', methods=['POST'])
def create():
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400
    
    name = request.json.get('name', None)
    phone = request.json.get('phone', None)

    if not name or name == '':
        return jsonify({"error": "Name in required"}), 400
    if not phone or phone == '':
        return jsonify({"error": "Phone is required"}), 400

    user = {
        "name": name,
        "phone": phone
    }

    new_user = my_queue.enqueue(user)

    return jsonify({"msg": "User added to the list", "result": new_user}), 200

@app.route('/next')
def next():
    deleted_user = my_queue.dequeue()
    return jsonify({"msg":"User deleted from the list", "result": deleted_user}), 200

if __name__ == "__main__":
    manager.run()
