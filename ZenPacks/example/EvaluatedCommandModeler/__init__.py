import sys

from Products.ZenModel.ZenPack import ZenPack as ZenPackBase
from Products.ZenRelations.zPropertyCategory import setzPropertyCategory
from Products.ZenUtils.ZenTales import talesEvalStr


setzPropertyCategory('zExamplePath', 'Example')


class ZenPack(ZenPackBase):
    packZProperties = [
        ('zExamplePath', '/scripts', 'string'),
        ]


# SshClient does a relative import of CollectorClient. This makes it
# impossible to use the @monkeypatch decorator. We instead have to find
# the relative import in sys.modules and monkeypatch it there.
if 'CollectorClient' in sys.modules:
    CollectorClient = sys.modules['CollectorClient']

    def CollectorClient_getCommands(self):
        '''
        The commands which we will use to collect data.

        Overridden here to allow TALES evaluation of modeler plugin command
        attribute.
        '''
        for command in self._commands:
            if '${' not in command:
                yield command

            try:
                yield talesEvalStr(command, self.device)
            except Exception:
                CollectorClient.log.exception(
                    "%s - command parsing error",
                    self.device.id)

    CollectorClient.CollectorClient.getCommands = CollectorClient_getCommands
