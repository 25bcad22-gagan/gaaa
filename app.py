from flask import Flask, request, jsonify
import psycopg2
import os
from flask_cors import CORS

# Initialize app
app = Flask(__name__)
CORS(app)

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")

# Connect to PostgreSQL
def get_connection():
    return psycopg2.connect(DATABASE_URL, sslmode='require')


# Create table if not exists
def init_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id SERIAL PRIMARY KEY,
            text TEXT NOT NULL,
            completed BOOLEAN DEFAULT FALSE
        );
    """)
    conn.commit()
    cur.close()
    conn.close()


# Run once when app starts
init_db()


# ---------------- ROUTES ---------------- #

# Home route (for testing)
@app.route("/")
def home():
    return "✅ API is running successfully!"


# Get all tasks
@app.route("/tasks", methods=["GET"])
def get_tasks():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, text, completed FROM tasks ORDER BY id DESC")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    tasks = []
    for row in rows:
        tasks.append({
            "id": row[0],
            "text": row[1],
            "completed": row[2]
        })

    return jsonify(tasks)


# Add new task
@app.route("/tasks", methods=["POST"])
def add_task():
    data = request.json

    if not data or "text" not in data:
        return jsonify({"error": "Task text is required"}), 400

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO tasks (text) VALUES (%s) RETURNING id",
        (data["text"],)
    )
    task_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({
        "id": task_id,
        "message": "Task added successfully"
    })


# Update task (mark complete/incomplete)
@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    data = request.json

    if "completed" not in data:
        return jsonify({"error": "completed field required"}), 400

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE tasks SET completed=%s WHERE id=%s",
        (data["completed"], task_id)
    )
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message": "Task updated"})


# Delete task
@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM tasks WHERE id=%s", (task_id,))
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message": "Task deleted"})


# Run locally
if __name__ == "__main__":
    app.run(debug=True)
