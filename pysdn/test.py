import unittest

from pysdn.devices import Port, Connector, Transceiver
from pysdn.devices.Cisco import ASR9001
from pysdn.cables import UTPCat6Patch
from pysdn.transceivers import SFPPlus

from pysdn.exceptions import SelfConnect, CantHandleTransceiver

class TestPorts(unittest.TestCase):

    def test_cant_connect_to_self(self):
        p = Port(connector=Connector.RJ45, name='port')
        self.assertRaises(SelfConnect, p.connect, p, UTPCat6Patch())

    def test_port_cant_handle_sfp(self):
        p = Port(connector=Connector.RJ45, name='port')
        self.assertRaises(CantHandleTransceiver, p.set_transceiver, SFPPlus())

    def test_port_can_handle_sfp(self):
        p = Port(connector=Connector.SFPPLUS, name='port')
        p.set_transceiver(SFPPlus())
        self.assertIs(type(p.get_transceiver()), SFPPlus)
        self.assertIsInstance(p.get_transceiver(), Transceiver)

class TestDevices(unittest.TestCase):

    def test_asr_has_a_console(self):
        asr = ASR9001(name='asr')
        self.assertIs(type(asr.get_port('console')), Port)

    def test_unkown_port(self):
        asr = ASR9001(name='asr')
        self.assertRaises(Exception, asr.get_port, 'unkn')

