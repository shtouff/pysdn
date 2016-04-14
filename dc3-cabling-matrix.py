#!/usr/bin/env python3

import math

from pysdn.devices import PatchPanel, Router, LineCard, Port, Rack
from pysdn.devices.Cisco import Nexus3064, Nexus3048, ASR9001
from pysdn.devices.Opengear import CM4132
from pysdn.utils import CablingMatrix, IntercoMatrix, available_ports

def brasse_la_baie_telecom():
    # creation des racks
    r = Rack(name='DC3/baie-telecom')

    ## FO ##
    # 96 FO => 48 duplex
    po = PatchPanel(connector=Port.LC, name='po', size=48)
    r.rack(po, u=1, height=1)

    ## cuivre ##
    pc = PatchPanel(connector=Port.RJ45, name='pc', size=48)
    r.rack(pc, u=3, height=2)

    return r

def brasse_la_baie_serveur():
    r = Rack(name='DC3/baie-srv2')

    po = PatchPanel(connector=Port.LC, name='po', size=24)
    r.rack(po, u=1, height=1)

    pc = PatchPanel(connector=Port.RJ45, name='pc', size=24)
    r.rack(pc, u=3, height=1)

    # 23 et 25
    nex1 = Nexus3048(name='sw-acc-XXX-01')
    nex1.add_line_card(LineCard(connector=Port.RJ45, name='copper', portprefix='Eth1/', base=1, size=48))
    nex1.add_line_card(LineCard(connector=Port.RJ45, name='copper', portprefix='Eth1/', base=49, size=4))
    r.rack(nex1, u=23, height=1)

    nex2 = Nexus3048(name='sw-acc-XXX-02')
    nex2.add_line_card(LineCard(connector=Port.RJ45, name='copper', portprefix='Eth1/', base=1, size=48))
    nex2.add_line_card(LineCard(connector=Port.RJ45, name='copper', portprefix='Eth1/', base=49, size=4))
    r.rack(nex2, u=25, height=1)

    return r

def brasse_le_moins_2(matrix, po1, po2, downlinks):
    s1 = MerakiMS420(place='BETA R-2 right', u=10, name='sw-agg-1')
    s1.add_line_card(LineCard(connector=Port.LC, name='', portprefix='port', size=24))
    s2 = MerakiMS420(place='BETA R-2 right', u=11, name='sw-agg-2')
    s2.add_line_card(LineCard(connector=Port.LC, name='', portprefix='port', size=24))

    r1 = Router(place='BETA R-2 right', u=7, name='edge-01')
    r1.add_line_card(LineCard(connector=Port.LC, name='', portprefix='sfpplus', size=8))
    r2 = Router(place='BETA R-2 right', u=8, name='edge-02')
    r2.add_line_card(LineCard(connector=Port.LC, name='', portprefix='sfpplus', size=8))

    # we connect agg switches to panels
    for i in range(0, math.ceil(len(downlinks) / 2)):
        s1.cards[0].ports[i].connect(downlinks[2*i])
        s2.cards[0].ports[i].connect(downlinks[2*i+1])

    # interco sw-agg
    s1.cards[0].ports[21].connect(s2.cards[0].ports[21])

    # interco mikrotik
    r1.cards[0].ports[7].connect(r2.cards[0].ports[7])

    # operators
    r1.cards[0].ports[0].connect(po1.ports[0])
    r2.cards[0].ports[0].connect(po2.ports[0])

    # add devices to matrix
    matrix.add_switch(s1)
    matrix.add_switch(s2)
    matrix.add_switch(r1)
    matrix.add_switch(r2)

def brasse_le_plus_3(matrix, uplinks):
    place = 'ALPHA R+3'
    s1 = MerakiMS420(place=place, u=9, name='1')
    s1.add_line_card(LineCard(connector=Port.LC, name='', portprefix='port', size=24))
    s2 = MerakiMS420(place=place, u=11, name='2')
    s2.add_line_card(LineCard(connector=Port.LC, name='', portprefix='port', size=24))
    s3 = MerakiMS420(place=place, u=13, name='3')
    s3.add_line_card(LineCard(connector=Port.LC, name='', portprefix='port', size=24))

    s1.cards[0].ports[22].connect(uplinks[0])
    s1.cards[0].ports[23].connect(uplinks[1])
    s2.cards[0].ports[22].connect(uplinks[2])
    s2.cards[0].ports[23].connect(uplinks[3])
    s3.cards[0].ports[22].connect(uplinks[4])
    s3.cards[0].ports[23].connect(uplinks[5])

    # patch desktop switches
    p1 = PatchPanel(connector=Port.LC, place=place, u=3, name='', size=24)
    p2 = PatchPanel(connector=Port.LC, place=place, u=5, name='', size=24)
    p3 = PatchPanel(connector=Port.LC, place=place, u=7, name='', size=24)

    desks = 65
    agg_ports = available_ports(need=desks, devices=(s1, s2, s3, ))
    patch_ports = available_ports(need=desks, devices=(p1, p2, p3, ))

    for i in range(0, desks):
        agg_ports[i].connect(patch_ports[i])

    # patch wifi switch
    sw1 = MerakiMS220(place=place, u=17, name='wifi')
    sw1.add_line_card(LineCard(connector=Port.RJ45, name='', portprefix='port', size=24))
    agg_ports = available_ports(need=1, devices=(s1, s2, s3, ))
    sw1.cards[0].ports[23].connector = Port.LC
    sw1.cards[0].ports[23].connect(agg_ports[-1])

    pc1 = PatchPanel(connector=Port.RJ45, place=place, u=20, name='tiroir cuivre', size=24)
    wifis = 10
    agg_ports = available_ports(need=wifis, devices=(sw1, ))
    patch_ports = available_ports(need=wifis, devices=(pc1, ))

    for i in range(0, wifis):
        agg_ports[i].connect(patch_ports[i])

    matrix.add_switch(s1)
    matrix.add_switch(s2)
    matrix.add_switch(s3)
    matrix.add_switch(sw1)

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

    #m.add_rack(r1)
    #m.add_rack(r2)
    #m.dump()

if __name__ == '__main__':
    main()

