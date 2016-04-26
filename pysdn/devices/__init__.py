#!/usr/bin/env python3

from pysdn import exceptions
from pysdn.ports import PatchPort
from pysdn import Cable, Connector, Transceiver, Port

class RackableDevice(object):
    def __init__(self, **kwargs):
        if 'height' in kwargs:
            self.height = kwargs['height']
        else:
            self.height = 1

        self.name = kwargs['name']
        self.ports = {}

    def add_port(self, port):
        if not isinstance(port, Port):
            raise Exception('Port instance expected')

        if port.name in self.ports:
            raise Exception('port {} already added'.format(port.name))

        if port.owner is None:
            port.owner = self
        else:
            raise Exception('port already owned by {}'.format(port.owner))

        self.ports[port.name] = port
        if not isinstance(port, Port):
            raise Exception('Port instance expected')

    def get_port(self, name):

        if name in self.ports:
            return self.ports[name]

        for card in self.cards.values():
            for port in card.ports:
                if port.name == name:
                    self.ports[port.name] = port
                    return port

        raise Exception('no such port')

    def __str__(self):
        return self.name

class PatchPanel(RackableDevice):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)

        if 'base' in kwargs:
            self.base = kwargs['base']
        else:
            self.base = 1
        self.size = kwargs['size']
        self.connector = kwargs['connector']

        self.ports = []
        for i in range(0, self.size):
            self.ports.append(PatchPort(connector=self.connector, owner=self,
                name='port{}'.format(i+self.base)))

    def multi_x_connect(self, position, peer, peerPosition, size):
        for i in range(0, size):
            self.ports[position - 1 + i].x_connect(peer.ports[peerPosition - 1 + i])

class PluggableModule(object):
    def __init__(self, **kwargs):
        self.name = kwargs['name']
        self.ports = {}

    def add_port(self, port):
        if not isinstance(port, Port):
            raise Exception('Port instance expected')

        if port.name in self.ports:
            raise Exception('port {} already added'.format(port.name))

        if port.owner is None:
            port.owner = self
        else:
            raise Exception('port already owned by {}'.format(port.owner))

        self.ports[port.name] = port
        if not isinstance(port, Port):
            raise Exception('Port instance expected')

    def __str__(self):
        return self.name

class LineCard(PluggableModule):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if 'base' in kwargs:
            self.base = kwargs['base']
        else:
            self.base = 1

        if 'size' in kwargs:
            self.size = kwargs['size']
        else:
            self.size = 8

        if 'connector' in kwargs:
            self.connector = kwargs['connector']
        else:
            self.connector = Port.LC

        for i in range(0, self.size):
            self.add_port(Port(name='{}{}'.format(self.name, i+self.base), connector=self.connector))

class MuxModule(PluggableModule):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if 'connector' in kwargs:
            self.connector = kwargs['connector']
        else:
            self.connector = Port.LC

        if 'channels' in kwargs:
            self.channels = kwargs['channels']
        else:
            self.channels = range(28, 36)

        if 'upgrade' in kwargs:
            self.upgrade = kwargs['upgrade']
        else:
            self.upgrade = False

        if 'monitor' in kwargs:
            self.monitor = kwargs['monitor']
        else:
            self.monitor = False

        self.ports = {}
        self.add_port(Port(name='{}/common'.format(self.name), connector=self.connector))

        if self.monitor:
            self.add_port(Port(name='{}/monitor'.format(self.name), connector=self.connector))

        if self.upgrade:
            self.add_port(Port(name='{}/upgrade'.format(self.name), connector=self.connector))

        for channel in self.channels:
            self.add_port(Port(name='{}/ch{}'.format(self.name, str(channel)), connector=self.connector))

class ActiveNetworkDevice(RackableDevice):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.modules = {}

    def add_module(self, module):
        if not isinstance(module, PluggableModule):
            raise Exception('PluggableModule instance expected')

        if module.name in self.modules:
            raise Exception('module {} already added'.format(module.name))

        self.modules[module.name] = module
        module.owner = self

    def get_port(self, name):
        try:
            return super().get_port(name)
        except Exception as e:
            for module in self.modules.values():
                if name in module.ports:
                    return module.ports[name]

        raise Exception('no such port: {}'.format(name))

class OpticalMux(ActiveNetworkDevice):
    pass

class Switch(ActiveNetworkDevice):
    pass

class Router(ActiveNetworkDevice):
    pass

class L3Switch(Router, Switch):
    pass

