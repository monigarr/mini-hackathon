from fastapi.testclient import TestClient

from src.main import app


def test_api_happy_path_download_and_observations() -> None:
    client = TestClient(app)

    created = client.post("/api/sessions")
    assert created.status_code == 200
    session_id = created.json()["session_id"]

    for message in (
        "Box 1 40000, Box 2 2400, Box 4 40000, Box 6 40000",
        "Single",
        "No, I am independent",
    ):
        response = client.post(
            "/api/chat", json={"session_id": session_id, "message": message}
        )
        assert response.status_code == 200
        assert response.json()["download_url"] is None

    done = client.post(
        "/api/chat", json={"session_id": session_id, "message": "Yes"}
    )
    assert done.status_code == 200
    assert done.json()["download_url"] == f"/api/download/{session_id}"

    pdf = client.get(f"/api/download/{session_id}")
    assert pdf.status_code == 200
    assert pdf.content.startswith(b"%PDF")

    observations = client.get(f"/api/observations/{session_id}")
    assert observations.status_code == 200
    event_types = {item["event_type"] for item in observations.json()["observations"]}
    assert "state_transition" in event_types
    assert "tool_execution_completed" in event_types

