class UnknownConnector(Exception):
    pass

class NotCompatibleConnector(Exception):
    pass

class AlreadyConnected(Exception):
    pass

class NotConnected(Exception):
    pass

class SelfConnect(Exception):
    pass

class AlreadyXConnected(Exception):
    pass

class NotXConnected(Exception):
    pass

class SelfXConnect(Exception):
    pass

class InsufficientAvailablePorts(Exception):
    pass

class InsufficientAvailableIPv4Space(Exception):
    pass

class InsufficientAvailableVLANSpace(Exception):
    pass

class CantHandleTransceiver(Exception):
    pass

