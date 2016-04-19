

class Cable(object):
    def __init__(self, **kwargs):
        if 'length' in kwargs:
            self.length = kwargs['length']
        else:
            self.length = 1

class LCLCDuplexPatch(Cable):
    pass

class SCLCDuplexPatch(Cable):
    pass

class UTPCat6Patch(Cable):
    pass

#class SimplexFiber(Cable):
#    pass
#
#class DuplexFiber(Cable):
#    pass
#
#class RJ45(Cable):
#    pass
