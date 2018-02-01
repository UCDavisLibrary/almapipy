"""
Error classes and other helpful functions
"""


class Error(Exception):
    """Base class for exceptions"""
    pass


class AlmaError(Error):
    """
    Base Exception class for Alma API calls
    """

    def __init__(self, message, response=None, url=None):
        super(AlmaError, self).__init__(message)
        self.message = message
        self.response = response
        self.url = url


class ArgError(Error):
    def __init__(self, message):
        super(ArgError, self).__init__(message)
        self.message = "Invalid Argument: " + message
