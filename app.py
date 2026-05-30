"""
Student Management System — REST API
A lightweight Flask backend used as the test target.
Run this server locally before executing the test suite.
"""

from flask import Flask, jsonify, request
from datetime import datetime

app = Flask(__name__)

# ─────────────────────────────────────────────
# In-memory data store (no DB required to run)
# ─────────────────────────────────────────────
students = {
    1: {
        "id": 1,
        "name": "Alice Johnson",
        "email": "alice.johnson@example.com",
        "age": 21,
        "course": "Computer Science",
        "grade": "A",
        "enrolled_at": "2023-08-01"
    },
    2: {
        "id": 2,
        "name": "Bob Smith",
        "email": "bob.smith@example.com",
        "age": 22,
        "course": "Electrical Engineering",
        "grade": "B+",
        "enrolled_at": "2023-08-01"
    },
    3: {
        "id": 3,
        "name": "Carol Williams",
        "email": "carol.w@example.com",
        "age": 20,
        "course": "Mathematics",
        "grade": "A-",
        "enrolled_at": "2024-01-15"
    }
}
next_id = 4


# ─── Helpers ──────────────────────────────────
def validate_student_payload(data, require_all=True):
    required_fields = ["name", "email", "age", "course"]
    errors = []

    if require_all:
        for field in required_fields:
            if field not in data:
                errors.append(f"Missing required field: '{field}'")

    if "email" in data and "@" not in data["email"]:
        errors.append("Invalid email format.")

    if "age" in data:
        if not isinstance(data["age"], int) or data["age"] < 1 or data["age"] > 120:
            errors.append("'age' must be an integer between 1 and 120.")

    return errors


# ─── Routes ───────────────────────────────────

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "timestamp": datetime.utcnow().isoformat()}), 200


@app.route("/api/students", methods=["GET"])
def get_all_students():
    course_filter = request.args.get("course")
    result = list(students.values())
    if course_filter:
        result = [s for s in result if s["course"].lower() == course_filter.lower()]
    return jsonify({"count": len(result), "students": result}), 200


@app.route("/api/students/<int:student_id>", methods=["GET"])
def get_student(student_id):
    student = students.get(student_id)
    if not student:
        return jsonify({"error": f"Student with id {student_id} not found."}), 404
    return jsonify(student), 200


@app.route("/api/students", methods=["POST"])
def create_student():
    global next_id
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body must be valid JSON."}), 400

    errors = validate_student_payload(data, require_all=True)
    if errors:
        return jsonify({"error": "Validation failed.", "details": errors}), 422

    new_student = {
        "id": next_id,
        "name": data["name"],
        "email": data["email"],
        "age": data["age"],
        "course": data["course"],
        "grade": data.get("grade", "N/A"),
        "enrolled_at": datetime.utcnow().strftime("%Y-%m-%d")
    }
    students[next_id] = new_student
    next_id += 1
    return jsonify(new_student), 201


@app.route("/api/students/<int:student_id>", methods=["PUT"])
def update_student(student_id):
    student = students.get(student_id)
    if not student:
        return jsonify({"error": f"Student with id {student_id} not found."}), 404

    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body must be valid JSON."}), 400

    errors = validate_student_payload(data, require_all=True)
    if errors:
        return jsonify({"error": "Validation failed.", "details": errors}), 422

    student.update({
        "name": data["name"],
        "email": data["email"],
        "age": data["age"],
        "course": data["course"],
        "grade": data.get("grade", student["grade"])
    })
    return jsonify(student), 200


@app.route("/api/students/<int:student_id>", methods=["PATCH"])
def partial_update_student(student_id):
    student = students.get(student_id)
    if not student:
        return jsonify({"error": f"Student with id {student_id} not found."}), 404

    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body must be valid JSON."}), 400

    errors = validate_student_payload(data, require_all=False)
    if errors:
        return jsonify({"error": "Validation failed.", "details": errors}), 422

    for key in ["name", "email", "age", "course", "grade"]:
        if key in data:
            student[key] = data[key]

    return jsonify(student), 200


@app.route("/api/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    student = students.pop(student_id, None)
    if not student:
        return jsonify({"error": f"Student with id {student_id} not found."}), 404
    return jsonify({"message": f"Student {student_id} deleted successfully."}), 200


@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Endpoint not found."}), 404


@app.errorhandler(405)
def method_not_allowed(e):
    return jsonify({"error": "Method not allowed."}), 405


if __name__ == "__main__":
    app.run(debug=True, port=5000)
