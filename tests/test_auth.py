from flask import g, session

def test_index(client):
    response = client.get('/')
    assert b'<h1>TSCT Portal</h1>' in response.data
    assert b'<form method="post">' in response.data

def test_login(client, auth):
    assert client.get('/').status_code == 200

    # asserts that we go back to index if login fails
    with client:
        response = auth.login('dd','dd')
        assert 'user_id' not in session
        assert g.user == None

    # assert that correct login works
    with client:
        response = auth.login()
        assert response.headers['Location'] == 'http://localhost/home'
        assert session['user_id'] == 1
        client.get('/home')
        assert g.user[0] == 1

def test_logout(client, auth):
    # once logged in, check if logout works
    with client:
        response = auth.login()
        response = client.get('/home')
        response = client.get('/logout')
        assert response.headers['Location'] == 'http://localhost/'
        assert 'user_id' not in session
        client.get('/')
        assert g.user == None
