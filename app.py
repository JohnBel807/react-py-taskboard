from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
import os
# routes_brayan.py (puede estar en app.py al inicio)
from flask import Blueprint, request, jsonify
from datetime import datetime
import os, sqlite3, uuid

bp = Blueprint("brayans", __name__)

def conn():
    c = sqlite3.connect("instance/mydatabase.db")
    c.row_factory = sqlite3.Row
    return c

@bp.post("/api/brayans")
def create_brayan():
    data = request.get_json(force=True)
    name  = (data.get("name") or "").strip()
    phone = (data.get("phone") or "").strip()
    email = (data.get("email") or "").strip()
    consent = bool(data.get("consent") is True)
    consent_text = (data.get("consent_text") or "").strip()
    if not (name and phone and email and consent and consent_text):
        return {"error":"Faltan campos o consentimiento"}, 400
    consent_ts = datetime.now().isoformat(timespec="seconds")
    ip = request.remote_addr
    with conn() as cx:
        cur = cx.execute("""
            INSERT INTO brayans(name, phone, email, consent, consent_text, consent_timestamp, consent_ip, created_at)
            VALUES (?,?,?,?,?,?,?,?)
        """, (name, phone, email, 1, consent_text, consent_ts, ip, consent_ts))
        brayan_id = cur.lastrowid
    return {"id": brayan_id}, 201

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@bp.post("/api/posts")
def create_post():
    brayan_id = request.form.get("brayan_id")
    kind = (request.form.get("kind") or "text").strip()
    content_text = (request.form.get("content_text") or "").strip()
    link_url = (request.form.get("link_url") or "").strip()
    image = request.files.get("image")
    if not brayan_id:
        return {"error":"brayan_id requerido"}, 400
    if kind not in ("text","image","link"):
        return {"error":"kind inválido"}, 400
    if kind == "text" and not content_text:
        return {"error":"texto requerido"}, 400
    if kind == "link" and not link_url:
        return {"error":"link requerido"}, 400
    image_path = None
    if kind == "image":
        if not image:
            return {"error":"imagen requerida"}, 400
        ext = os.path.splitext(image.filename)[1].lower()
        if ext not in (".jpg",".jpeg",".png"):
            return {"error":"solo .jpg/.jpeg/.png"}, 400
        filename = f"{uuid.uuid4().hex}{ext}"
        path = os.path.join(UPLOAD_DIR, filename)
        image.save(path)
        image_path = path
    ts = datetime.now().isoformat(timespec="seconds")
    with conn() as cx:
        cx.execute("""
          INSERT INTO posts (brayan_id, kind, content_text, image_path, link_url, status, created_at)
          VALUES (?,?,?,?,?,'pending',?)
        """, (brayan_id, kind, content_text or None, image_path, link_url or None, ts))
    return {"ok": True}, 201
# Fin routes_brayan.py


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
