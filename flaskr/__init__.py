from flask import Flask, json
from werkzeug.exceptions import HTTPException
from .exceptions import InvalidUserInputException

def create_app():
    """App entry point
    Main function serving as an entry point and configuration of the service.
    """
    
    app = Flask(__name__)
    app.config.from_mapping(
        #  Secret key used to protect data
        #  MUST BE OVERRIDDEN WITH RANDOM ONE FOR DEPLOYMENT
        SECRET_KEY='dev'
    )
    
    from . import auth
    app.register_blueprint(auth.bp)
    
    from . import search
    app.register_blueprint(search.bp)
    
    @app.errorhandler(InvalidUserInputException)
    def handle_invalid_keyword(e):
        """Invalid keyword exception handler
        """
        
        return e.to_dict()

    @app.errorhandler(HTTPException)
    def handle_generic_errors(e):
        """Generic error handler
        Returns JSON instead of HTML for HTTP error
        """
        response = e.get_response()
        response.data = json.dumps({
            "status_code": e.code,
            "name": e.name,
            "description": e.description
        })
        response.content_type = "application/json"
        return response
    
    return app