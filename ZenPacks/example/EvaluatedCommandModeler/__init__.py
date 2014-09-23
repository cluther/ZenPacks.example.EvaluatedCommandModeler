import sys

from Products.ZenModel.ZenPack import ZenPack as ZenPackBase
from Products.ZenRelations.zPropertyCategory import setzPropertyCategory
from Products.ZenUtils.Utils import monkeypatch
from Products.ZenUtils.ZenTales import talesEvalStr


setzPropertyCategory('zExamplePath', 'Example')


class ZenPack(ZenPackBase):
    packZProperties = [
        ('zExamplePath', '/scripts', 'string'),
        ]


# SshClient does a relative import of CollectorClient. This means we
# have to monkeypatch the relative CollectorClient module already in
# sys.modules.
if 'CollectorClient' in sys.modules:
    CollectorClient = sys.modules['CollectorClient']

    @monkeypatch(CollectorClient.CollectorClient)
    def __init__(self, *args, **kwargs):
        # original is injected into locals by the monkeypatch decorator.
        original(self, *args, **kwargs)

        # Reset cmdmap and _commands.
        self.cmdmap = {}
        self._commands = []

        # Get plugins from args or kwargs.
        plugins = kwargs.get('plugins')
        if plugins is None:
            if len(args) > 3:
                plugins = args[3]
            else:
                plugins = []

        # Get device from args or kwargs.
        device = kwargs.get('device')
        if device is None:
            if len(args) > 5:
                device = args[5]
            else:
                device = None

        # Do TALES evaluation of each plugin's command.
        for plugin in plugins:
            if '${' in plugin.command:
                try:
                    command = talesEvalStr(plugin.command, device)
                except Exception:
                    CollectorClient.log.exception(
                        "%s - command parsing error",
                        device.id)

                    continue
            else:
                command = plugin.command

            self.cmdmap[command] = plugin
            self._commands.append(command)
