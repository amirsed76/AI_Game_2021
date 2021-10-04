import json

from server.logics.map import Map, Tile
from server.logics.agent import Agent
from server.logics.actions import Actions
import random
import numpy as np
from server.logics import Exceptions, game_rules
from datetime import datetime


class Game:
    def __init__(self, time_out: int, agents: list, game_map: Map, turn_count):
        self.time_out = time_out
        self.agents = agents
        self.game_map = game_map
        self.max_turn_count = turn_count
        self.turn_number = 0
        self.turn_logs = []
        self.current_report = ""

    @staticmethod
    def create_game(config, player_connections: list, game_map: Map):
        addresses = [(0, 0), (game_map.height - 1, game_map.width - 1), (0, game_map.width - 1),
                     (game_map.height - 1, 0)]

        if config["init_random_location"]:
            random.shuffle(addresses)

        agents = []
        for i, conn in enumerate(player_connections):
            y, x = addresses[i]
            agents.append(Agent(agent_id=i, tile=game_map.get_tile(y=y, x=x), init_score=config["init_score"],
                                trap_count=config["trap_count"], connection=conn))

        time_out = config["time_out"]
        turn_count = config["turn_count"]
        return Game(time_out=time_out, agents=agents, game_map=game_map, turn_count=turn_count)

    def get_show(self, for_player=None):
        map_array = self.game_map.get_show()
        map_array = map_array.astype(dtype=np.dtype("U25"))
        for agent in self.agents:
            y, x = agent.tile.address
            map_array[y][x] = map_array[y][x] + agent.character
            if for_player is None or agent.id == for_player.id:
                for trap_tile in agent.trap_tiles:
                    y, x = trap_tile.address
                    map_array[y][x] = map_array[y][x] + agent.trap_character

        return map_array

    def do_turn_init(self, agent):
        height, width = self.game_map.tiles.shape
        content = f"{height} {width} {agent.character} {agent.id} {agent.score} {self.max_turn_count} {len(self.agents)} " \
                  f"{agent.trap_count}"
        agent.connection.write_utf(msg=content)
        confirm_data = agent.connection.read_data()
        if confirm_data is None or confirm_data.lower() != "confirm":
            raise Exception(f"agent with id={agent.id} not send confirm")

    def send_turn_info(self, agent):
        map_chars = self.get_show(for_player=agent).reshape(self.game_map.height * self.game_map.width, ).tolist()
        content = f"{self.turn_number} {agent.trap_count} {' '.join([str(player.score) for player in self.agents])} {' '.join(map_chars)}"
        agent.connection.write_utf(msg=content)

    def do_turn(self, agent: Agent):
        self.send_turn_info(agent)
        turn_action_request = agent.connection.read_data()
        action = Actions(turn_action_request)
        self.do_action(action=action, agent=agent)
        self.current_report = f"accepted action : {action.value}"

    def add_gem(self, agent: Agent, gem):
        gem_constraints = game_rules.CONSTRAINTS
        constraint_score = 0
        constraint_max_gem_eating = 1000
        agent_gems_count = agent.get_gems_count()
        agent_gem_count = 0

        if gem == Tile.TileType.GEM1:
            constraint_score = gem_constraints["min_score_for_get_gem_1"]
            constraint_max_gem_eating = gem_constraints["max_eating_gem_1"]
            agent_gem_count = agent_gems_count["gem1"]

        if gem == Tile.TileType.GEM2:
            constraint_score = gem_constraints["min_score_for_get_gem_2"]
            constraint_max_gem_eating = gem_constraints["max_eating_gem_2"]
            agent_gem_count = agent_gems_count["gem2"]

        if gem == Tile.TileType.GEM3:
            constraint_score = gem_constraints["min_score_for_get_gem_3"]
            constraint_max_gem_eating = gem_constraints["max_eating_gem_3"]
            agent_gem_count = agent_gems_count["gem3"]

        if gem == Tile.TileType.GEM4:
            constraint_score = gem_constraints["min_score_for_get_gem_4"]
            constraint_max_gem_eating = gem_constraints["max_eating_gem_4"]
            agent_gem_count = agent_gems_count["gem4"]

        if agent.score >= constraint_score and agent_gem_count <= constraint_max_gem_eating:
            agent.add_gem(gem)
            agent.tile.tile_type = Tile.TileType.EMPTY

    def do_move_action(self, agent, target: Tile):

        for other_agent in self.agents:
            if other_agent == agent:
                continue
            if other_agent.tile == target:
                if agent.score >= other_agent:
                    other_agent.hit_hurts.append(agent)
                else:
                    agent.hit_hurts.append(other_agent)
                return

        if target.is_wall():
            raise

        agent.tile = target
        gem = target.get_gem()
        if gem is not None:
            self.add_gem(agent=agent, gem=gem)

        return

    def do_up_action(self, agent: Agent):
        current_y, current_X = agent.tile.address
        X, Y = current_X, current_y - 1
        target = self.game_map.get_tile(y=Y, x=X)
        if target is None:
            raise Exceptions.NotAvailableMove(agent_id=agent.id, move="up", tile_address=agent.tile.address)

        self.do_move_action(agent=agent, target=target)

    def do_down_action(self, agent: Agent):
        current_y, current_X = agent.tile.address
        X, Y = current_X, current_y + 1
        target = self.game_map.get_tile(y=Y, x=X)
        if target is None:
            raise Exceptions.NotAvailableMove(agent_id=agent.id, move="down", tile_address=agent.tile.address)
        self.do_move_action(agent=agent, target=target)

    def do_right_action(self, agent):
        current_y, current_X = agent.tile.address
        X, Y = current_X + 1, current_y
        target = self.game_map.get_tile(y=Y, x=X)
        if target is None:
            raise Exceptions.NotAvailableMove(agent_id=agent.id, move="right", tile_address=agent.tile.address)
        self.do_move_action(agent=agent, target=target)

    def do_left_action(self, agent):
        current_y, current_X = agent.tile.address
        X, Y = current_X - 1, current_y
        target = self.game_map.get_tile(y=Y, x=X)
        if target is None:
            raise Exceptions.NotAvailableMove(agent_id=agent.id, move="left", tile_address=agent.tile.address)
        self.do_move_action(agent=agent, target=target)

    def do_teleport(self, agent: Agent):
        teleports = self.game_map.get_teleports()
        if not agent.tile.tile_type == Tile.TileType.TELEPORT:
            raise Exceptions.TeleportOnInvalidTile(agent_id=agent.id, tile_address=agent.tile.address)
        teleports.remove(agent.tile)

        if len(teleports) > 0:
            target = random.choice(teleports)
            self.do_move_action(agent=agent, target=target)
        else:
            raise Exceptions.NotExistAvailableTeleport(agent_id=agent.id)

    def do_put_trap(self, agent):
        agent: Agent
        tile = agent.tile

        if agent.trap_count <= 0:
            raise Exceptions.AgentNotHaveTrap(agent_id=agent.id)

        for player in self.agents:
            if tile in agent.trap_tiles:
                raise Exceptions.ExistTrap(tile_address=tile.address, agent_id=agent.id)

        if tile.is_teleport():
            raise Exceptions.CantPutTrapInTeleport(agent_id=agent.id)

        trap_index = len(agent.trap_tiles)
        constraint_gem_score = game_rules.TRAP_CONSTRAINT_SCORE[trap_index]
        if agent.score > constraint_gem_score:
            agent.add_trap_tile(tile=tile)
        else:
            raise Exceptions.TrapConstraintFailed(agent_id=agent.id)

    def do_action(self, action, agent):

        if action == Actions.UP:
            self.do_up_action(agent=agent)

        elif action == Actions.DOWN:
            self.do_down_action(agent=agent)

        elif action == Actions.RIGHT:
            self.do_right_action(agent=agent)

        elif action == Actions.LEFT:
            self.do_left_action(agent=agent)

        elif action == Actions.TELEPORT:
            self.do_teleport(agent=agent)

        elif action == Actions.TRAP:
            self.do_put_trap(agent=agent)

        elif action == Actions.NOOP:
            pass

        else:
            raise Exceptions.InValidAction(agent_id=agent.id)

    def turn_log(self, agent_id, finish=False, winner_id=None, report=""):
        self.turn_logs.append(

            {
                "turn": self.turn_number,
                "agent": agent_id,
                "agents_info": [player.get_information() for player in self.agents],
                "finish": finish,
                "winner_id": winner_id,
                "map": self.get_show().tolist(),
                "report": report
            }

        )

    def is_finish(self):
        for agent in self.agents:
            if agent.score <= game_rules.GAME_OVER_SCORE:
                return True

        return False

    def get_winner(self):
        # TODO for two players
        agents = sorted(self.agents, key=lambda agent: -agent.score)

        if len(agents) == 1:
            return None
        else:
            agent1, agent2 = agents[0], agents[1]
            if agent1.score < agent2.score:
                return [agent2]
            if agent2.score < agent1.score:
                return [agent1]
            else:
                return [agent1, agent2]

    def run(self):
        for agent in self.agents:
            self.do_turn_init(agent=agent)
            agent.connection.set_time_out(self.time_out)

        report = ""
        for turn_number in range(1, self.max_turn_count + 1):
            self.turn_number = turn_number
            print("_" * 20)
            print(f"turn : {turn_number} \n ")

            for agent in self.agents:
                try:
                    agent.turn_age = turn_number
                    self.do_turn(agent=agent)
                except Exception as e:
                    self.current_report = str(e)
                gem1_count, gem2_count, gem3_count, gem4_count = agent.get_gems_count().values()
                report = f"agent {agent.id} => score:{agent.score} gem1:{gem1_count} gem2:{gem2_count} gem3:{gem3_count} gem4:{gem4_count} trap_count:{agent.trap_count} report: {self.current_report}"
                print(report)

                self.turn_log(agent_id=agent.id, finish=False, winner_id=None,
                              report=f"agent {agent.id} :{self.current_report}")

            if self.is_finish():
                break

        winners = self.get_winner()

        if winners is None:
            winner = None
            for agent in self.agents:
                try:
                    agent.connection.write_utf(msg=f"finish!")
                    self.turn_log(agent_id=None, finish=True, winner_id=None,
                                  report=f"finish!")
                except:
                    pass

        elif len(winners) == 1:
            winner = winners[0]
            for agent in self.agents:
                try:
                    agent.connection.write_utf(msg=f"finish! winner = agent {winner.id}")
                    self.turn_log(agent_id=None, finish=True, winner_id=winner.id,
                                  report=f"finish! winner = agent {winner.id}")
                except:
                    pass
        else:
            winner = None
            for agent in self.agents:
                try:
                    agent.connection.write_utf(msg=f"finish! Draw the game")
                except:
                    pass
            self.turn_log(agent_id=None, finish=True, winner_id=None, report=f"finish! The game ended in a draw")

        now_time = datetime.now()
        with open(f"game_logs/{now_time.month}_{now_time.day}_{now_time.hour}_{now_time.minute}_{now_time.second}.json",
                  "w") as file:
            json.dump(self.turn_logs, file)
