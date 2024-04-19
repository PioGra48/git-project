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

    @app.route('/search/<keyword>')
    def findByKeyword(keyword):
        url = f'https://api.github.com/search/repositories?q={keyword}'
        contents_json = get_json(url)
        
        info_json = {
            "items": {}
        }
        for i, item in enumerate(contents_json["items"]):
            item_info_dict = {}
            
            item_info_dict["repo_name"] = item["name"]
            item_info_dict["owner_login"] = item["owner"]["login"]
            item_info_dict["repo_url"] = item["html_url"]
            
            info_json["items"][f"{i}"] = item_info_dict
            
        return info_json
    
    return app