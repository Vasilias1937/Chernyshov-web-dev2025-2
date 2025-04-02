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

def test_post_detail_template(client, captured_templates, mocker, posts_list):
    with captured_templates as templates:
        mocker.patch(
            "app.posts_list",
            return_value=posts_list,
            autospec=True
        )
        
        _ = client.get('/posts/0')
        assert len(templates) == 1
        template, context = templates[0]
        assert template.name == 'post.html'
        assert context['title'] == 'Заголовок поста'
        assert 'post' in context

def test_post_detail_data(client, mocker, posts_list):
    mocker.patch(
        "app.posts_list",
        return_value=posts_list,
        autospec=True
    )
    
    response = client.get('/posts/0')
    assert response.status_code == 200
    # Проверяем наличие данных поста
    assert posts_list[0]['title'] in response.text
    assert posts_list[0]['author'] in response.text
    assert posts_list[0]['text'] in response.text

def test_post_detail_date_format(client, mocker, posts_list):
    mocker.patch(
        "app.posts_list",
        return_value=posts_list,
        autospec=True
    )
    
    response = client.get('/posts/0')
    assert response.status_code == 200
    # Проверяем формат даты
    formatted_date = posts_list[0]['date'].strftime('%d.%m.%Y')
    assert formatted_date in response.text

def test_post_detail_image(client, mocker, posts_list):
    mocker.patch(
        "app.posts_list",
        return_value=posts_list,
        autospec=True
    )
    
    response = client.get('/posts/0')
    assert response.status_code == 200
    # Проверяем наличие изображения
    assert posts_list[0]['image_id'] in response.text

def test_post_detail_comment_form(client, mocker, posts_list):
    mocker.patch(
        "app.posts_list",
        return_value=posts_list,
        autospec=True
    )
    
    response = client.get('/posts/0')
    assert response.status_code == 200
    # Проверяем наличие формы комментария
    assert "Оставьте комментарий" in response.text
    assert '<textarea class="form-control"' in response.text
    assert '<button type="submit" class="btn btn-primary">Отправить</button>' in response.text

def test_post_detail_comments_section(client, mocker, posts_list):
    # Добавляем комментарии к посту для теста
    posts_list[0]['comments'] = [
        {
            'author': 'Тестовый автор',
            'text': 'Тестовый комментарий',
            'replies': []
        }
    ]
    
    mocker.patch(
        "app.posts_list",
        return_value=posts_list,
        autospec=True
    )
    
    response = client.get('/posts/0')
    assert response.status_code == 200
    # Проверяем наличие секции комментариев
    assert "Комментарии:" in response.text
    assert "Тестовый автор" in response.text
    assert "Тестовый комментарий" in response.text

def test_post_detail_comment_replies(client, mocker, posts_list):
    # Добавляем комментарии с ответами к посту для теста
    posts_list[0]['comments'] = [
        {
            'author': 'Тестовый автор',
            'text': 'Тестовый комментарий',
            'replies': [
                {
                    'author': 'Автор ответа',
                    'text': 'Тестовый ответ'
                }
            ]
        }
    ]
    
    mocker.patch(
        "app.posts_list",
        return_value=posts_list,
        autospec=True
    )
    
    response = client.get('/posts/0')
    assert response.status_code == 200
    # Проверяем наличие ответов на комментарии
    assert "Автор ответа" in response.text
    assert "Тестовый ответ" in response.text

def test_post_detail_no_comments(client, mocker, posts_list):
    # Пост без комментариев для теста
    posts_list[0]['comments'] = []
    
    mocker.patch(
        "app.posts_list",
        return_value=posts_list,
        autospec=True
    )
    
    response = client.get('/posts/0')
    assert response.status_code == 200
    # Проверяем сообщение об отсутствии комментариев
    assert "Пока нет комментариев. Будьте первым!" in response.text

def test_post_detail_nonexistent_index(client, mocker, posts_list):
    mocker.patch(
        "app.posts_list",
        return_value=posts_list,
        autospec=True
    )
    
    # Запрос к несуществующему индексу поста
    response = client.get('/posts/999')
    # Проверяем ответ 404
    assert response.status_code == 404

def test_post_index_link_in_posts_list(client, mocker, posts_list):
    mocker.patch(
        "app.posts_list",
        return_value=posts_list,
        autospec=True
    )
    
    response = client.get('/posts')
    assert response.status_code == 200
    # Проверяем наличие ссылки на пост с правильным индексом
    assert '/posts/0' in response.text

def test_post_detail_header_footer(client, mocker, posts_list):
    mocker.patch(
        "app.posts_list",
        return_value=posts_list,
        autospec=True
    )
    
    response = client.get('/posts/0')
    assert response.status_code == 200
    # Проверяем наличие шапки и подвала
    assert 'navbar' in response.text
    assert 'Чернышов Артур Александрович, группа 231-329' in response.text

def test_post_detail_navigation(client, mocker, posts_list):
    mocker.patch(
        "app.posts_list",
        return_value=posts_list,
        autospec=True
    )
    
    response = client.get('/posts/0')
    assert response.status_code == 200
    # Проверяем наличие ссылок навигации
    assert 'href="/posts"' in response.text
    assert 'href="/about"' in response.text
    assert 'href="/"' in response.text
