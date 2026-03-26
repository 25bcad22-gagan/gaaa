import os
from flask import Flask, render_template, request, jsonify
import psycopg2
from urllib.parse import urlparse

app = Flask(_name_)

# --- Get DATABASE_URL from environment ---
DATABASE_URL = os.environ.get("DATABASE_URL")

# --- Parse DB URL ---
result = urlparse(DATABASE_URL)

db_host = result.hostname
db_port = result.port or 5432
db_name = result.path[1:]
db_user = result.username
db_password = result.password


# --- Function to get DB connection ---
def get_db_connection():
    return psycopg2.connect(
        host=db_host,
        port=db_port,
        database=db_name,
        user=db_user,
        password=db_password
    )


# --- Initialize DB (create table if not exists) ---
def init_db():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS contacts (
        id SERIAL PRIMARY KEY,
        name TEXT,
        email TEXT,
        message TEXT
    )
    """)

    conn.commit()
    cur.close()
    conn.close()


# Run DB init once on startup
init_db()


# --- Routes ---
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/contact', methods=['POST'])
def contact():
    data = request.json

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO contacts (name, email, message) VALUES (%s, %s, %s)",
        (data['name'], data['email'], data['message'])
    )

    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message": "Message saved successfully!"})


@app.route('/admin')
def admin():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM contacts ORDER BY id DESC")
    data = cur.fetchall()

    cur.close()
    conn.close()

    return render_template("admin.html", data=data)


# --- Run locally only ---
if _name_ == '_main_':
    app.run(debug=True)