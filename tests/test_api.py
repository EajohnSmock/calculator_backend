import os

import pytest

from src.app import create_app


@pytest.fixture()
def client(tmp_path, monkeypatch):
    database_path = tmp_path / 'test.db'
    monkeypatch.setenv(
        'CALCULATOR_DB_PATH',
        str(database_path)
    )

    app = create_app()
    app.config.update(TESTING=True)

    with app.test_client() as test_client:
        yield test_client


def test_calculate_and_history(client):
    response = client.post(
        '/api/calculate',
        json={'expression': '(1+2)*3'}
    )

    assert response.status_code == 200
    assert response.get_json()['result'] == '9'

    history_response = client.get('/api/history')
    history = history_response.get_json()['history']

    assert len(history) == 1
    assert history[0]['expression'] == '(1+2)*3'
    assert history[0]['result'] == '9'


def test_delete_history(client):
    create_response = client.post(
        '/api/calculate',
        json={'expression': '5*8'}
    )
    record_id = create_response.get_json()['record']['id']

    delete_response = client.delete(
        f'/api/history/{record_id}'
    )

    assert delete_response.status_code == 200

    history_response = client.get('/api/history')
    assert history_response.get_json()['history'] == []
