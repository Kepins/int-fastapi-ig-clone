class ServiceError(Exception):
    pass


class AlreadyExists(Exception):
    pass


class NotFound(Exception):
    pass


class PasswordNotMatching(Exception):
    pass


class NotResourceOwner(Exception):
    pass
