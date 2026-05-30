# REST API Testing – Student Management System

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-3.0-lightgrey?logo=flask)
![Postman](https://img.shields.io/badge/Postman-Collection-orange?logo=postman)
![Pytest](https://img.shields.io/badge/Pytest-8.x-green?logo=pytest)
![Tests](https://img.shields.io/badge/Test%20Cases-42-brightgreen)
![Status](https://img.shields.io/badge/Status-Complete-success)

A complete REST API testing project for a **Student Management System** — covering manual test cases in Postman and an automated test suite in Python (pytest + requests). Demonstrates real-world QA skills including CRUD validation, status code verification, error-handling checks, and regression testing.

---

## 📋 Table of Contents

- [Project Overview](#project-overview)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [API Endpoints](#api-endpoints)
- [Getting Started](#getting-started)
- [Running the Tests](#running-the-tests)
- [Postman Collection](#postman-collection)
- [Test Coverage Summary](#test-coverage-summary)
- [Key Testing Scenarios](#key-testing-scenarios)
- [Sample Test Report](#sample-test-report)

---

## Project Overview

This project tests a Student Management REST API built with Flask. The testing strategy covers:

- **CRUD operations** — Create, Read, Update (PUT & PATCH), Delete
- **Status code verification** — 200, 201, 400, 404, 405, 422
- **Response payload validation** — field presence, data types, value correctness
- **Error handling** — invalid inputs, missing fields, bad email formats, out-of-range ages
- **Regression testing** — ensuring backend changes don't break existing functionality
- **Edge cases** — double deletes, empty bodies, unknown endpoints, method-not-allowed scenarios

---

## Tech Stack

| Tool       | Purpose                              |
|------------|--------------------------------------|
| Python     | Test automation language             |
| Flask      | Backend API server (test target)     |
| Postman    | Manual API testing & collection      |
| pytest     | Test framework for automated suite   |
| requests   | HTTP client for Python tests         |
| pytest-html| HTML test report generation          |

---

## Project Structure

```
student-management-api-testing/
│
├── app.py                          # Flask REST API (test target)
├── requirements.txt                # Python dependencies
├── pytest.ini                      # Pytest configuration
├── .gitignore
│
├── tests/
│   ├── conftest.py                 # Session fixtures & server health check
│   └── test_students_api.py        # Full automated test suite (42 test cases)
│
├── collections/
│   ├── Student_Management_API.postman_collection.json   # Postman collection
│   └── SMS_Local.postman_environment.json               # Postman environment
│
├── docs/
│   ├── manual_test_cases.md        # Detailed manual test case documentation
│   └── bug_report_template.md      # Bug reporting template with sample
│
└── reports/                        # Auto-generated HTML reports (pytest-html)
```

---

## API Endpoints

| Method | Endpoint                  | Description              |
|--------|---------------------------|--------------------------|
| GET    | `/health`                 | Server health check      |
| GET    | `/api/students`           | Get all students         |
| GET    | `/api/students?course=X`  | Filter students by course|
| GET    | `/api/students/:id`       | Get student by ID        |
| POST   | `/api/students`           | Create a new student     |
| PUT    | `/api/students/:id`       | Full update of a student |
| PATCH  | `/api/students/:id`       | Partial update           |
| DELETE | `/api/students/:id`       | Delete a student         |

### Request / Response Example

**POST /api/students**

Request body:
```json
{
  "name": "Alice Johnson",
  "email": "alice@example.com",
  "age": 21,
  "course": "Computer Science",
  "grade": "A"
}
```

Response `201 Created`:
```json
{
  "id": 4,
  "name": "Alice Johnson",
  "email": "alice@example.com",
  "age": 21,
  "course": "Computer Science",
  "grade": "A",
  "enrolled_at": "2024-06-01"
}
```

---

## Getting Started

### Prerequisites

- Python 3.10+
- pip
- Postman (for manual testing)

### 1. Clone the Repository

```bash
git clone https://github.com/<your-username>/student-management-api-testing.git
cd student-management-api-testing
```

### 2. Create a Virtual Environment

```bash
python -m venv venv

# macOS/Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Start the Flask Server

```bash
python app.py
```

Server runs at `http://localhost:5000`. Keep this terminal open.

---

## Running the Tests

Open a **new terminal** (with venv activated):

### Run Full Test Suite

```bash
pytest
```

### Run with Verbose Output

```bash
pytest -v
```

### Run a Specific Test Class

```bash
pytest tests/test_students_api.py::TestCreateStudent -v
```

### Run a Specific Test

```bash
pytest tests/test_students_api.py::TestDeleteStudent::test_delete_removes_student_from_system -v
```

### Generate HTML Report

```bash
pytest --html=reports/test_report.html --self-contained-html
```

Open `reports/test_report.html` in your browser to view the report.

---

## Postman Collection

### Import the Collection

1. Open Postman
2. Click **Import** → select `collections/Student_Management_API.postman_collection.json`
3. Import the environment → `collections/SMS_Local.postman_environment.json`
4. Select **SMS – Local Environment** from the environment dropdown

### Run All Requests

- Use **Collection Runner** (▶ Run button) to execute all requests in sequence
- Test scripts are embedded in each request and auto-validate responses

### Collection Structure

```
🔎 Health Check (1 request)
📚 GET Students (5 requests)
➕ POST – Create Student (5 requests)
✏️ PUT – Full Update (3 requests)
🩹 PATCH – Partial Update (3 requests)
🗑️ DELETE Student (2 requests)
🔁 Regression Scenarios (2 requests)
```

---

## Test Coverage Summary

| Category             | Test Cases | Scenarios Covered                                           |
|----------------------|------------|-------------------------------------------------------------|
| Health Check         | 3          | 200 OK, JSON response, timestamp field                      |
| GET All Students     | 6          | Full list, course filter, empty filter, count validation    |
| GET Student by ID    | 3          | Valid ID, 404 not found, all fields present                 |
| POST Create Student  | 11         | Valid create, missing fields, invalid email/age, empty body |
| PUT Full Update      | 5          | Valid update, 404, missing fields, invalid email            |
| PATCH Partial Update | 5          | Single field, other fields unchanged, 404, invalid value    |
| DELETE Student       | 4          | Delete existing, 404, GET after delete, double delete       |
| Regression           | 5          | Persist after update, unique IDs, count change, 404/405     |
| **Total**            | **42**     |                                                             |

---

## Key Testing Scenarios

### Positive Tests
- Creating a student with all required fields returns `201` with a unique `id`
- Fetching a valid student ID returns all expected fields
- `PATCH` updates only the specified field; other fields remain unchanged
- `DELETE` removes the student; subsequent `GET` returns `404`

### Negative Tests
- `POST` with missing `name`, `email`, `age`, or `course` → `422`
- `POST` with invalid email format (`no-at-sign`) → `422`
- `POST` with age out of range (`-1`, `0`, `999`) → `422`
- `PUT`/`GET`/`DELETE` with non-existent ID → `404`
- Request to unknown endpoint → `404`
- `DELETE /api/students` (no ID) → `405 Method Not Allowed`

### Regression Tests
- `GET` after `PUT` reflects the updated data
- Two `POST` calls with the same payload generate different IDs
- Student count in `GET /api/students` correctly decrements after `DELETE`

---

## Sample Test Report

```
tests/test_students_api.py::TestHealthCheck::test_health_endpoint_returns_200 PASSED
tests/test_students_api.py::TestGetAllStudents::test_get_all_returns_200 PASSED
tests/test_students_api.py::TestCreateStudent::test_create_valid_student_returns_201 PASSED
tests/test_students_api.py::TestCreateStudent::test_create_student_invalid_email_returns_422 PASSED
tests/test_students_api.py::TestDeleteStudent::test_double_delete_returns_404 PASSED
tests/test_students_api.py::TestRegressionScenarios::test_total_count_decrements_after_delete PASSED

======================== 42 passed in 1.83s ========================
```

---

## Author

**Moin Khan**
BE Computer Science & Engineering
GitHub: [github.com/Moinkhan18](https://github.com/Moinkhan18)
LinkedIn: [linkedin.com/in/mohammad-moin-khan-036403223](https://linkedin.com/in/mohammad-moin-khan-036403223)
