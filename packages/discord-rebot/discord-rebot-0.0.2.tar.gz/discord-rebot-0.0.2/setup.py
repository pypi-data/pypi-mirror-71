# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['discordRebot']

package_data = \
{'': ['*']}

install_requires = \
['discord.py>=1.3.3,<2.0.0']

setup_kwargs = {
    'name': 'discord-rebot',
    'version': '0.0.2',
    'description': 'RegEx based command mapping discord BOT framework with authorization',
    'long_description': '[![Latest version on\nPyPi](https://badge.fury.io/py/discord-rebot.svg)](https://badge.fury.io/py/discord-rebot)\n[![Supported Python\nversions](https://img.shields.io/pypi/pyversions/discord-rebot.svg)](https://pypi.org/project/discord-rebot/)\n[![Documentation\nstatus](https://readthedocs.org/projects/discord-rebot/badge/?version=latest&style=flat-square)](https://discord-rebot.readthedocs.io/en/latest/?badge=latest)\n[![Code style:\nblack](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) <!--\n[![Downloads](https://pepy.tech/badge/discord-rebot/month)](https://pepy.tech/project/discord-rebot/month)-->\n<a href="https://tox.readthedocs.io">\n    <img src="https://raw.githubusercontent.com/nkpro2000sr/discord-rebot/master/docs/_static/img/discordRebot.png"\n         alt="discord-rebot logo"\n         height="200px"\n         align="left">\n</a>\n\n# Welcome to discord-rebot (py)\n\n**discordRebot** is a RegEx based command mapping discord BOT framework\nwith **authorization**.\n\n</br>\n\n## Why discordRebot?\n\n**discordRebot** is easy to use, minimal, and async ready framework\nusing [discord.py](https://discordpy.readthedocs.io/en/latest)\n\nMost of the bots uses a single prefix, string to match command and args\nsplit by spaces, example `!cmd arg1 arg2`.\n\nBut discordRebot uses RegEx for both matching the command and capturing\nthe arguments. It gives more control over both matching the command and\nparsing arguments.\n\nAlso, it provides authorization to authorize the author of the message\nbefore executing the command.\n\n## Basic Example\n\nA minimal bot with echo command\n\n```python3\nfrom discordRebot import *\n\nclient = discord.Client()\nkey = Mapper()\n\n@key(re.compile(r"^!echo (.*)$")) # Eg: \'!echo hello\' -> \'hello\'\ndef echo(msg, string):\n    return string\necho.auth = None\n\nclient.event(Manager(key).on_message)\nimport os; client.run(os.environ["DBToken"])\n```\nYou can find more examples in the examples directory.\n\n## Features\n\n*   It also supports  \n    *   [generators](https://wiki.python.org/moin/Generators)  \n    *   [asynchronousfunctions](https://docs.python.org/library/asyncio.html)  \n    *   [asynchronousgenerators](https://www.python.org/dev/peps/pep-0525)  \n    ##### Example:\n    ```python3\n    @key(re.compile(r"^!ticker (\\d*) (\\d*)$"))\n    async def ticker(msg, delay, to):\n        delay, to = int(delay), int(to)\n        for i in range(to):\n            yield i\n            await asyncio.sleep(delay)\n    ```\n\n*   Authorizes the message author  \n    based on  \n    *   user\\_id example:`1234567890`  \n    *   user\\_name example:`\'user#1234\'`  \n    *   roles server *(not applicable for DM)*  \n    *   permissions of members in server *(not applicable for DM)*  \n    *   custom **Callable[[author], bool]**  \n    ##### Example:\n    ```python3\n    @key("am i authorized ?")\n    def amiauthorized(msg):\n        return "Authorized"\n    amiauthorized.auth = {1234567890, \'user#1234\'}\n    # only executable by user1 (with id 1234567890) and user2 (with username \'user#1234\')\n    ```\n\n*   Can match multiple commands with a message  \n    ##### Example:\n    ```python3\n    @key(re.compile(r"^([\\s\\S]*)$"))\n    def printmsg(msg, content):\n        print(f"@{msg.author}:")\n        print(content)\n\n    @key("whereami")\n    def whereami(msg):\n        if msg.guild:\n            return msg.guild.name\n        else:\n            return "DM"\n    ```\n\n## Links\n* [Documentation](https://discordRebot.readthedocs.io/en/latest/)\n* [PyPi](https://pypi.org/project/discord-rebot/)\n\n</br></br>\n<sup> [discordpy-ext-rebot](https://github.com/nkpro2000sr/discordpy-ext-rebot) comming soon (for full featured Discord Bot with RegEx based argparser) </sup>\n',
    'author': 'nkpro2000sr',
    'author_email': 'srnaveen2k@yahoo.com',
    'maintainer': 'nkpro2000sr',
    'maintainer_email': 'srnaveen2k@yahoo.com',
    'url': 'https://github.com/nkpro2000sr/discord-rebot',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
