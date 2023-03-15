"""

    Exceptions

"""


class ConvexBaseError(Exception):
    def __init__(self, source: str, code: str, text: str):
        self.source = source
        self.code = code
        self.text = text

    def __str__(self):
        return f'{self.source}: {self.code} {self.text}'


class ConvexAPIError(ConvexBaseError):
    """ Raised when a request error occurs """


class ConvexRequestError(ConvexBaseError):
    """ Raised when a error-code is returned from a web call """
