# This is just an advanced example

import argparse
import os, sys
import subprocess
import threading
import asyncio
import nest_asyncio
from discordRebot import *

client = discord.Client()
Convert = Converter(bot=client)


@client.event
async def on_ready():
    print(f"{client.user.name} is Online :]")


P2F = dict()

### Python shell
async def Exec(msg, code):
    try:
        code = compile(code, "code", "eval")
        Exec._ = eval(code, {**Exec.globals, "_": Exec._, "msg": msg}, Exec.globals)
        return RE_MARKDOWN.sub(r"\\\1", repr(Exec._))
    except SyntaxError:
        try:
            code = compile(code, "code", "exec")
            exec(code, {**Exec.globals, "_": Exec._, "msg": msg}, Exec.globals)
            return "EXEC success"
        except:
            return RE_MARKDOWN.sub(r"\\\1", repr(sys.exc_info()))
    except:
        return RE_MARKDOWN.sub(r"\\\1", repr(sys.exc_info()))


Exec.globals = dict()
Exec._ = None

### System shell
async def Shell(msg, cmd):
    process = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=True,
    )
    Shell.processes.append(process)  # To kill running subprocess
    response = list()
    threading.Thread(  # To not wait untill done
        target=lambda p, r: r.extend(p.communicate()), args=(process, response)
    ).start()
    while not response:
        await asyncio.sleep(0.3)
    Shell.processes.remove(process)

    output, error = response[0].decode(), response[1].decode()
    outAerr = "```bash\n$ " + cmd.replace("`", "`" + ZWS) + "\n```"
    if output:
        outAerr += "```bash\n" + output.replace("`", "`" + ZWS) + "\n```"
    if error:
        outAerr += "stderr:\n```bash\n" + error.replace("`", "`" + ZWS) + "\n```"
    outAerr += f"Return code = {process.returncode}"
    return outAerr


Shell.processes = list()

### To exit
async def Exit(msg):
    await msg.channel.send("Bye Bye")
    await client.close()


P2F["!exit"] = Exit


def add_rshell(pattern=r"^\$ ([\s\S]*)$", auth=None):
    pattern = re.compile(pattern)
    Shell.auth = auth

    P2F[pattern] = Shell


def add_rpy(pattern=r"^>> ([\s\S]*)$", auth=None, globals=None):
    pattern = re.compile(pattern)
    Exec.auth = auth
    Exec.globals = __builtins__.globals() if globals is None else globals

    P2F[pattern] = Exec

    nest_asyncio.apply()  # to use asyncio.run(coro) in rpy


def run(token):
    global mybot
    mybot = Manager(P2F)
    client.event(mybot.on_message)
    client.run(token)


def core(parser, args):

    if args.rshell_auth is not DontAdd:
        add_rshell(auth=args.rshell_auth)

    if getattr(args, "rpy_auth, rpy_globals") is not DontAdd:
        authAglobals = getattr(args, "rpy_auth, rpy_globals")
        if len(authAglobals) == 1:
            add_rpy(auth=authAglobals[0])
        else:
            add_rpy(auth=authAglobals[0], globals=authAglobals[1])

    run(args.Token)


DontAdd = type("Don't_add_this FLAG", (), {})


def parse_args():
    parser = argparse.ArgumentParser(
        prog="discordRebot.tryrebot",
        description="To try an advanced example of rebot.\n"
        + "Example: `python -m discordRebot.tryrebot $TOKEN --rpy 'Roles[\"Admin\"],'`",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "--rshell",
        dest="rshell_auth",
        action="store",
        type=lambda x: eval(x, globals()),
        const=None,
        default=DontAdd,
        nargs="?",
        help="To add remote shell to rebot with given auth",
    )
    parser.add_argument(
        "--rpy",
        dest="rpy_auth, rpy_globals",
        action="store",
        type=lambda x: eval(x, globals()),
        const=(None, None),
        default=DontAdd,
        nargs="?",
        help="To add remote py repl to rebot with given auth and globals",
    )
    parser.add_argument("Token", action="store", type=str, help="Token to run discord bot client")
    parser.set_defaults(func=core)

    return parser, parser.parse_args()


def main():
    parser, args = parse_args()
    args.func(parser, args)


if __name__ == "__main__":
    main()
