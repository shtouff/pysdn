from abc import ABCMeta

class Outlet:
    __metaclass__ = ABCMeta

class Port(object):

    p_port = None
    owner = None
    transceiver = None

    def __init__(self, **kwargs):
        self.name = kwargs['name']
        self.connector = kwargs['connector']

        if self.connector not in Connector.known_connectors():
            raise UnknownConnector()

    def set_transceiver(self, transceiver):
        if not isinstance(transceiver, Transceiver):
            raise Exception('Transceiver instance expected')

        if not transceiver.is_compatible(self.connector):
            raise exceptions.CantHandleTransceiver()

        self.transceiver = transceiver

    def has_transceiver(self):
        return self.transceiver is not None

    def get_transceiver(self):
        if self.has_transceiver():
            return self.transceiver
        else:
            raise Exception('no transceiver on this port')

    def is_connected(self):
        return p_port is not None

    def __str__(self):
        return self.name

class Transceiver(object):

    compatible_connectors = ()

    def is_compatible(self, connector):
        return connector in self.compatible_connectors

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

    # transceivers
    GBIC = 200
    SFP = 201
    SFPPLUS = 202
    XFP = 203
    QSFP = 204

    def known_connectors():
        return (Connector.LC,
                Connector.SC,
                Connector.FC,
                Connector.RJ45,
                Connector.DB9,
                Connector.DB25,
                Connector.C13,

                Connector.GBIC,
                Connector.SFP,
                Connector.SFPPLUS,
                Connector.XFP,
                Connector.QSFP,
                )

class Cable(object):
    def __init__(self, **kwargs):
        if 'length' in kwargs:
            self.length = kwargs['length']
        else:
            self.length = 1

    def connect(self, A, B):
        pass

    def __str__(self):
        return '{}-{}'.format(self.name, self.length)

