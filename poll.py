from typing import List


class Poll:
    def __init__(self, question: str, options: List[str], username: str):
        self.question = question
        self.options = options
        self.votes = [0] * len(options)
        self.user = username
        self.users = []