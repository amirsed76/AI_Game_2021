from algorithm import action
from base import BaseAgent, Action
from pickle_initializer import initial_pickle


class Agent(BaseAgent):
    def __init__(self):
        super().__init__()
        if self.character == "A":
            self.opponent_Char = "B"
        else:
            self.opponent_Char = "A"
        self.old_opponent_loc = [-1, -1]
        self.old_agent_loc = [-1, -1]

    def do_turn(self) -> Action:
        next_move, self.old_opponent_loc = action(self.grid, self.agent_scores[self.id - 1],
                                                  self.agent_scores[(self.id + 1) % 2], self.character,
                                                  self.opponent_Char,
                                                  self.old_opponent_loc, self.old_agent_loc, self.trap_count)

        if next_move == "up":
            return Action.UP
        if next_move == "down":
            return Action.DOWN
        if next_move == "left":
            return Action.LEFT
        if next_move == "right":
            return Action.RIGHT
        if next_move == "teleport":
            return Action.TELEPORT
        if next_move == "noop":
            return Action.NOOP
        if next_move == "trap":
            return Action.TRAP
        # return random.choice(
        #     # [Action.UP, Action.DOWN, Action.LEFT, Action.RIGHT, Action.TELEPORT, Action.NOOP, Action.TRAP]
        #     [Action.UP, Action.DOWN, Action.LEFT, Action.RIGHT])


if __name__ == '__main__':
    initial_pickle()
    data = Agent().play()
    print("FINISH : ", data)
