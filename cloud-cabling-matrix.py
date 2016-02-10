#!/usr/bin/env python3

from pysdn.devices import PatchPanel, Switch, LineCard, Port
from pysdn.utils import CablingMatrix

def brasse_le_moins_2(matrix, p1, po1, po2):
    s1 = Switch(place='BETA R-2 right', u=10, name='sw-agg-1')
    s1.add_line_card(LineCard(connector=Port.LC, name='', portprefix='port', size=24))
    s2 = Switch(place='BETA R-2 right', u=11, name='sw-agg-2')
    s2.add_line_card(LineCard(connector=Port.LC, name='', portprefix='port', size=24))

    r1 = Switch(place='BETA R-2 right', u=7, name='edge-01')
    r1.add_line_card(LineCard(connector=Port.LC, name='', portprefix='sfpplus', size=8))
    r2 = Switch(place='BETA R-2 right', u=8, name='edge-02')
    r2.add_line_card(LineCard(connector=Port.LC, name='', portprefix='sfpplus', size=8))

    # we connect agg switches to panels
    for i in range(0, 9):
        s1.cards[0].ports[i].connect(p1.ports[2*i])
        s2.cards[0].ports[i].connect(p1.ports[2*i+1])
    # only 2 switches on R4b
    s1.cards[0].ports[8].disconnect()
    s2.cards[0].ports[8].disconnect()

    # interco sw-agg
    s1.cards[0].ports[21].connect(s2.cards[0].ports[21])

    # interco mikrotik
    r1.cards[0].ports[7].connect(r2.cards[0].ports[7])

    # external
    r1.cards[0].ports[0].connect(po1.ports[0])
    r2.cards[0].ports[0].connect(po2.ports[0])

    # add devices to matrix
    matrix.add_switch(s1)
    matrix.add_switch(s2)
    matrix.add_switch(r1)
    matrix.add_switch(r2)

def brasse_le_plus_3(matrix, uplinks):
    s1 = Switch(place='ALPHA R+3', u=9, name='1')
    s1.add_line_card(LineCard(connector=Port.LC, name='', portprefix='port', size=24))
    s2 = Switch(place='ALPHA R+3', u=11, name='2')
    s2.add_line_card(LineCard(connector=Port.LC, name='', portprefix='port', size=24))
    s3 = Switch(place='ALPHA R+3', u=13, name='3')
    s3.add_line_card(LineCard(connector=Port.LC, name='', portprefix='port', size=24))
    s4 = Switch(place='ALPHA R+3', u=15, name='4')
    s4.add_line_card(LineCard(connector=Port.LC, name='', portprefix='port', size=24))

    s1.cards[0].ports[22].connect(uplinks[0])
    s1.cards[0].ports[23].connect(uplinks[1])
    s2.cards[0].ports[22].connect(uplinks[2])
    s2.cards[0].ports[23].connect(uplinks[3])
    s3.cards[0].ports[23].connect(uplinks[4])
    s4.cards[0].ports[23].connect(uplinks[5])

    matrix.add_switch(s1)
    matrix.add_switch(s2)
    matrix.add_switch(s3)
    matrix.add_switch(s4)

def brasse_le_plus_4a(matrix, uplinks):
    s1 = Switch(place='BETA R+4a', u=9, name='1')
    s1.add_line_card(LineCard(connector=Port.LC, name='', portprefix='port', size=24))
    s2 = Switch(place='BETA R+4a', u=11, name='2')
    s2.add_line_card(LineCard(connector=Port.LC, name='', portprefix='port', size=24))
    s3 = Switch(place='BETA R+4a', u=13, name='3')
    s3.add_line_card(LineCard(connector=Port.LC, name='', portprefix='port', size=24))

    s1.cards[0].ports[22].connect(uplinks[0])
    s1.cards[0].ports[23].connect(uplinks[1])
    s2.cards[0].ports[22].connect(uplinks[2])
    s2.cards[0].ports[23].connect(uplinks[3])
    s3.cards[0].ports[22].connect(uplinks[4])
    s3.cards[0].ports[23].connect(uplinks[5])

    matrix.add_switch(s1)
    matrix.add_switch(s2)
    matrix.add_switch(s3)

def brasse_le_plus_4b(matrix, uplinks):
    s1 = Switch(place='BETA R+4b', u=7, name='1')
    s1.add_line_card(LineCard(connector=Port.LC, name='', portprefix='port', size=24))
    s2 = Switch(place='BETA R+4b', u=9, name='2')
    s2.add_line_card(LineCard(connector=Port.LC, name='', portprefix='port', size=24))

    s1.cards[0].ports[22].connect(uplinks[0])
    s1.cards[0].ports[23].connect(uplinks[1])
    s2.cards[0].ports[22].connect(uplinks[2])
    s2.cards[0].ports[23].connect(uplinks[3])

    matrix.add_switch(s1)
    matrix.add_switch(s2)

def main():
    m = CablingMatrix()

    po1 = PatchPanel(connector=Port.SC, place='BETA R-2 left', u=1, name='tiroir operateur1', size=12)
    po2 = PatchPanel(connector=Port.SC, place='BETA R-2 left', u=2, name='tiroir operateur2', size=12)
    p1 = PatchPanel(connector=Port.LC, place='BETA R-2 right', u=3, name='tiroir2', size=24)
    p2 = PatchPanel(connector=Port.LC, place='ALPHA R+3',u=1, name='tiroir1', size=6)
    p3 = PatchPanel(connector=Port.LC, place='ALPHA R+4a', u=1, name='tiroir1', size=6)
    p4 = PatchPanel(connector=Port.LC, place='ALPHA R+4b', u=1, name='tiroir1', size=6)

    # cross-co
    p1.multi_x_connect(position=1, peer=p2, peerPosition=1, size=6)
    p1.multi_x_connect(position=7, peer=p3, peerPosition=1, size=6)
    p1.multi_x_connect(position=13, peer=p4, peerPosition=1, size=6)

    brasse_le_moins_2(matrix=m, p1=p1, po1=po1, po2=po2)
    brasse_le_plus_3(matrix=m, uplinks=p2.ports)
    brasse_le_plus_4a(matrix=m, uplinks=p3.ports)
    brasse_le_plus_4b(matrix=m, uplinks=p4.ports)

    m.dump()

if __name__ == '__main__':
    main()




