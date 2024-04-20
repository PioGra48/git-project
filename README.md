# Requirements
Create new Python virtual environment
```
python3 -m venv <env_name>
```

Start the virtual environment with
```
source <env_name>/bin/activate
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

# Use
## Request format
The service consists of one GET endpoint on `/search/<keyword>`.
Replace `<keyword>` in endpoint URL with any keyword to search Git Hub for any related repositories.
Additionally, you can `per_page` and `page` URL parameters after keyword:
`per_page` - specifies the number of shown repository data entries. Default: 30. Type: Integer.
`page` - chooses the page number of shown entries. Default: 1. Type: Integer.

## Response format
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