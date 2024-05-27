from .match import Match

class Round:
    def __init__(self, matches):
        self.matches = matches

    def to_dict(self):
        return [match.to_dict() for match in self.matches]
