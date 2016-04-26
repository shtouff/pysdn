from pysdn import Connector, Transceiver, Cable

class CableEndpoint(object):
    pass

class LCLCDuplexPatch(Cable):
    name = 'lc-lc-duplex'

    def connect(self, A, B):
        self.a


class SCLCDuplexPatch(Cable):
    pass

class UTPCat6Patch(Cable):
    name = 'utp-cat6'

class Twinax(Cable, Transceiver):
    name = 'twinax'
