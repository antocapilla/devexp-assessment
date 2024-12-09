class SinchError(Exception):
    """Base exception for all Sinch errors."""
    pass

class AuthenticationError(SinchError):
    """Raised when authentication fails."""
    pass

class NotFoundError(SinchError):
    """Raised when a resource is not found."""
    pass

class ValidationError(SinchError):
    """Raised when request validation fails."""
    pass