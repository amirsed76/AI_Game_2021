import random
from python_client.base import BaseAgent, Action
import time

class Agent(BaseAgent):

    def do_turn(self) -> Action:
        return random.choice([Action.UP, Action.DOWN, Action.LEFT, Action.RIGHT, Action.TELEPORT, Action.NOOP])


if __name__ == '__main__':
    data = Agent().play()
    print("FINISH : ", data)
