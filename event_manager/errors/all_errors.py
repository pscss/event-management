class BaseEventError(Exception):
    def __init__(self, code: int = 400, message: str = "Bad Input"):
        self.code = code
        self.message = message


class InsufficientTickets(BaseEventError):
    def __init__(self):
        super().__init__(code=400, message="Insufficient Tickets")


class ResourceNotFound(BaseEventError):
    def __init__(self, message: str):
        super().__init__(code=400, message=message)
