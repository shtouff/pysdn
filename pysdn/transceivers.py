from pysdn.devices import Connector, Transceiver

class SFPPlus(Transceiver):
    def __init__(self):
        self.connector = Connector.LC

