from http import HTTPStatus


def test_tags_status_code(fake_client):
    response = fake_client.get('/classificator/tags')
    assert response.status_code == HTTPStatus.OK


def test_tags_type(fake_client):
    response = fake_client.get('/classificator/tags')
    assert response.status_code == HTTPStatus.OK

    tags = response.json()['tags']
    assert isinstance(tags, list)


def test_predict_tags_type(fake_client, fake_image):
    response = fake_client.post('/classificator/predict', files={'image_file': fake_image})
    preds = response.json()['tags']
    assert isinstance(preds, list)


def test_predict_proba_status_code(fake_client, fake_image):
    response = fake_client.post('/classificator/predict_proba', files={'image_file': fake_image})
    probs = response.json()
    assert isinstance(probs, dict)


def test_predict_proba_between_zero_and_one(fake_client, fake_image):
    response = fake_client.post('/classificator/predict_proba', files={'image_file': fake_image})
    for tag, prob in response.json().items():
        prob = float(prob)
        assert prob <= 1
        assert prob >= 0


def test_healthcheck_status_code(fake_client):
    response = fake_client.get('/classificator/healthcheck')
    assert response.status_code == HTTPStatus.OK
