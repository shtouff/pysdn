from pysdn.devices import Switch, L3Switch, Router, Port, LineCard, Connector, Transceiver

class Nexus3064_X(L3Switch):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.add_port(Port(name='console', connector=Connector.RJ45))
        # 48xSFP+
        for i in range(0, 48):
            self.add_port(Port(name='Eth1/{}'.format(i), connector=Connector.SFPPLUS))
        # 4xQSFP+
        for i in range(48, 52):
            self.add_port(Port(name='Eth1/{}'.format(i), connector=Connector.QSFP))

class Nexus3048(L3Switch):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.add_port(Port(name='console', connector=Connector.RJ45))
        # 48xRJ45
        for i in range(0, 48):
            self.add_port(Port(name='Eth1/{}'.format(i), connector=Connector.RJ45))
        # 4xSFP+
        for i in range(48, 52):
            self.add_port(Port(name='Eth1/{}'.format(i), connector=Connector.SFPPLUS))

class ASR9001(Router):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.height = 2
        self.add_port(Port(connector=Connector.RJ45, name='console'))
        self.add_port(Port(connector=Connector.RJ45, name='aux'))
        self.add_port(Port(connector=Connector.RJ45, name='mgt0'))
        self.add_port(Port(connector=Connector.RJ45, name='mgt1'))

        for i in range(0,4):
            self.add_port(Port(connector=Connector.SFPPLUS, name='sfp+{}'.format(i)))

class SF300(Switch):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_port(Port(connector=Connector.DB9, name='console'))

class SF300_24(SF300):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_module(LineCard(connector=Connector.RJ45, name='fa', base=1, size=24))
        self.add_module(LineCard(connector=Connector.RJ45, name='gi', base=1, size=4))
