from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_create_todo():
    response = client.post('/todo/create', json={"id": 1,
                                                 "content": "test",
                                                 "is_done": False,
                                                 "created_at": "2022-07-27T16:00:58",
                                                 "updated_at": "2022-07-27T16:00:58"})
    assert response.status_code == 200, response.text
    data = response.json()
    assert data['content'] == 'test'
    assert 'id' in data
    todo_id = data['id']

    response = client.get(f'/todo/get/{todo_id}')
    assert response.status_code == 200, response.text
    data = response.json()
    assert data['content'] == 'test'
    assert data['id'] == todo_id


def test_get_all():
    response = client.get('/todo/all')
    assert response.status_code == 200, response.text


def test_put_content():
    response = client.get(f'/todo/get/{1}')
    assert response.status_code == 200, response.text
    data_before = response.json()
    assert data_before['content'] == 'test'

    response = client.put(f'/todo/change_content/{1}', json={"id": 1,
                                                             "content": "test",
                                                             "is_done": False,
                                                             "created_at": "2022-07-27T16:00:58",
                                                             "updated_at": "2022-07-27T16:00:58"})
    assert response.status_code == 200, response.text
    data_after = response.json()
    assert data_after['content'] == 'changed'
    assert data_before != data_after


def test_delete_todo():
    response = client.delete(f'/todo/delete/{1}')
    assert response.status_code == 200
    assert response.content == 'null'





