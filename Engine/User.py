class User:
    def __init__(self, role):
        self.role = role

    def update(self, callback) -> None:
        callback()