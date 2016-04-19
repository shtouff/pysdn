import unittest

from pysdn.devices import Port, Connector
from pysdn.devices.Cisco import ASR9001
from pysdn.cables import UTPCat6Patch

from pysdn.exceptions import SelfConnect

class TestPorts(unittest.TestCase):

    def test_cant_connect_to_self(self):
        p = Port(connector=Connector.RJ45, name='port')
        self.assertRaises(SelfConnect, p.connect, p, UTPCat6Patch())

class TestDevices(unittest.TestCase):

    def test_asr_has_a_console(self):
        asr = ASR9001(name='asr')
        self.assertIs(type(asr.get_port('console')), Port)

    def test_unkown_port(self):
        asr = ASR9001(name='asr')
        self.assertRaises(Exception, asr.get_port, 'unkn')

