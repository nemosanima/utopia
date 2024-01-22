class Request:
    def __init__(self, environ):
        self.path = environ.get('PATH_INFO')
        self.method = environ.get('REQUEST_METHOD')
