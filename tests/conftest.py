#  Add path to the project to make flaskr module visible
import sys
sys.path.append('..')

import pytest

from flaskr import create_app


class AuthActions():
    def __init__(self, client):
        self._client = client
    
    def login(self, username='test', token='TEST_TOKEN'):
        return self._client.post(
            '/auth/loging',
            data = {
                "username": username,
                "token": token
            })
    
    def logout(self):
        return self._client.get('/auth/logout')


@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })
    
    yield app

@pytest.fixture
def client(app):
    return app.test_client()
    
@pytest.fixture
def auth(client):
    return AuthActions(client)