from pysdn.devices import Connector, Transceiver

class LCDuplexTransceiver(Transceiver):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.connector = Connector.LC
        self.rx = None
        self.tx = None

class LCSimplexTransceiver(Transceiver):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.connector = Connector.LC

class SFPPlus(LCDuplexTransceiver):
    compatible_connectors = ( Connector.SFPPLUS, )

class SFP(LCDuplexTransceiver):
    compatible_connectors = ( Connector.SFPPLUS, Connector.SFP )

class XFP(LCDuplexTransceiver):
    compatible_connectors = ( Connector.XFP, )

class SFPBidi(LCSimplexTransceiver):
    compatible_connectors = ( Connector.SFPPLUS, Connector.SFP )
