import os
import json
import urllib.request as rq
 
from flask import Flask, request
from werkzeug.exceptions import HTTPException


#  URI reserved characters, user's keyword cannot contain them unencoded
RESERVED = ('!', '#', '$', '&', "'", '(', ')', '*', '+', ',', '/', ':', ';', '=', '?', '@', '[', ']')


def get_json(url: str) -> dict:
    """Reads url contents and returns them as JSON

    Args:
        url (str): URL path 

    Returns:
        dict: JSON-format dictionary
    """
    
    request_url = rq.urlopen(url)
    
    response = request_url.read()
    
    #  convert page content from string to JSON
    return json.loads(response)
    

class InvalidUserInputException(Exception):
    """Exception raised in cases of invalid user input
    """
    
    def __init__(self, message, payload=None):
        """Initializes the exception
        Initializes the exception with custom message, HTTP Status 400: Bad Request due to user error
        """
        
        super().__init__()
        self.message = message
        self.status_code = 400
        self.payload = payload
    
    def to_dict(self):
        """ Converts the exception to dict
        Converts the exception to JSON-formatted dictionary
        """
        
        ed = dict(self.payload or ())
        
        ed["status_code"] = self.status_code
        ed["name"] = "Bad request"
        ed["message"] = self.message
        
        return ed


def create_app():
    """App entry point
    Main function serving as an entry point and configuration of the service.
    """
    
    app = Flask(__name__)

    @app.route('/search/<keyword>')
    def findByKeyword(keyword: str) -> dict:
        """ Keyword based repository search
        Uses user specified keyword to search GitHub repositories and returns their name, URL and their owner's login.

        Args:
            keyword (str): User specified search keyword

        URL params:
            per_page: Items shown per page. Defaults to 30.
            page: Page number of the results. Defaults to 1.
        
        Raises:
            InvalidKeywordException: Exception raised in case of keyword containing URI reserved characters

        Returns:
            dict: JSON-formatted dictionary containing found repositories' info
        """
        
        #  Get raw query string for keyword testing
        raw_query = request.query_string.decode()
        
        #  Extract keyword from raw query
        raw_keyword = raw_query[: raw_query.find('?')]
        
        #  Check if keyword was cut early by reserved character
        #  If cut, raise exception
        #  In some cases, reserved character can cut keyword early, but not show up in keyword
        #  Comparision to its raw form helps prevent those
        if keyword != raw_keyword:
            raise InvalidUserInputException('Keyword contains unencoded URI reserved character(s)')
        
        #  Check for any unencoded URI reserved characters in keyword.
        #  If found raise exception
        if any(char in keyword for char in RESERVED):
            raise InvalidUserInputException('Keyword contains unencoded URI reserved character(s)')
        
        #  Default number of items shown per page
        items_per_page = 30
        
        #  In case of user specified number, update number of items per page
        per_page_arg = request.args.get('per_page')
        if per_page_arg is not None:
            #  Check if user "per_page" argument is an integer
            #  If not, raise exception
            try:
                int(per_page_arg)
            except:
                raise InvalidUserInputException('Invalid "per_page" argument value.')
            items_per_page = per_page_arg
        
        #  Default page number
        page_number = 1
        #  In case of user specified page number, update page number
        page_arg = request.args.get('page')
        if page_arg is not None:
            #  Check if user "page" argument is an integer
            #  If not, raise exception
            try:
                int(page_arg)
            except:
                raise InvalidUserInputException('Invalid "page" argument value.')
        page_number = page_arg
        
        #  URL connecting to GitHub API repositories search endpoint
        #  URL formatted according to user input
        url = f'https://api.github.com/search/repositories?q={keyword}&page={page_number}&per_page={items_per_page}'
        response = get_json(url)
        
        #  Create new JSON-formatted dictionary storing the repository data
        repos_data = {
            "items": {}
        }
        
        #  Iterate over search results and save the repository data
        for i, repo in enumerate(response["items"]):
            repo_data = {}
            
            repo_data["repo_name"] = repo["name"]
            repo_data["owner_login"] = repo["owner"]["login"]
            repo_data["repo_url"] = repo["html_url"]
            
            repos_data["items"][f"{i}"] = repo_data
        
        return repos_data
    
    @app.errorhandler(InvalidUserInputException)
    def handle_invalid_keyword(e):
        """Invalid keyword exception handler
        """
        
        return e.to_dict()
    
    @app.errorhandler(HTTPException)
    def handle_generic_errors(e):
        """Generic error handler
        """
        response = e.get_response()
        response.data = {
            "status_code": e.code,
            "name": e.name,
            "description": e.description
        }
        response.content_type = "application/json"
        
        return response
    
    return app