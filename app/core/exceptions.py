class AppException(Exception):
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class NotFoundError(AppException):
    def __init__(self, message: str = "Resource not found"):
        super().__init__(message=message, status_code=404)


class ConflictError(AppException):
    def __init__(self, message: str = "Resource already exists"):
        super().__init__(message=message, status_code=409)


class UnauthorizedError(AppException):
    def __init__(self, message: str = "Invalid credentials"):
        super().__init__(message=message, status_code=401)


class ForbiddenError(AppException):
    def __init__(self, message: str = "Forbidden"):
        super().__init__(message=message, status_code=403)
