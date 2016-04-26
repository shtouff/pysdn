from pysdn import Port, Connector
from pysdn.devices import ActiveNetworkDevice, LineCard

class CM4132(ActiveNetworkDevice):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.add_module(LineCard(connector=Connector.RJ45, name='port', base=1, size=32))
        self.add_port(Port(connector=Connector.RJ45, name='lan'))
        self.add_port(Port(connector=Connector.DB9, name='local'))

