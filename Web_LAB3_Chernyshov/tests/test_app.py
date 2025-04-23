import pytest
from app.app import app
from flask_login import login_user
from app.app import User

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    with app.test_client() as client:
        yield client

def test_index_page_status(client):
    response = client.get('/')
    assert response.status_code == 200

def test_index_page_content(client):
    response = client.get('/')
    assert b'Welcome' in response.data

def test_visits_counter_status(client):
    response = client.get('/visits')
    assert response.status_code == 200

def test_visits_counter_increment(client):
    initial_response = client.get('/visits')
    initial_visits = int(initial_response.data.split(b'visits: ')[1].split(b'<')[0])
    
    response = client.get('/visits')
    new_visits = int(response.data.split(b'visits: ')[1].split(b'<')[0])
    
    assert new_visits == initial_visits + 1

def test_login_page_status(client):
    response = client.get('/login')
    assert response.status_code == 200

def test_login_page_content(client):
    response = client.get('/login')
    assert b'Login' in response.data

def test_successful_login(client):
    response = client.post('/login', data={
        'username': 'user',
        'password': 'qwerty'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Success' in response.data

def test_failed_login(client):
    response = client.post('/login', data={
        'username': 'wrong',
        'password': 'wrong'
    })
    assert response.status_code == 200
    assert b'Invalid' in response.data

def test_secret_page_unauthorized(client):
    response = client.get('/secret')
    assert response.status_code == 302  # Redirect to login

def test_secret_page_authorized(client):
    with client:
        user = User('user')
        login_user(user)
        response = client.get('/secret')
        assert response.status_code == 200
        assert b'Secret' in response.data 