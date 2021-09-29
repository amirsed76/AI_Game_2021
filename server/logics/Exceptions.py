class ExistTrap(Exception):
    def __init__(self, agent_id, tile_address):
        self.tile_address = tile_address
        self.agent_id = agent_id

    @property
    def message(self):
        return f"exist a trap in tile = {self.tile_address} , when agent {self.agent_id} wanted put "

    def __str__(self):
        return self.message


class AgentNotHaveTrap(Exception):
    def __init__(self, agent_id):
        self.agent_id = agent_id

    @property
    def message(self):
        return f"agent {self.agent_id} does not have trap"

    def __str__(self):
        return self.message


class CantPutTrapInTeleport(Exception):
    def __init__(self, agent_id):
        self.agent_id = agent_id

    @property
    def message(self):
        return f"can't put trap on teleport [agent = {self.agent_id}]"

    def __str__(self):
        return self.message


class NotExistAvailableTeleport(Exception):
    def __init__(self, agent_id):
        self.agent_id = agent_id

    @property
    def message(self):
        return f"agent {self.agent_id} can't use teleport because not exist available teleport "

    def __str__(self):
        return self.message


class NotAvailableMove(Exception):
    def __init__(self, agent_id, move: str, tile_address):
        self.agent_id = agent_id
        self.move = move
        self.tile_address = tile_address

    @property
    def message(self):
        return f"can't go {self.move} in address = {self.tile_address} with agent {self.agent_id}"

    def __str__(self):
        return self.message


class TrapConstraintFailed(Exception):
    def __init__(self, agent_id):
        self.agent_id = agent_id

    @property
    def message(self):
        return f"trap constraint failed for agent {self.agent_id}"

    def __str__(self):
        return self.message


class InValidAction(Exception):
    def __init__(self, agent_id):
        self.agent_id = agent_id

    @property
    def message(self):
        return f"agent {self.agent_id} send invalid action or time out for sending it "

    def __str__(self):
        return self.message



class TeleportOnInvalidTile(Exception):
    def __init__(self, agent_id, tile_address):
        self.tile_address = tile_address
        self.agent_id = agent_id


    @property
    def message(self):
        return f"agent {self.agent_id} can't teleport in tile {self.tile_address} "

    def __str__(self):
        return self.message
