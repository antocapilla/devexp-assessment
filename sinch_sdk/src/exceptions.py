class MessagingException(Exception):
    pass

class BadRequestError(MessagingException):
    pass

class UnauthorizedError(MessagingException):
    pass

class NotFoundError(MessagingException):
    pass