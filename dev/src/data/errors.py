class RepositoryNotConnected(Exception):
    pass


class RepositoryDuplicateKeyError(Exception):
    def __init__(self, handle: str):
        self.handle = handle


class RepositoryNotFoundError(Exception):
    def __init__(self, handle: str):
        self.handle = handle
