#!/usr/bin/env python3

import math

from pysdn.devices import PatchPanel, Router, LineCard, Port, Rack, Connector
from pysdn.devices.Cisco import Nexus3064_X, Nexus3048, ASR9001, SF300_24
from pysdn.devices.Opengear import CM4132
from pysdn.utils import CablingMatrix, IntercoMatrix, available_ports

def brasse_la_baie_telecom():
    # creation des racks
    r = Rack(name='DC3/4.2/F23')

    ## FO ##
    # 96 FO => 48 duplex
    po = PatchPanel(connector=Connector.LC, name='po', size=48)
    r.rack(po, u=1, height=1)

    pop = PatchPanel(connector=Connector.LC, name='pop', size=24)
    r.rack(pop, u=3, height=1)

    # 5-6: ASR1
    asr1 = ASR9001(name='core-01')
    asr1.add_module(LineCard(connector=Connector.LC, name='R/SFP', base=0, size=20))
    asr1.add_module(LineCard(connector=Connector.LC, name='L/XFP', base=0, size=4))
    r.rack(asr1, u=5, height=2)
    # 8-9: ASR2
    asr2 = ASR9001(name='core-02')
    asr2.add_module(LineCard(connector=Connector.LC, name='R/SFP', base=0, size=20))
    asr2.add_module(LineCard(connector=Connector.LC, name='L/XFP', base=0, size=4))
    r.rack(asr2, u=8, height=2)

    # 11: mux

    # 13: dist1
    nex1 = Nexus3064_X(name='dist-01')
    r.rack(nex1, u=13, height=1)
    # 15: dist2
    nex2 = Nexus3064_X(name='dist-02')
    r.rack(nex2, u=15, height=1)

    # 17-18: arbor

    # 20: oob
    sf = SF300_24(name='sw-oob')
    r.rack(sf, u=20, height=1)

    # 22: console
    og = CM4132(name='console')
    r.rack(og, u=22, height=1)

    # 24-25: cuivre
    pc = PatchPanel(connector=Connector.RJ45, name='pc', size=48)
    r.rack(pc, u=24, height=2)

    # brassage console
    for (port, device) in ( ('port1', asr1), ('port2', asr2), ('port3', nex1), ('port4', nex2) ):
        og.get_port(port).connect(device.get_port('console'))

    return r

def brasse_la_baie_serveur():
    r = Rack(name='DC3/baie-srv2')

    # u1 & u2: patch panels
    po = PatchPanel(connector=Connector.LC, name='po', size=24)
    r.rack(po, u=1, height=1)

    pc = PatchPanel(connector=Connector.RJ45, name='pc', size=24)
    r.rack(pc, u=2, height=1)

    # u24 & u26: nexus 3048 switches
    nex1 = Nexus3048(name='sw-acc-XXX-01')
    r.rack(nex1, u=24, height=1)

    nex2 = Nexus3048(name='sw-acc-XXX-02')
    r.rack(nex2, u=26, height=1)

    nex1.get_port('Eth1/48').connect(nex2.get_port('Eth1/48'))
    #nex1.get_port('Eth1/1').connect(pc.ports[1])

    return r

def main():
    m = CablingMatrix()

    ## brassage ##
    r1 = brasse_la_baie_telecom()
    r2 = brasse_la_baie_serveur()

    # cross-co telecom vers les baies srv
    o_size = 6
    c_size = 4
    o_off = c_off = 1

    for rack in (r2, ):
        r1.devices['po'].multi_x_connect(position=1, peer=rack.devices['po'], peerPosition=1, size=o_size)
        r1.devices['pc'].multi_x_connect(position=1, peer=rack.devices['pc'], peerPosition=1, size=c_size)
        o_size += o_off
        c_size += c_off

    m.add_rack(r1)
    m.add_rack(r2)
#    m.dump()

if __name__ == '__main__':
    main()

