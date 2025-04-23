import pytest
from app import app
from datetime import datetime

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_post_page_status(client):
    """Тест статуса страницы поста"""
    response = client.get('/posts/0')
    assert response.status_code == 200

def test_post_page_template(client):
    """Тест использования правильного шаблона"""
    response = client.get('/posts/0')
    assert b'blog-post' in response.data

def test_post_title_present(client):
    """Тест наличия заголовка поста"""
    response = client.get('/posts/0')
    assert b'title' in response.data

def test_post_author_present(client):
    """Тест наличия автора поста"""
    response = client.get('/posts/0')
    assert b'author' in response.data

def test_post_date_format(client):
    """Тест формата даты"""
    response = client.get('/posts/0')
    date_format = datetime.now().strftime('%d.%m.%Y')
    assert bytes(date_format.encode()) in response.data

def test_post_content_present(client):
    """Тест наличия текста поста"""
    response = client.get('/posts/0')
    assert b'text' in response.data

def test_post_image_present(client):
    """Тест наличия изображения"""
    response = client.get('/posts/0')
    assert b'img' in response.data

def test_post_comments_section_present(client):
    """Тест наличия секции комментариев"""
    response = client.get('/posts/0')
    assert b'comments' in response.data

def test_post_comment_form_present(client):
    """Тест наличия формы комментариев"""
    response = client.get('/posts/0')
    assert b'comment-form' in response.data

def test_post_comments_list_present(client):
    """Тест наличия списка комментариев"""
    response = client.get('/posts/0')
    assert b'comments-list' in response.data

def test_post_comment_author_present(client):
    """Тест наличия автора комментария"""
    response = client.get('/posts/0')
    assert b'comment' and b'author' in response.data

def test_post_comment_text_present(client):
    """Тест наличия текста комментария"""
    response = client.get('/posts/0')
    assert b'comment' and b'text' in response.data

def test_post_replies_present(client):
    """Тест наличия ответов на комментарии"""
    response = client.get('/posts/0')
    assert b'replies' in response.data

def test_nonexistent_post(client):
    """Тест обработки несуществующего поста"""
    response = client.get('/posts/999')
    assert response.status_code == 404

def test_footer_content(client):
    """Тест содержимого футера"""
    response = client.get('/posts/0')
    assert b'Чернышов Артур Александрович' in response.data
    assert b'221-322' in response.data

def test_posts_index(client):
    response = client.get("/posts")
    assert response.status_code == 200
    assert "Последние посты" in response.text

def test_posts_index_template(client, captured_templates, mocker, posts_list):
    with captured_templates as templates:
        mocker.patch(
            "app.posts_list",
            return_value=posts_list,
            autospec=True
        )
        
        _ = client.get('/posts')
        assert len(templates) == 1
        template, context = templates[0]
        assert template.name == 'posts.html'
        assert context['title'] == 'Посты'
        assert len(context['posts']) == 1
