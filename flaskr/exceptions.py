class InvalidUserInputException(Exception):
    """Exception raised in cases of invalid user input
    """
    
    def __init__(self, message, statuscode=400, payload=None):
        """Initializes the exception
        Initializes the exception with custom message and status code defaulting to HTTP Status 400: Bad Request due to user error
        """
        
        super().__init__()
        self.message = message
        self.status_code = statuscode
        self.payload = payload
    
    def to_dict(self):
        """ Converts the exception to dict
        Converts the exception to JSON-formatted dictionary
        """
        
        ed = dict(self.payload or ())
        
        ed["status_code"] = self.status_code
        match self.status_code:
            case 400:
                ed["name"] = "Bad request"
            case 403:
                ed["name"] = "Forbidden"
        ed["message"] = self.message
        
        return ed