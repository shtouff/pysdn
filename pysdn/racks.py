
class Rack(object):

    # 47 U
    DEFAULT_HEIGHT = 47
    name = None
    u = None
    devices = None

    def __init__(self, **kwargs):
        self.name = kwargs['name']

        if 'height' in kwargs:
            self.height = kwargs['height']
        else:
            self.height = self.DEFAULT_HEIGHT

        self.devices = {}
        self.u = {}

    def rack(self, device, u):
        for pos in range(u, u+device.height):
            if pos in self.u:
                raise Exception('This rack position is already occupied')

        du =[]
        for pos in range(u, u+device.height):
            self.u[pos] = device
            du.append(pos)

        self.devices[device.name] = device
        device.owner = self
        device.u = ','.join(map(str,du))

    def __str__(self):
        return self.name

