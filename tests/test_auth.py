import pytest

_user_info = {
        "username": "user123",
        "token": "user123-token-456"
    }

def test_login(client):
    response = client.post('/auth/login', json=_user_info)        

    assert response.status_code == 200
    assert response.headers["Location"] == '/auth/user'
    assert response.json["username"] == _user_info["username"]
    with client.session_transaction() as session:
        assert session["username"] == _user_info["username"]
        assert session["token"] == _user_info["token"]

def test_login_username_missing(client):
    response = client.post('/auth/login', json={"token": _user_info["token"]})
    
    assert response.status_code == 403

def test_login_token_missing(client):
    response = client.post('/auth/login', json={"username": _user_info["username"]})
    
    assert response.status_code == 403
    
def test_get_user_not_logged_in(client):
    response = client.get('/auth/user')
    
    assert response.status_code == 200
    assert response.json["username"] == None

def test_get_user_logged_in(client):
    post_response = client.post('/auth/login', json=_user_info)
    
    assert post_response.status_code == 200
    
    get_response = client.get('/auth/user')
    
    assert get_response.status_code == 200
    assert get_response.json["username"] == _user_info["username"]
    with client.session_transaction() as session:
        assert session["username"] == _user_info["username"]
        assert session["token"] == _user_info["token"]

def test_logout(client):
    response = client.get('/auth/logout')
    
    assert response.status_code == 200
    with client.session_transaction() as session:
        assert "username" not in session
        assert "token" not in session

    