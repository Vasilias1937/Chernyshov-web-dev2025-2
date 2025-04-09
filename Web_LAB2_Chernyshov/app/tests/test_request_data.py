import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_url_params_page(client):
    response = client.get('/request-data/url-params?test=123&param=value')
    assert response.status_code == 200
    assert 'test' in response.text
    assert '123' in response.text
    assert 'param' in response.text
    assert 'value' in response.text

def test_headers_page(client):
    response = client.get('/request-data/headers')
    assert response.status_code == 200
    assert 'User-Agent' in response.text
    assert 'Host' in response.text

def test_cookies_page_set_cookie(client):
    response = client.get('/request-data/cookies')
    assert response.status_code == 200
    assert 'test_cookie' in response.text
    assert 'test_value' in response.text

def test_cookies_page_delete_cookie(client):
    # Сначала устанавливаем cookie
    client.get('/request-data/cookies')
    # Затем удаляем её
    response = client.get('/request-data/cookies')
    assert response.status_code == 200
    assert 'test_cookie' not in response.text

def test_form_page_get(client):
    response = client.get('/request-data/form')
    assert response.status_code == 200
    assert 'name' in response.text
    assert 'email' in response.text
    assert 'message' in response.text

def test_form_page_post(client):
    data = {
        'name': 'Test User',
        'email': 'test@example.com',
        'message': 'Test message'
    }
    response = client.post('/request-data/form', data=data)
    assert response.status_code == 200
    assert 'Test User' in response.text
    assert 'test@example.com' in response.text
    assert 'Test message' in response.text

def test_phone_validation_page_get(client):
    response = client.get('/phone-validation')
    assert response.status_code == 200
    assert 'Номер телефона' in response.text

def test_phone_validation_valid_number(client):
    valid_numbers = [
        '+7 (123) 456-75-90',
        '8(123)4567590',
        '123.456.75.90'
    ]
    for number in valid_numbers:
        response = client.post('/phone-validation', data={'phone': number})
        assert response.status_code == 200
        assert 'is-invalid' not in response.text
        assert '8-123-456-75-90' in response.text

def test_phone_validation_invalid_length(client):
    invalid_numbers = [
        '+7 (123) 456-75-9',  # 9 цифр
        '8(123)45675901',     # 12 цифр
        '123.456.75.9'        # 9 цифр
    ]
    for number in invalid_numbers:
        response = client.post('/phone-validation', data={'phone': number})
        assert response.status_code == 200
        assert 'is-invalid' in response.text
        assert 'Неверное количество цифр' in response.text

def test_phone_validation_invalid_characters(client):
    invalid_numbers = [
        '+7 (123) 456-75-90!',
        '8(123)4567590#',
        '123.456.75.90@'
    ]
    for number in invalid_numbers:
        response = client.post('/phone-validation', data={'phone': number})
        assert response.status_code == 200
        assert 'is-invalid' in response.text
        assert 'недопустимые символы' in response.text

def test_phone_validation_empty_input(client):
    response = client.post('/phone-validation', data={'phone': ''})
    assert response.status_code == 200
    assert 'is-invalid' in response.text

def test_phone_validation_formatting(client):
    test_cases = [
        ('+7 (123) 456-75-90', '8-123-456-75-90'),
        ('8(123)4567590', '8-123-456-75-90'),
        ('123.456.75.90', '8-123-456-75-90')
    ]
    for input_number, expected_output in test_cases:
        response = client.post('/phone-validation', data={'phone': input_number})
        assert response.status_code == 200
        assert expected_output in response.text

def test_phone_validation_error_classes(client):
    response = client.post('/phone-validation', data={'phone': 'invalid'})
    assert response.status_code == 200
    assert 'is-invalid' in response.text
    assert 'invalid-feedback' in response.text

def test_phone_validation_success_classes(client):
    response = client.post('/phone-validation', data={'phone': '+7 (123) 456-75-90'})
    assert response.status_code == 200
    assert 'is-invalid' not in response.text
    assert 'invalid-feedback' not in response.text 