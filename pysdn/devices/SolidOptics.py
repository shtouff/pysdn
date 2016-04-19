from pysdn.devices import OpticalMux

class DWDMMux8CHUPG(OpticalMux):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.add_module(name='left',  channels=(28, 29, 30, 31, 32, 33, 34, 35), upgrade=True, monitor=False)
        self.add_module(name='right', channels=(28, 29, 30, 31, 32, 33, 34, 35), upgrade=True, monitor=False)

