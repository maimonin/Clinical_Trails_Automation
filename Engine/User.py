class User:
    def __init__(self, role, id):
        self.role = role
        self.id = id

    def update(self, callback) -> bool:
        callback()
        return True
