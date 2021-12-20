class User:
    def __init__(self, role, id, socket):
        self.role = role
        self.id = id
        self.socket=socket

    def update(self, callback) -> bool:
        callback()
        return True
