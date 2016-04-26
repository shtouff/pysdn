from pysdn import Connector, Transceiver, Port

class PatchPort(Port):
    x_port = None

    def x_connect(self, x_port):
        if not isinstance(x_port, PatchPort):
            raise Exception('PatchPort instance expected')

        if self.x_port is not None:
            raise AlreadyXConnected('{} => {}'.format(self, self.x_port))

        if x_port.x_port is not None:
            raise AlreadyXConnected('{} => {}'.format(x_port, x_port.x_port))

        if x_port is self:
            raise SelfXConnect()

        self.x_port = x_port
        x_port.x_port = self

    def x_disconnect(self):
        if self.x_port is None:
            raise NotXConnected()

        self.x_port.x_port = None
        self.x_port = None

