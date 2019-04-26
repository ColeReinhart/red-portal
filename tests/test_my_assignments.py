def test_validation_my_assignments(client, auth):
    with client:
        response = client.get('/my_assignments/2')
        assert response.headers['Location'] == 'http://localhost/'
    with client:
        auth.login("student_2@stevenscollege.edu", "x")
        response = client.get('/my_assignments/2')
        assert response.status_code == 401
        assert b'You are not permitted to view this page' in response.data
    with client:
        auth.login()
        response = client.get('/my_assignments/2')
        assert response.status_code == 401
        assert b'You are not permitted to view this page' in response.data
    with client:
        auth.login('student@stevenscollege.edu','asdfgh')
        response = client.get('/my_assignments/2')
        assert response.status_code == 200
        assert b'CSET 155B' in response.data
