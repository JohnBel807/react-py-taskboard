from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
import os

app = Flask(__name__)

# Permite CRA (3000) y Vite (5173). En prod limita al dominio real.
CORS(app, resources={r"/api/*": {"origins": ["http://localhost:3000", "http://localhost:5173"]}})

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

@app.route('/api/data', methods=['GET'])
def get_data():
    return jsonify(message="Hola my doggy!")

class User(db.Model):
    id   = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

@app.route('/api/greet', methods=['GET','POST'])
def greet():
    if request.method == 'GET':
        return jsonify(greeting="Hello, World!")
    if not request.is_json:
        return jsonify(error="Invalid input, JSON expected"), 400

    data = request.get_json() or {}
    name = (data.get('name') or '').strip()
    if not name:
        return jsonify(error="Name is required"), 400

    # Guardar en DB (idempotente por 'unique')
    try:
        user = User(name=name)
        db.session.add(user)
        db.session.commit()
        created = True
    except IntegrityError:
        db.session.rollback()
        created = False

    resp = jsonify(
        greeting=f"Hello, {name}!",
        saved=True,
        created=created
    )
    return (resp, 201) if created else (resp, 200)

@app.route('/api/users', methods=['POST'])
def create_user():
    if not request.is_json:
        return jsonify(error="Invalid input, JSON expected"), 400
    data = request.get_json() or {}
    name = (data.get('name') or '').strip()
    if not name:
        return jsonify(error="Name is required"), 400
    try:
        u = User(name=name)
        db.session.add(u)
        db.session.commit()
        return jsonify(id=u.id, name=u.name), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify(error="User already exists"), 409

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)
