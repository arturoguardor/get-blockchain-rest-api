import pytest
import json
from app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_welcome(client):
    rv = client.get('/')
    assert b'Welcome to my Blockchain API' in rv.data


def test_l3(client):
    # Realiza una solicitud GET a la ruta '/l3/'
    response = client.get('/l3/')

    # Verifica que el código de estado de la respuesta sea 200 (OK)
    assert response.status_code == 200


def test_get_symbol_asks():
    response = app.test_client().get('/l3/BTC-USD/asks/')
    assert response.status_code == 200
    assert response.content_type == 'application/json'


def test_get_symbol():
    response = app.test_client().get('/l3/BTC-USD/')
    assert response.status_code == 200
    assert response.content_type == 'application/json'


def test_get_symbol_bids_success(client):
    response = client.get('/l3/btc-usd/bids/')
    data = json.loads(response.data)

    assert response.status_code == 200
    assert 'average_value' in data['bids']
    assert 'greater_value' in data['bids']
    assert 'lesser_value' in data['bids']
    assert 'total_qty' in data['bids']
    assert 'total_px' in data['bids']


def test_valid_symbol(client):
    response = client.get('/l3/BTC-USD/asks/')
    assert response.status_code == 200


if __name__ == "__main__":
    pytest.main()
