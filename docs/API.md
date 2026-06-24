# API Reference

Base URL for local development:

```text
http://127.0.0.1:8000
```

## `GET /health`

Returns app health.

Response:

```json
{
  "status": "healthy",
  "version": "1.0.0"
}
```

## `POST /api/sessions`

Creates a new in-memory conversation session and returns the first agent question.

Response:

```json
{
  "session_id": "abc123",
  "message": "Hi, I can help...",
  "question_count": 1,
  "state": "awaiting_w2"
}
```

## `POST /api/chat`

Processes one user message.

Request:

```json
{
  "session_id": "abc123",
  "message": "Box 1 40000, Box 2 2400, Box 4 40000, Box 6 40000"
}
```

Response:

```json
{
  "session_id": "abc123",
  "message": "Question 2 of 5: are you filing as Single or Married Filing Jointly?",
  "question_count": 2,
  "state": "awaiting_filing_status",
  "download_url": null
}
```

When complete, `download_url` is populated:

```json
{
  "session_id": "abc123",
  "message": "Your draft 2025 Form 1040 is ready...",
  "question_count": 4,
  "state": "complete",
  "download_url": "/api/download/abc123"
}
```

## `GET /api/download/{session_id}`

Downloads the generated PDF for a completed session.

Response:

- `200 OK`
- `Content-Type: application/pdf`
- `Content-Disposition: attachment; filename="Form_1040_{session_id}.pdf"`

## `GET /api/observations/{session_id}`

Returns structured observation events for judge review.

Response:

```json
{
  "session_id": "abc123",
  "observations": [
    {
      "timestamp": "2026-06-24T20:00:00+00:00",
      "session_id": "abc123",
      "event_type": "state_transition",
      "state": "awaiting_w2",
      "question_count": 0,
      "event_data": {
        "from": "start",
        "to": "awaiting_w2"
      }
    }
  ]
}
```

