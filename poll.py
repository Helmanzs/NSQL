from typing import List


class Poll:
    def __init__(self, question: str, options: List[str], user: str, users: List[str]):
        self.question = question
        self.options = options
        self.votes = [0] * len(options)
        self.user = user
        self.users = users