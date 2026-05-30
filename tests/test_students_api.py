"""
tests/test_students_api.py

Automated test suite for Student Management System REST API.
Covers: CRUD operations, status codes, response payloads,
        error handling, edge cases, and regression scenarios.

Run: pytest tests/ -v --tb=short
"""

import pytest
import requests

BASE_URL = "http://localhost:5000/api/students"
HEALTH_URL = "http://localhost:5000/health"

# ─── Fixtures ─────────────────────────────────────────────────────────────────

@pytest.fixture(scope="session")
def base_url():
    return BASE_URL


@pytest.fixture
def sample_student():
    return {
        "name": "Test Student",
        "email": "test.student@example.com",
        "age": 22,
        "course": "Computer Science",
        "grade": "A"
    }


@pytest.fixture
def created_student(sample_student):
    """Creates a student and returns its data; cleans up after the test."""
    response = requests.post(BASE_URL, json=sample_student)
    assert response.status_code == 201, "Fixture: Failed to create student"
    data = response.json()
    yield data
    # Cleanup
    requests.delete(f"{BASE_URL}/{data['id']}")


# ─── 1. Health Check ──────────────────────────────────────────────────────────

class TestHealthCheck:
    def test_health_endpoint_returns_200(self):
        """Server should respond with 200 OK on /health."""
        r = requests.get(HEALTH_URL)
        assert r.status_code == 200

    def test_health_response_has_status_ok(self):
        """Response body should contain status: ok."""
        r = requests.get(HEALTH_URL)
        assert r.json()["status"] == "ok"

    def test_health_response_has_timestamp(self):
        """Response body should include a timestamp field."""
        r = requests.get(HEALTH_URL)
        assert "timestamp" in r.json()


# ─── 2. GET All Students ──────────────────────────────────────────────────────

class TestGetAllStudents:
    def test_get_all_returns_200(self):
        r = requests.get(BASE_URL)
        assert r.status_code == 200

    def test_get_all_returns_json(self):
        r = requests.get(BASE_URL)
        assert r.headers["Content-Type"] == "application/json"

    def test_get_all_response_has_students_list(self):
        r = requests.get(BASE_URL)
        body = r.json()
        assert "students" in body
        assert isinstance(body["students"], list)

    def test_get_all_response_has_count(self):
        r = requests.get(BASE_URL)
        body = r.json()
        assert "count" in body
        assert body["count"] == len(body["students"])

    def test_filter_students_by_course(self):
        r = requests.get(BASE_URL, params={"course": "Computer Science"})
        assert r.status_code == 200
        students = r.json()["students"]
        for student in students:
            assert student["course"].lower() == "computer science"

    def test_filter_nonexistent_course_returns_empty(self):
        r = requests.get(BASE_URL, params={"course": "Astrophysics"})
        assert r.status_code == 200
        assert r.json()["count"] == 0


# ─── 3. GET Single Student ────────────────────────────────────────────────────

class TestGetStudentById:
    def test_get_existing_student_returns_200(self):
        r = requests.get(f"{BASE_URL}/1")
        assert r.status_code == 200

    def test_get_existing_student_has_expected_fields(self):
        r = requests.get(f"{BASE_URL}/1")
        body = r.json()
        for field in ["id", "name", "email", "age", "course", "grade"]:
            assert field in body, f"Missing field: {field}"

    def test_get_existing_student_id_matches(self):
        r = requests.get(f"{BASE_URL}/1")
        assert r.json()["id"] == 1

    def test_get_nonexistent_student_returns_404(self):
        r = requests.get(f"{BASE_URL}/99999")
        assert r.status_code == 404

    def test_get_nonexistent_student_returns_error_message(self):
        r = requests.get(f"{BASE_URL}/99999")
        assert "error" in r.json()


# ─── 4. POST – Create Student ─────────────────────────────────────────────────

class TestCreateStudent:
    def test_create_valid_student_returns_201(self, sample_student):
        r = requests.post(BASE_URL, json=sample_student)
        assert r.status_code == 201
        # Cleanup
        requests.delete(f"{BASE_URL}/{r.json()['id']}")

    def test_create_student_response_has_id(self, sample_student):
        r = requests.post(BASE_URL, json=sample_student)
        body = r.json()
        assert "id" in body
        requests.delete(f"{BASE_URL}/{body['id']}")

    def test_create_student_persists_data(self, created_student):
        r = requests.get(f"{BASE_URL}/{created_student['id']}")
        assert r.status_code == 200
        assert r.json()["name"] == created_student["name"]

    def test_create_student_missing_name_returns_422(self):
        payload = {"email": "x@x.com", "age": 21, "course": "CS"}
        r = requests.post(BASE_URL, json=payload)
        assert r.status_code == 422

    def test_create_student_missing_email_returns_422(self):
        payload = {"name": "X", "age": 21, "course": "CS"}
        r = requests.post(BASE_URL, json=payload)
        assert r.status_code == 422

    def test_create_student_invalid_email_returns_422(self):
        payload = {"name": "X", "email": "not-an-email", "age": 21, "course": "CS"}
        r = requests.post(BASE_URL, json=payload)
        assert r.status_code == 422

    def test_create_student_invalid_age_returns_422(self):
        payload = {"name": "X", "email": "x@x.com", "age": -5, "course": "CS"}
        r = requests.post(BASE_URL, json=payload)
        assert r.status_code == 422

    def test_create_student_empty_body_returns_400(self):
        r = requests.post(BASE_URL, data="not json",
                          headers={"Content-Type": "application/json"})
        assert r.status_code == 400

    def test_create_student_no_body_returns_400(self):
        r = requests.post(BASE_URL)
        assert r.status_code == 400

    def test_create_student_response_includes_enrolled_at(self, sample_student):
        r = requests.post(BASE_URL, json=sample_student)
        body = r.json()
        assert "enrolled_at" in body
        requests.delete(f"{BASE_URL}/{body['id']}")


# ─── 5. PUT – Full Update ─────────────────────────────────────────────────────

class TestUpdateStudent:
    def test_put_valid_payload_returns_200(self, created_student):
        payload = {
            "name": "Updated Name",
            "email": "updated@example.com",
            "age": 25,
            "course": "Data Science",
            "grade": "B"
        }
        r = requests.put(f"{BASE_URL}/{created_student['id']}", json=payload)
        assert r.status_code == 200

    def test_put_updates_name(self, created_student):
        payload = {
            "name": "New Name",
            "email": created_student["email"],
            "age": created_student["age"],
            "course": created_student["course"]
        }
        r = requests.put(f"{BASE_URL}/{created_student['id']}", json=payload)
        assert r.json()["name"] == "New Name"

    def test_put_nonexistent_student_returns_404(self):
        payload = {"name": "X", "email": "x@x.com", "age": 21, "course": "CS"}
        r = requests.put(f"{BASE_URL}/99999", json=payload)
        assert r.status_code == 404

    def test_put_missing_required_field_returns_422(self, created_student):
        payload = {"name": "Only Name"}
        r = requests.put(f"{BASE_URL}/{created_student['id']}", json=payload)
        assert r.status_code == 422

    def test_put_invalid_email_returns_422(self, created_student):
        payload = {
            "name": "X",
            "email": "bad-email",
            "age": 21,
            "course": "CS"
        }
        r = requests.put(f"{BASE_URL}/{created_student['id']}", json=payload)
        assert r.status_code == 422


# ─── 6. PATCH – Partial Update ────────────────────────────────────────────────

class TestPartialUpdateStudent:
    def test_patch_single_field_returns_200(self, created_student):
        r = requests.patch(f"{BASE_URL}/{created_student['id']}",
                           json={"grade": "A+"})
        assert r.status_code == 200

    def test_patch_updates_only_specified_field(self, created_student):
        original_email = created_student["email"]
        r = requests.patch(f"{BASE_URL}/{created_student['id']}",
                           json={"grade": "A+"})
        body = r.json()
        assert body["grade"] == "A+"
        assert body["email"] == original_email

    def test_patch_nonexistent_student_returns_404(self):
        r = requests.patch(f"{BASE_URL}/99999", json={"grade": "A"})
        assert r.status_code == 404

    def test_patch_invalid_age_returns_422(self, created_student):
        r = requests.patch(f"{BASE_URL}/{created_student['id']}",
                           json={"age": 999})
        assert r.status_code == 422


# ─── 7. DELETE Student ────────────────────────────────────────────────────────

class TestDeleteStudent:
    def test_delete_existing_student_returns_200(self, sample_student):
        create_r = requests.post(BASE_URL, json=sample_student)
        student_id = create_r.json()["id"]
        r = requests.delete(f"{BASE_URL}/{student_id}")
        assert r.status_code == 200

    def test_delete_returns_success_message(self, sample_student):
        create_r = requests.post(BASE_URL, json=sample_student)
        student_id = create_r.json()["id"]
        r = requests.delete(f"{BASE_URL}/{student_id}")
        assert "message" in r.json()

    def test_delete_removes_student_from_system(self, sample_student):
        create_r = requests.post(BASE_URL, json=sample_student)
        student_id = create_r.json()["id"]
        requests.delete(f"{BASE_URL}/{student_id}")
        r = requests.get(f"{BASE_URL}/{student_id}")
        assert r.status_code == 404

    def test_delete_nonexistent_student_returns_404(self):
        r = requests.delete(f"{BASE_URL}/99999")
        assert r.status_code == 404

    def test_double_delete_returns_404(self, sample_student):
        create_r = requests.post(BASE_URL, json=sample_student)
        student_id = create_r.json()["id"]
        requests.delete(f"{BASE_URL}/{student_id}")
        r = requests.delete(f"{BASE_URL}/{student_id}")
        assert r.status_code == 404


# ─── 8. Regression Tests ──────────────────────────────────────────────────────

class TestRegressionScenarios:
    def test_get_after_update_reflects_new_data(self, created_student):
        """Regression: GET after PUT should return updated data."""
        new_name = "Regression Updated Name"
        payload = {
            "name": new_name,
            "email": created_student["email"],
            "age": created_student["age"],
            "course": created_student["course"]
        }
        requests.put(f"{BASE_URL}/{created_student['id']}", json=payload)
        r = requests.get(f"{BASE_URL}/{created_student['id']}")
        assert r.json()["name"] == new_name

    def test_create_does_not_overwrite_existing_students(self, sample_student):
        """Regression: POST should always generate a new unique ID."""
        r1 = requests.post(BASE_URL, json=sample_student)
        r2 = requests.post(BASE_URL, json=sample_student)
        id1 = r1.json()["id"]
        id2 = r2.json()["id"]
        assert id1 != id2
        requests.delete(f"{BASE_URL}/{id1}")
        requests.delete(f"{BASE_URL}/{id2}")

    def test_total_count_decrements_after_delete(self, sample_student):
        """Regression: count in GET all should decrease after a DELETE."""
        r_before = requests.get(BASE_URL)
        count_before = r_before.json()["count"]

        create_r = requests.post(BASE_URL, json=sample_student)
        student_id = create_r.json()["id"]

        r_after_create = requests.get(BASE_URL)
        assert r_after_create.json()["count"] == count_before + 1

        requests.delete(f"{BASE_URL}/{student_id}")
        r_after_delete = requests.get(BASE_URL)
        assert r_after_delete.json()["count"] == count_before

    def test_invalid_endpoint_returns_404(self):
        """Regression: unknown endpoints should return 404."""
        r = requests.get("http://localhost:5000/api/nonexistent")
        assert r.status_code == 404

    def test_method_not_allowed_returns_405(self):
        """Regression: DELETE on /api/students (no ID) should return 405."""
        r = requests.delete(BASE_URL)
        assert r.status_code == 405
