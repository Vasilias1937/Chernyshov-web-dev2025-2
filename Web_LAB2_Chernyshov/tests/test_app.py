import pytest
from app.app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index_page_status(client):
    response = client.get('/')
    assert response.status_code == 200

def test_index_page_content(client):
    response = client.get('/')
    assert b'Welcome' in response.data

def test_form_page_status(client):
    response = client.get('/form')
    assert response.status_code == 200

def test_form_page_content(client):
    response = client.get('/form')
    assert b'Form' in response.data

def test_form_submission_valid(client):
    response = client.post('/submit', data={
        'name': 'Test User',
        'email': 'test@example.com',
        'message': 'Test message'
    })
    assert response.status_code == 200
    assert b'Test User' in response.data
    assert b'test@example.com' in response.data

def test_form_submission_invalid_email(client):
    response = client.post('/submit', data={
        'name': 'Test User',
        'email': 'invalid-email',
        'message': 'Test message'
    })
    assert response.status_code == 400

def test_form_submission_missing_fields(client):
    response = client.post('/submit', data={})
    assert response.status_code == 400

def test_form_validation(client):
    response = client.post('/validate', data={
        'field': 'test'
    })
    assert response.status_code == 200

def test_error_handling(client):
    response = client.get('/error')
    assert response.status_code == 404

def test_static_files(client):
    response = client.get('/static/css/style.css')
    assert response.status_code == 200

def test_headers(client):
    response = client.get('/')
    assert 'Content-Type' in response.headers
    assert 'text/html' in response.headers['Content-Type']

def test_cookies(client):
    response = client.get('/')
    assert 'Set-Cookie' in response.headers

def test_session(client):
    with client.session_transaction() as session:
        session['test'] = 'test_value'
    response = client.get('/')
    assert response.status_code == 200

def test_request_methods(client):
    response = client.get('/')
    assert response.status_code == 200
    response = client.post('/')
    assert response.status_code == 405  # Method Not Allowed

def test_query_parameters(client):
    response = client.get('/?param=value')
    assert response.status_code == 200 