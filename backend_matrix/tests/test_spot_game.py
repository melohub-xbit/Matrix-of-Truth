import pytest
from main import app

def test_get_pair():
    client = app.test_client()
    response = client.get('/api/spot-game/pair')
    assert response.status_code == 200
    data = response.get_json()
    assert 'id' in data
    assert 'items' in data
    assert len(data['items']) == 2

def test_submit_vote():
    client = app.test_client()
    response = client.post('/api/spot-game/vote', 
                         json={'pair_id': 'pair-001', 'choice': 0})
    assert response.status_code == 200