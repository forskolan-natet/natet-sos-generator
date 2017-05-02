import random


class Day:

    def __init__(self, members=[]):
        random.shuffle(members)
        self.members = members
        self.tallen = self.members[0]
        self.granen = self.members[1]
