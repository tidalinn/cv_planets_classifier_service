from http import HTTPStatus


def test_metrics_status_code(fake_client):
    response = fake_client.get('/metrics')
    assert response.status_code == HTTPStatus.OK


def test_metrics_contains_custom_metrics(fake_client):
    response = fake_client.get('/metrics')
    assert response.status_code == HTTPStatus.OK
    assert b'app_request_count' in response.content
    assert b'app_request_latency_seconds' in response.content
