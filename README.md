# Requirements
Create new Python virtual environment
```
python3 -m venv <env_name>
```

Start the virtual environment with
## Linux/MacOS
```
source <env_name>/bin/activate
```
## Windows
```
source <env_name>/Source/activate.bat  // For CMD
source <env_name>/Source/activate.ps1  // For Powershell
```

Install required libraries
```
python3 -m pip install -r requirements.txt
```

# Running
Run the service with
```
flask --app flaskr run --debug
```
In case port 5000 is already in use, run
```
flask --app flaskr run --debug --port <port>
``` 

# Testing
To run tests, run
```
cd tests
pytest
```

# Endpoints
## GET /search/<keyword>
### Request format
Replace `<keyword>` in endpoint URL with any keyword to search Git Hub for any related repositories.
If provided username and token, can access private repostitories as authorized by the provided token.
Additionally, you can `per_page` and `page` URL parameters after keyword:
`per_page` - specifies the number of shown repository data entries. Default: 30. Type: Integer.
`page` - chooses the page number of shown entries. Default: 1. Type: Integer.

### Response format
The endpoint returns JSON object with data from found repositories.
The JSON is formatted as such:
```
{
    "items: {
        "1": {
            "repo_name": Name of the found repository,
            "owner_login": Login of the owner of the repository,
            "repo_url": URL address to the repository
        }
    }
}
```
In case the search found no results, empty JSON is returned.

## POST /auth/login
### Request format
Takes JSON request body to save username and GitHub personal access token to session.
```
{
    "username": "<username>",
    "token": "<token>"
}
```
### Response format
Responds with Http 200: Ok with user provided username in case of success.
In case user is already logged in returns Http 403: Forbidden.

## GET /auth/user
### Response format
Returns username provided during login by the user.
If not logged in, informs about it.

## /auth/logout
### Response format
Deletes username and token from session.
Returns Http 200: OK.