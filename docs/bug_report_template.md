# Bug Report Template – Student Management API

Use this template for every defect found during testing.

---

## BUG-001 – [Short descriptive title]

| Field             | Details                                  |
|-------------------|------------------------------------------|
| **Bug ID**        | BUG-001                                  |
| **Reported By**   | QA Tester                                |
| **Date**          | YYYY-MM-DD                               |
| **Severity**      | Critical / High / Medium / Low           |
| **Priority**      | P1 / P2 / P3                             |
| **Status**        | Open / In Progress / Resolved / Closed   |
| **Environment**   | Local / Dev / Staging                    |

### Endpoint
`METHOD /api/endpoint`

### Description
Brief description of the defect.

### Steps to Reproduce
1. Step one
2. Step two
3. Step three

### Expected Result
What should have happened.

### Actual Result
What actually happened.

### Request
```json
{
  "key": "value"
}
```

### Response (Actual)
```json
{
  "error": "unexpected"
}
```

### Expected Response
```json
{
  "success": true
}
```

### Screenshots / Postman Export
Attach screenshot or export .json from Postman.

### Notes
Any additional context, workaround, or related test case ID.

---

## Sample Filled Bug Report

## BUG-SAMPLE – POST /api/students returns 500 for age = 0 instead of 422

| Field             | Details                                  |
|-------------------|------------------------------------------|
| **Bug ID**        | BUG-SAMPLE                               |
| **Reported By**   | Moin Khan                                |
| **Date**          | 2024-06-01                               |
| **Severity**      | High                                     |
| **Priority**      | P2                                       |
| **Status**        | Open                                     |
| **Environment**   | Local (Flask dev server)                 |

### Endpoint
`POST /api/students`

### Description
When `age` is sent as `0`, the server responds with an unhandled 500 Internal Server Error instead of returning a 422 Validation Error.

### Steps to Reproduce
1. Send POST to `http://localhost:5000/api/students`
2. Body: `{ "name": "Test", "email": "t@t.com", "age": 0, "course": "CS" }`
3. Observe response

### Expected Result
`422 Unprocessable Entity` with validation error message.

### Actual Result
`500 Internal Server Error`

### Request
```json
{
  "name": "Test",
  "email": "t@t.com",
  "age": 0,
  "course": "CS"
}
```

### Expected Response
```json
{
  "error": "Validation failed.",
  "details": ["'age' must be an integer between 1 and 120."]
}
```

### Notes
Related to TC-004g. Validation condition uses `>= 1` but the check for `isinstance` may short-circuit incorrectly.
