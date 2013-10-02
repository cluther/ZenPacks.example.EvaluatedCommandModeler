'''
Example modeler plugin demonstrating a modeler plugin technique.

This modeler plugin provides no useful value and shouldn't actually be
used as anything more than an example.
'''

from Products.DataCollector.plugins.CollectorPlugin import CommandPlugin


class EvaluatedCommand(CommandPlugin):
    deviceProperties = CommandPlugin.deviceProperties + (
        'zExamplePath',
        )

    # Note that we're using TALES in the command. Normally that's not
    # possible. Check out the monkeypatch of channelOpen in this
    # ZenPack's __init__.py to see what makes it possible.

    command = '${here/zExamplePath}/myscript.sh'

    def process(self, device, results, log):
        log.info(
            'Modeler %s processing data for device %s',
            self.name(), device.id)

        maps = []

        # Do something useful with results.
        log.info(results)

        return maps
