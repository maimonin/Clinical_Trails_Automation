class Test:
    def __init__(self, name, duration, instructions, staff):
        self.name = name
        self.duration = duration
        self.instructions = instructions
        self.staff = staff

    def to_json(self):
        return {'name': self.name, 'instructions': self.instructions, 'staff': self.staff, 'duration': self.duration}