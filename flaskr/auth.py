import json

from . import InvalidUserInputException
from flask import session, request, Response, Blueprint

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/login', methods=["POST"])
def login():
    """Logging in endpoint
    Endpoint used in logging in. Uses request body to get username and GitHub personal access token provided by the user.

    Raises:
        InvalidUserInputException: In case user is already logged in, return Http 403: Forbidden
    """
    
    #  Proceed if no user logged in
    #  Otherwise, return Http 403: Forbidden
    if "username" not in session:
        login_info = request.get_json()
        
        #  Check if necessery info was provided
        if "username" not in login_info or "token" not in login_info:
            raise InvalidUserInputException('Information missing.', statuscode=403)
        
        #  Save user info to session and return Http 200: OK
        session["username"] = login_info["username"]
        session["token"] = login_info["token"]
        return Response(response=json.dumps({"username": login_info["username"]}), status=200, mimetype='application/json', headers={"Location": '/auth/user'})
    else:
        raise InvalidUserInputException('User already logged in.', statuscode=403)

@bp.route('/user', methods=["GET"])
def get_user():
    """User endpoint
    Returns username provided during login.
    """
    if "username" in session:
        return {
            "username": session["username"]
        }
    else:
        return {
            "username": None
        }

@bp.route('/logout')
def logout():
    """Logout endpoint
    Deletes user info from session.
    """
    session.pop("username", None)
    session.pop("token", None)

    return Response({}, status=200)