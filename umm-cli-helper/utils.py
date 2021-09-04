import yaml
from command import Command, CommandSet


def parse_commands(path: str):
    """"""
    with open(path) as f:
        comm_dict = yaml.full_load(f)
    commands = []
    for k, v in comm_dict["commands"].items():
        commands.append(Command(id=k, command=v["command"], tags=v["tags"]))

    return CommandSet(commands)
