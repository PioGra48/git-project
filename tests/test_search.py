import pytest

from flaskr.search import get_json


_gh_api_url = 'https://api.github.com/search/repositories?q='

def test_search(client):
    keyword = 'tetris'
    
    response = client.get(f'/search/{keyword}')
    gh_api_response_json = get_json(f'{_gh_api_url}{keyword}')
    
    assert response.json["total"] == gh_api_response_json["total_count"]
    assert response.json["items"]["0"]["repo_name"] == gh_api_response_json["items"][0]["name"]
