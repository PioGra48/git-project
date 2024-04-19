import os
import json
import urllib.request as rq

from flask import Flask


def get_json(url: str) -> dict:
    """Reads url contents and returns them as JSON

    Args:
        url (str): url path 

    Returns:
        dict: JSON-format dictionary
    """
    
    page = rq.urlopen(url)
    content = page.read()
    
    return json.loads(content)


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY = 'dev'
    )
    
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    @app.route('/<owner>/<repo>')
    def getRepo(owner, repo):
        url = f'http://api.github.com/repos/{owner}/{repo}'
        contents_json = get_json(url)
        
        info_json = {}
        info_json["repo_name"] = contents_json["name"]
        info_json["owner_login"] = contents_json["owner"]["login"]
        info_json["repo_url"] = contents_json["html_url"]
        
        return info_json
    
    return app