from pysdn import Connector, Transceiver, Port

class LCDuplexTransceiver(Transceiver):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.connector = Connector.LC
        self.rx = pysdn.ports.Port(name='rx', connector=Connector.LC)
        self.tx = pysdn.ports.Port(name='tx', connector=Connector.LC)

class LCSimplexTransceiver(Transceiver):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.port = pysdn.ports.Port(name='port', connector=Connector.LC)

class SFPPlus(LCDuplexTransceiver):
    compatible_connectors = ( Connector.SFPPLUS, )

class SFP(LCDuplexTransceiver):
    compatible_connectors = ( Connector.SFPPLUS, Connector.SFP )

class XFP(LCDuplexTransceiver):
    compatible_connectors = ( Connector.XFP, )

class SFPBidi(LCSimplexTransceiver):
    compatible_connectors = ( Connector.SFPPLUS, Connector.SFP )
