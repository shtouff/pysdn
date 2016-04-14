#!/usr/bin/env python3

from pysdn.exceptions import UnknownConnector, NotCompatibleConnector, InsufficientAvailablePorts
from pysdn.exceptions import AlreadyConnected, NotConnected, SelfConnect
from pysdn.exceptions import AlreadyXConnected, NotXConnected, SelfXConnect

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

        for pos in range(u, u+height):
            self.u[pos] = device

        self.devices[device.name] = device

    def __str__(self):
        return self.name

class Port(object):

    LC = 100
    SC = 101
    FC = 102

    RJ45 = 200

    knownConnectors = (LC, SC, FC, RJ45)

    p_port = None

    def __init__(self, **kwargs):
        self.name = kwargs['name']
        self.connector = kwargs['connector']
        self.owner = kwargs['owner']

        if self.connector not in self.knownConnectors:
            raise UnknownConnector()

    def connect(self, port):
        if self.p_port is not None or port.p_port is not None:
            raise AlreadyConnected()

        if port is self:
            raise SelfConnect()

        if self.is_fiber() and not port.is_fiber() or self.is_copper() and not port.is_copper():
            raise NotCompatibleConnector()

        self.p_port = port
        port.p_port = self

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

    def x_connect(self, port):
        if self.x_port is not None or port.x_port is not None:
            raise AlreadyXConnected()

        if port is self:
            raise SelfXConnect()

        if self.is_fiber() and not port.is_fiber() or self.is_copper() and not port.is_copper():
            raise NotCompatibleConnector()

        self.x_port = port
        port.x_port = self

    def x_disconnect(self):
        if self.x_port is None:
            raise NotXConnected()

        self.x_port.x_port = None
        self.x_port = None

class NetworkDevice(object):
    pass

class PatchPanel(NetworkDevice):
    def __init__(self, base=1, **kwargs):
        self.base = base
        self.size = kwargs['size']
        self.name = kwargs['name']
        self.connector = kwargs['connector']

        self.ports = []
        for i in range(0, self.size):
            self.ports.append(PatchPort(connector=self.connector, owner=self,
                name='port{}'.format(i+self.base)))

    def multi_x_connect(self, position, peer, peerPosition, size):
        for i in range(0, size):
            self.ports[position - 1 + i].x_connect(peer.ports[peerPosition - 1 + i])

    def __str__(self):
        return self.name

class LineCard(NetworkDevice):
    def __init__(self, base=1, portprefix='', **kwargs):
        self.base = base
        self.portprefix = portprefix
        self.size = kwargs['size']
        self.name = kwargs['name']
        self.connector = kwargs['connector']

        self.ports = []
        for i in range(0, self.size):
            self.ports.append(Port(connector=self.connector, owner=self,
                name='{}{}'.format(self.portprefix, i+self.base)))

    def __str__(self):
        if len(self.name) > 0:
            return '{}/'.format(self.name)
        return ''

class ActiveNetworkDevice(NetworkDevice):
    def __init__(self, **kwargs):
        self.name = kwargs['name']
        self.cards = []

    def add_line_card(self, card):
        self.cards.append(card)
        card.owner = self

    def __str__(self):
        return self.name

class Switch(ActiveNetworkDevice):
    pass

class Router(ActiveNetworkDevice):
    pass

class L3Switch(Router, Switch):
    pass

class MerakiMS420(L3Switch):
    pass

class MerakiMS220(Switch):
    pass

