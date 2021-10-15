import random
from base import BaseAgent, Action


class Agent(BaseAgent):

    def do_turn(self) -> Action:
        return random.choice(
            [Action.UP, Action.DOWN, Action.LEFT, Action.RIGHT, Action.TELEPORT, Action.NOOP, Action.TRAP])


if __name__ == '__main__':
    data = Agent().play()
    print("FINISH : ", data)
