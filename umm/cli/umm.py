import subprocess

import click
from pygments import console

from umm.cli.client import confirm_request, umm_request


@click.command()
@click.option("--start", "-s", is_flag=True)
@click.option("--add", is_flag=True)
@click.argument("tags", nargs=-1)
def umm(start, add, tags):
    if add:
        # add simple commands
        return
    if start:
        print("umm server starting")
        from umm.server.__main__ import main

        main()
        return

    candidates = umm_request(tags)

    if len(candidates["commands"]) == 0:
        print("no candidate commands found")
        return

    for command in candidates["commands"]:
        msg = f"{command['command']} [y/n/c/p]?"
        msg = console.colorize("green", msg)
        action_str = click.prompt(msg, default="y")

        while action_str not in ["y", "n", "c", "p"]:
            print("invalid input. use [y/n/c/p]")
            action_str = click.prompt(msg, default="y")

        if action_str != "n":
            break

    # no candidate command selected found
    if action_str == "n":
        print("no command selected")
        return

    # if command has prompts
    prompts = command.get("prompts", [])
    in_data = []
    for prompt in prompts:
        in_data.append(click.prompt(f"{prompt} = ?"))

    # build command
    command_str = command["command"]
    for i, value in enumerate(in_data):
        command_str = command_str.replace(f"${i+1}", value)

    # get action
    command_actions = {
        "y": ([command_str], {"shell": True}),
        "c": ([f"echo {command_str} |pbcopy"], {"shell": True}),
        "p": ([f"echo {command_str}"], {"shell": True}),
    }

    cmd, kwargs = command_actions[action_str]
    subprocess.run(cmd, **kwargs)
    _ = confirm_request(command["id"])