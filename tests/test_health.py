from fastapi.testclient import TestClient

from app.main import app


def test_health_endpoint_has_runtime_flags():
    with TestClient(app) as client:
        response = client.get('/health')

    assert response.status_code == 200
    payload = response.json()
    assert 'scheduler_running' in payload
    assert 'facebook_configured' in payload
