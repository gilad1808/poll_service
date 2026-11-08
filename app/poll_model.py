
class Poll:
    def __init__(self, id: int, question: str):
        self.id = id
        self.question = question


class PollOption:
    def __init__(self, id: int, poll_id: int, option_text: str):
        self.id = id
        self.poll_id = poll_id
        self.option_text = option_text


class Vote:
    def __init__(self, id: int, poll_id: int, option_id: int, user_id: int):
        self.id = id
        self.poll_id = poll_id
        self.option_id = option_id
        self.user_id = user_id
