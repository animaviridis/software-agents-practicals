import random


class Agent:
    def __init__(self, competence):
        self.competence = competence
        self.neighbours = set()
        self.score = [0, 0]

    def __str__(self):
        return f"Agent: competence={self.competence}, score={self.score}"

    def do_task(self):
        return random.random() < self.competence

    def delegate(self):
        success = False
        if self.pick_partner().do_task():
            self.score[0] += 1
            success = True
        else:
            self.score[1] += 1
        return success

    def get_reputation(self, target):
        """returns the reputation value for agent target according to this agent"""

        raise NotImplementedError()

    def pick_partner(self):
        """select a partner for interaction from the agent's neighbours"""

        raise NotImplementedError()
