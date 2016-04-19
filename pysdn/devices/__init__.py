#!/usr/bin/env python3

#import abc

from pysdn.exceptions import UnknownConnector, NotCompatibleConnector, InsufficientAvailablePorts
from pysdn.exceptions import AlreadyConnected, NotConnected, SelfConnect
from pysdn.exceptions import AlreadyXConnected, NotXConnected, SelfXConnect

from pysdn.cables import Cable

class Rack(object):

    # 47 U
    DEFAULT_HEIGHT = 47
    name = None
    u = {}
    devices = {}

    def __init__(self, **kwargs):
        self.name = kwargs['name']

        if 'height' in kwargs:
            self.height = kwargs['height']
        else:
            self.height = self.DEFAULT_HEIGHT

        self.devices = {}
        self.u = {}

    def rack(self, device, u, height):
        for pos in range(u, u+height):
            if pos in self.u:
                raise Exception('This rack position is already occupied')

        du =[]
        for pos in range(u, u+height):
            self.u[pos] = device
            du.append(pos)

        self.devices[device.name] = device
        device.owner = self
        device.u = ','.join(map(str,du))

    def __str__(self):
        return self.name

class Transceiver(object):

    GBIC = 200
    SFP = 201
    SFPPLUS = 202
    XFP = 203
    QSFP = 204

    def known_transceivers():
        return (Transceiver.GBIC,
                Transceiver.SFP,
                Transceiver.SFPPLUS,
                Transceiver.XFP,
                Transceiver.QSFP,
                )

class Connector(object):

    # fiber connectors
    LC = 100
    SC = 101
    FC = 102
    # copper connectors
    RJ45 = 103
    DB9 = 104
    DB25 = 105
    # power connector
    C13 = 106

    def known_connectors():
        return (Connector.LC,
                Connector.SC,
                Connector.FC,
                Connector.RJ45,
                Connector.DB9,
                Connector.DB25,
                Connector.C13,
                )

class Port(object):

    p_port = None
    owner = None
    transceiver = None

    def __init__(self, **kwargs):
        self.name = kwargs['name']
        self.connector = kwargs['connector']

        if self.connector not in Connector.known_connectors() and\
                self.connector not in Transceiver.known_transceivers():
            raise UnknownConnector()

    def set_transceiver(self, transceiver):
        if not isinstance(transceiver, Transceiver):
            raise Exception('Transceiver instance expected')

        if self.connector not in Transceiver.known_transceivers():
            raise Exception('This port cant have a transceiver')

        self.transceiver = transceiver

    def has_transceiver(self):
        return self.transceiver is not None

    def get_transceiver(self):
        if self.has_transceiver():
            return self.transceiver
        else:
            raise Exception('no transceiver on this port')

    def connect(self, p_port, cable):
        if not isinstance(p_port, Port):
            raise Exception('Port instance expected')

        if not isinstance(cable, Cable):
            raise Exception('Cable instance expected')

        if self.p_port is not None:
            raise AlreadyConnected('%s => %s'.format(self, self.p_port))

        if p_port.p_port is not None:
            raise AlreadyConnected('%s => %s'.format(p_port, p_port.p_port))

        if p_port is self:
            raise SelfConnect()

        if self.is_fiber() and not p_port.is_fiber() or self.is_copper() and not p_port.is_copper():
            raise NotCompatibleConnector()

        self.p_port = p_port
        p_port.p_port = self

    def disconnect(self):
        if self.p_port is None:
            raise NotConnected()

        self.p_port.p_port = None
        self.p_port = None

    def is_fiber(self):
        return self.connector >= 100 and self.connector <= 199

    def is_copper(self):
        return self.connector >= 200 and self.connector <= 299

    def __str__(self):
        return self.name

class PatchPort(Port):
    x_port = None

    def x_connect(self, x_port):
        if not isinstance(x_port, PatchPort):
            raise Exception('PatchPort instance expected')

        if self.x_port is not None:
            raise AlreadyXConnected('%s => %s'.format(self, self.x_port))

        if x_port.x_port is not None:
            raise AlreadyXConnected('%s => %s'.format(x_port, x_port.x_port))

        if x_port is self:
            raise SelfXConnect()

        if self.is_fiber() and not x_port.is_fiber() or self.is_copper() and not x_port.is_copper():
            raise NotCompatibleConnector()

        self.x_port = x_port
        x_port.x_port = self

    def x_disconnect(self):
        if self.x_port is None:
            raise NotXConnected()

        self.x_port.x_port = None
        self.x_port = None

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

