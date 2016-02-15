#!/usr/bin/env python3

import math

from pysdn.devices import PatchPanel, Switch, LineCard, Port
from pysdn.utils import CablingMatrix, available_ports

def brasse_le_moins_2(matrix, po1, po2, downlinks):
    s1 = Switch(place='BETA R-2 right', u=10, name='sw-agg-1')
    s1.add_line_card(LineCard(connector=Port.LC, name='', portprefix='port', size=24))
    s2 = Switch(place='BETA R-2 right', u=11, name='sw-agg-2')
    s2.add_line_card(LineCard(connector=Port.LC, name='', portprefix='port', size=24))

    r1 = Switch(place='BETA R-2 right', u=7, name='edge-01')
    r1.add_line_card(LineCard(connector=Port.LC, name='', portprefix='sfpplus', size=8))
    r2 = Switch(place='BETA R-2 right', u=8, name='edge-02')
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
    s1 = Switch(place=place, u=9, name='1')
    s1.add_line_card(LineCard(connector=Port.LC, name='', portprefix='port', size=24))
    s2 = Switch(place=place, u=11, name='2')
    s2.add_line_card(LineCard(connector=Port.LC, name='', portprefix='port', size=24))
    s3 = Switch(place=place, u=13, name='3')
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
    sw1 = Switch(place=place, u=17, name='wifi')
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

def brasse_le_plus_4a(matrix, uplinks):
    place = 'ALPHA R+4a'
    s1 = Switch(place=place, u=9, name='1')
    s1.add_line_card(LineCard(connector=Port.LC, name='', portprefix='port', size=24))
    s2 = Switch(place=place, u=11, name='2')
    s2.add_line_card(LineCard(connector=Port.LC, name='', portprefix='port', size=24))
    s3 = Switch(place=place, u=13, name='3')
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

    desks = 58
    agg_ports = available_ports(need=desks, devices=(s1, s2, s3, ))
    patch_ports = available_ports(need=desks, devices=(p1, p2, p3, ))

    for i in range(0, desks):
        agg_ports[i].connect(patch_ports[i])

    # patch wifi switch
    sw1 = Switch(place=place, u=15, name='wifi')
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

def brasse_le_plus_4b(matrix, uplinks):
    place = 'ALPHA R+4b'
    s1 = Switch(place=place, u=7, name='1')
    s1.add_line_card(LineCard(connector=Port.LC, name='', portprefix='port', size=24))
    s2 = Switch(place=place, u=9, name='2')
    s2.add_line_card(LineCard(connector=Port.LC, name='', portprefix='port', size=24))

    s1.cards[0].ports[22].connect(uplinks[0])
    s1.cards[0].ports[23].connect(uplinks[1])
    s2.cards[0].ports[22].connect(uplinks[2])
    s2.cards[0].ports[23].connect(uplinks[3])

    # patch desktop switches
    p1 = PatchPanel(connector=Port.LC, place=place, u=3, name='', size=24)
    p2 = PatchPanel(connector=Port.LC, place=place, u=5, name='', size=24)

    desks = 30
    agg_ports = available_ports(need=desks, devices=(s1, s2, ))
    patch_ports = available_ports(need=desks, devices=(p1, p2, ))

    for i in range(0, desks):
        agg_ports[i].connect(patch_ports[i])

    # patch wifi switch
    sw1 = Switch(place=place, u=11, name='wifi')
    sw1.add_line_card(LineCard(connector=Port.RJ45, name='', portprefix='port', size=24))
    agg_ports = available_ports(need=1, devices=(s1, s2, ))
    sw1.cards[0].ports[23].connector = Port.LC
    sw1.cards[0].ports[23].connect(agg_ports[-1])

    pc1 = PatchPanel(connector=Port.RJ45, place=place, u=20, name='tiroir cuivre', size=24)
    wifis = 5
    agg_ports = available_ports(need=wifis, devices=(sw1, ))
    patch_ports = available_ports(need=wifis, devices=(pc1, ))

    for i in range(0, wifis):
        agg_ports[i].connect(patch_ports[i])

    matrix.add_switch(s1)
    matrix.add_switch(s2)
    matrix.add_switch(sw1)

def brasse_le_rdj(matrix, uplinks):
    place = 'ALPHA RDJ'
    s1 = Switch(place=place, u=7, name='1')
    s1.add_line_card(LineCard(connector=Port.LC, name='', portprefix='port', size=24))
    s2 = Switch(place=place, u=9, name='2')
    s2.add_line_card(LineCard(connector=Port.LC, name='', portprefix='port', size=24))

    s1.cards[0].ports[22].connect(uplinks[0])
    s1.cards[0].ports[23].connect(uplinks[1])
    s2.cards[0].ports[22].connect(uplinks[2])
    s2.cards[0].ports[23].connect(uplinks[3])

    # patch desktop switches
    p1 = PatchPanel(connector=Port.LC, place=place, u=3, name='', size=24)
    p2 = PatchPanel(connector=Port.LC, place=place, u=5, name='', size=24)

    desks = 23
    agg_ports = available_ports(need=desks, devices=(s1, s2, ))
    patch_ports = available_ports(need=desks, devices=(p1, p2, ))

    for i in range(0, desks):
        agg_ports[i].connect(patch_ports[i])

    # patch wifi switch
    sw1 = Switch(place=place, u=11, name='wifi')
    sw1.add_line_card(LineCard(connector=Port.RJ45, name='', portprefix='port', size=24))
    agg_ports = available_ports(need=1, devices=(s1, s2, ))
    sw1.cards[0].ports[23].connector = Port.LC
    sw1.cards[0].ports[23].connect(agg_ports[-1])

    pc1 = PatchPanel(connector=Port.RJ45, place=place, u=20, name='tiroir cuivre', size=24)
    wifis = 7
    agg_ports = available_ports(need=wifis, devices=(sw1, ))
    patch_ports = available_ports(need=wifis, devices=(pc1, ))

    for i in range(0, wifis):
        agg_ports[i].connect(patch_ports[i])

    matrix.add_switch(s1)
    matrix.add_switch(s2)
    matrix.add_switch(sw1)

def main():
    m = CablingMatrix()

    po1 = PatchPanel(connector=Port.SC, place='BETA R-2 left', u=1, name='tiroir operateur1', size=12)
    po2 = PatchPanel(connector=Port.SC, place='BETA R-2 left', u=2, name='tiroir operateur2', size=12)

    # basement / -2
    pb1 = PatchPanel(connector=Port.LC, place='BETA R-2 right', u=1, name='tiroir1', size=24)
    pb2 = PatchPanel(connector=Port.LC, place='BETA R-2 right', u=3, name='tiroir2', size=24)

    # floors
    p2 = PatchPanel(connector=Port.LC, place='ALPHA R+3',u=1, name='tiroir1', size=6)
    p3 = PatchPanel(connector=Port.LC, place='ALPHA R+4a', u=1, name='tiroir1', size=6)
    p4 = PatchPanel(connector=Port.LC, place='ALPHA R+4b', u=1, name='tiroir1', size=6)
    p5 = PatchPanel(connector=Port.LC, place='ALPHA RDJ', u=1, name='tiroir1', size=6)
    #p6 = PatchPanel(connector=Port.LC, place='ALPHA RDC', u=1, name='tiroir1', size=6)

    # cross-co
    pb1.multi_x_connect(position=1, peer=p5, peerPosition=1, size=6)
    #pb1.multi_x_connect(position=7, peer=p6, peerPosition=1, size=6)
    pb2.multi_x_connect(position=1, peer=p2, peerPosition=1, size=6)
    pb2.multi_x_connect(position=7, peer=p3, peerPosition=1, size=6)
    pb2.multi_x_connect(position=13, peer=p4, peerPosition=1, size=6)

    # brassage
    brasse_le_moins_2(matrix=m, po1=po1, po2=po2, downlinks=(pb2.ports[0:6] + pb2.ports[6:12] + pb2.ports[12:16] + pb1.ports[0:4]))
    brasse_le_plus_3(matrix=m, uplinks=p2.ports)
    brasse_le_plus_4a(matrix=m, uplinks=p3.ports)
    brasse_le_plus_4b(matrix=m, uplinks=p4.ports)
    brasse_le_rdj(matrix=m, uplinks=p5.ports)

    m.dump()

if __name__ == '__main__':
    main()

