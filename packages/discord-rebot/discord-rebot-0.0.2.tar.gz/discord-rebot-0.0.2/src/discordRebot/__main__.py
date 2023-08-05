"""cli for discordRebot"""

import argparse
import sys
from pathlib import Path

import re
import platform
import discord
import discordRebot as rebot
import pkg_resources
import aiohttp
import websockets


def show_version():
    """To show versions of modules/package used"""

    entries = []

    entries.append(
        "- Python v{0.major}.{0.minor}.{0.micro}-{0.releaselevel}".format(sys.version_info)
    )
    version_info = discord.version_info
    entries.append(
        "- discord.py v{0.major}.{0.minor}.{0.micro}-{0.releaselevel}".format(version_info)
    )
    if version_info.releaselevel != "final":
        pkg = pkg_resources.get_distribution("discord.py")
        if pkg:
            entries.append("    - discord.py pkg_resources: v{0}".format(pkg.version))

    entries.append("- discord-rebot v{0.__version__}".format(rebot))
    entries.append("- re v{0.__version__}".format(re))

    entries.append("- aiohttp v{0.__version__}".format(aiohttp))
    entries.append("- websockets v{0.__version__}".format(websockets))
    uname = platform.uname()
    entries.append("- system info: {0.system} {0.release} {0.version}".format(uname))
    print("\n".join(entries))


def core(parser, args):
    """func for show_version (-v)"""
    if args.version:
        show_version()


BOT_TEMPLATE = """#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from discordRebot import *
import config

client = discord.Client()
Convert = Converter(bot=client)
key = Mapper()

@client.event
async def on_ready():
    print(f"{client.user.name} is Online :]")

# write general commands here

# Example:
#  @key(re.compile(r"^!echo (.*)$"))
#  def echo(msg, string):
#      return string
#  echo.auth = None


client.event(Manager(key).on_message)
client.run(config.token)
"""

argv = sys.argv
sys.argv = [sys.argv[0]]
from discord.__main__ import to_path, gitignore_template as GITIGNORE_TEMPLATE

sys.argv = argv


def newrebot(parser, args):
    """func for newrebot"""

    new_directory = to_path(parser, args.directory) / to_path(parser, args.name)

    # as a note exist_ok for Path is a 3.5+ only feature
    # since we already checked above that we're >3.5
    try:
        new_directory.mkdir(exist_ok=True, parents=True)
    except OSError as exc:
        parser.error("could not create our bot directory ({})".format(exc))

    try:
        with open(str(new_directory / "config.py"), "w", encoding="utf-8") as config:
            config.write('token = "place your token here"\n')
    except OSError as exc:
        parser.error("could not create config file ({})".format(exc))

    try:
        with open(str(new_directory / "bot.py"), "w", encoding="utf-8") as bot:
            bot.write(BOT_TEMPLATE)
    except OSError as exc:
        parser.error("could not create bot file ({})".format(exc))

    if not args.no_git:
        try:
            with open(str(new_directory / ".gitignore"), "w", encoding="utf-8") as gitignore:
                gitignore.write(GITIGNORE_TEMPLATE)
        except OSError as exc:
            print("warning: could not create .gitignore file ({})".format(exc))

    print("successfully made rebot at", new_directory)


def add_newrebot_args(subparser):
    """to add newrebot args in parser"""

    parser = subparser.add_parser("newrebot", help="creates a command rebot project quickly")
    parser.set_defaults(func=newrebot)

    parser.add_argument("name", help="the bot project name")
    parser.add_argument(
        "directory",
        help="the directory to place it in (default: .)",
        nargs="?",
        default=Path.cwd(),
    )
    parser.add_argument(
        "--no-git", help="do not create a .gitignore file", action="store_true", dest="no_git"
    )


def parse_args():
    """to add show versions args in parser"""

    parser = argparse.ArgumentParser(
        prog="discordRebot", description="Tools for helping with discord-rebot"
    )
    parser.add_argument("-v", "--version", action="store_true", help="shows the library version")
    parser.set_defaults(func=core)

    subparser = parser.add_subparsers(dest="subcommand", title="subcommands")
    add_newrebot_args(subparser)
    return parser, parser.parse_args()


if __name__ == "__main__":
    parser, args = parse_args()
    args.func(parser, args)
