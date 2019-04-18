from flask import g, session

def test_validation(client, auth):
    # make sure user who accesses route is a teacher
    with client:
        auth.login()
        response = client.get('/sessions')
        assert b'<ul>' in response.data
    #if student accesses page, then bounce them back to home.
    with client:
        auth.login('student@stevenscollege.edu', 'asdfgh')
        response = client.get('/sessions')
        assert b'You are not permitted to view this page' in response.data
        # if student tries accessing sessions/1, then they aren't permitted to view page
        response = client.get('/sessions/1')
        assert b'You are not permitted to view this page' in response.data
        # if student tries accessing sessions/create, not permitted to view page
        response = client.get('/sessions/create')
        assert b'You are not permitted to view this page' in response.data

    # if teacher tries viewing sessions which doesn't belong to them, not permitted to view page


def test_session_route(client, auth):

    auth.login()
    assert client.get('/sessions').status_code == 200

    with client:
        response = client.get('/sessions/1')
        # represents the page which loaded, nice if result it's dynamic
        assert b'<p>A</p>' in response.data
        assert b'<p>2:00 - 4:20 MF</p>' in response.data

        # if you put in existing student, give success message and bounce back to session page
        response = client.post('/sessions/1', data=dict(
            student=2
        ))
        assert b'Student successfully added' in response.data

        # if you put in student who doesn't exist, bounce back to page and give error message
        response = client.post('/sessions/1', data=dict(
            student=2
        ))
        assert b'Student is already in this session' in response.data

    with client:
        response = client.get('/sessions/79')
        assert response.status_code == 404
        assert b'Session does not exist' in response.data


def test_session_create(client, auth):
    #page shows up when teacher is logged in
    auth.login()
    assert client.get('/sessions/create').status_code == 200
    #form shows up when route is acessed
    response = client.get('/sessions/create')
    assert b'<label>Session Letter:' in response.data
    response = client.post('/sessions/create', data=dict(
        session_letter='C',
        session_time='H'
    ))
    assert b'Session successfuly created' in response.data
