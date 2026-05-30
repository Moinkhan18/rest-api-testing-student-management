# Manual Test Cases – Student Management System REST API

## Test Environment
- **Base URL:** `http://localhost:5000`
- **Tool:** Postman
- **Date:** 2024

---

## TC-001 | GET /health – Health Check

| Field         | Details                      |
|---------------|------------------------------|
| Method        | GET                          |
| Endpoint      | `/health`                    |
| Auth          | None                         |
| Request Body  | None                         |

### Test Steps
1. Send GET request to `/health`

### Expected Results
| Step | Expected Status | Expected Response Body           |
|------|-----------------|----------------------------------|
| 1    | 200 OK          | `{ "status": "ok", "timestamp": "..." }` |

---

## TC-002 | GET /api/students – Fetch All Students

| Field         | Details                      |
|---------------|------------------------------|
| Method        | GET                          |
| Endpoint      | `/api/students`              |

### Test Scenarios

| TC ID   | Scenario                        | Input Params             | Expected Status | Expected Response                         |
|---------|---------------------------------|--------------------------|-----------------|-------------------------------------------|
| TC-002a | Fetch all students              | None                     | 200             | `{ count: N, students: [...] }`           |
| TC-002b | Filter by existing course       | `?course=Computer Science` | 200           | Students list where every item has matching course |
| TC-002c | Filter by nonexistent course    | `?course=Astrophysics`   | 200             | `{ count: 0, students: [] }`              |

---

## TC-003 | GET /api/students/:id – Fetch Single Student

| TC ID   | Scenario                    | Input              | Expected Status | Expected Response                    |
|---------|-----------------------------|--------------------|-----------------|--------------------------------------|
| TC-003a | Valid student ID            | `/api/students/1`  | 200             | Full student object with id=1        |
| TC-003b | Non-existent ID             | `/api/students/99999` | 404          | `{ "error": "..." }`                 |
| TC-003c | Verify all fields returned  | `/api/students/1`  | 200             | Has: id, name, email, age, course, grade, enrolled_at |

---

## TC-004 | POST /api/students – Create Student

| TC ID   | Scenario                       | Request Body                                               | Expected Status | Expected Response                  |
|---------|--------------------------------|------------------------------------------------------------|-----------------|------------------------------------|
| TC-004a | Valid payload                  | `{ name, email, age, course, grade }`                      | 201             | Created student with generated id  |
| TC-004b | Missing `name`                 | `{ email, age, course }`                                   | 422             | `{ error, details: [...] }`        |
| TC-004c | Missing `email`                | `{ name, age, course }`                                    | 422             | `{ error, details: [...] }`        |
| TC-004d | Missing `age`                  | `{ name, email, course }`                                  | 422             | `{ error, details: [...] }`        |
| TC-004e | Missing `course`               | `{ name, email, age }`                                     | 422             | `{ error, details: [...] }`        |
| TC-004f | Invalid email format           | `{ name, email: "bad", age, course }`                      | 422             | `{ error, details: [...] }`        |
| TC-004g | Age = 0                        | `{ name, email, age: 0, course }`                          | 422             | Validation error                   |
| TC-004h | Age = -1 (negative)            | `{ name, email, age: -1, course }`                         | 422             | Validation error                   |
| TC-004i | Age = 999 (too large)          | `{ name, email, age: 999, course }`                        | 422             | Validation error                   |
| TC-004j | Empty JSON body `{}`           | `{}`                                                       | 422             | Validation error                   |
| TC-004k | Non-JSON body                  | Plain text string                                          | 400             | `{ "error": "Request body must be valid JSON." }` |

---

## TC-005 | PUT /api/students/:id – Full Update

| TC ID   | Scenario                       | Input ID | Request Body                         | Expected Status | Expected Response          |
|---------|--------------------------------|----------|--------------------------------------|-----------------|----------------------------|
| TC-005a | Valid full update               | 1        | All required fields updated          | 200             | Updated student object     |
| TC-005b | Non-existent ID                 | 99999    | Valid full payload                   | 404             | `{ "error": "..." }`       |
| TC-005c | Missing required field          | 1        | `{ name: "Only" }`                   | 422             | Validation error           |
| TC-005d | Invalid email                   | 1        | `{ ..., email: "bad-format" }`       | 422             | Validation error           |
| TC-005e | Verify changes persist          | 1        | Updated name → GET /api/students/1   | 200             | GET reflects new name      |

---

## TC-006 | PATCH /api/students/:id – Partial Update

| TC ID   | Scenario                        | Input ID | Request Body              | Expected Status | Expected Response                  |
|---------|---------------------------------|----------|---------------------------|-----------------|------------------------------------|
| TC-006a | Update single field (grade)      | 1        | `{ grade: "A+" }`         | 200             | grade = "A+", other fields unchanged |
| TC-006b | Update single field (age)        | 1        | `{ age: 25 }`             | 200             | age = 25                           |
| TC-006c | Non-existent ID                  | 99999    | `{ grade: "B" }`          | 404             | `{ "error": "..." }`               |
| TC-006d | Invalid age in PATCH             | 1        | `{ age: 999 }`            | 422             | Validation error                   |
| TC-006e | Verify unmodified fields intact  | 1        | `{ grade: "C" }`          | 200             | email, name, course unchanged      |

---

## TC-007 | DELETE /api/students/:id – Delete Student

| TC ID   | Scenario                        | Input ID | Expected Status | Expected Response              |
|---------|---------------------------------|----------|-----------------|-------------------------------|
| TC-007a | Delete existing student          | (new)    | 200             | `{ "message": "... deleted" }` |
| TC-007b | Delete non-existent student      | 99999    | 404             | `{ "error": "..." }`           |
| TC-007c | GET after DELETE                 | (new)    | 404             | Student no longer found        |
| TC-007d | Double delete (idempotency)      | (new)    | 404 on 2nd      | Error on second attempt        |

---

## TC-008 | Regression Scenarios

| TC ID   | Scenario                                         | Steps                                       | Expected                                          |
|---------|--------------------------------------------------|---------------------------------------------|---------------------------------------------------|
| TC-008a | GET after PUT reflects updated data              | PUT student → GET same ID                   | GET response matches PUT payload                  |
| TC-008b | Two POST calls create unique IDs                 | POST student twice with same payload        | id fields differ between two responses            |
| TC-008c | Count decrements after DELETE                    | GET count → POST → GET count → DELETE → GET count | Count goes +1 then back to original        |
| TC-008d | Invalid endpoint returns 404                     | GET /api/nonexistent                        | 404 with error message                            |
| TC-008e | Method not allowed returns 405                   | DELETE /api/students (no ID)                | 405                                               |

---

## Test Summary Template

| Category            | Total | Passed | Failed | Blocked |
|---------------------|-------|--------|--------|---------|
| Health Check        | 3     |        |        |         |
| GET All Students    | 6     |        |        |         |
| GET Student by ID   | 3     |        |        |         |
| POST Create Student | 11    |        |        |         |
| PUT Full Update     | 5     |        |        |         |
| PATCH Partial Update| 5     |        |        |         |
| DELETE Student      | 4     |        |        |         |
| Regression          | 5     |        |        |         |
| **TOTAL**           | **42**|        |        |         |
