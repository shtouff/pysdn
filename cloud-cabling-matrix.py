#!/usr/bin/env python3

from pysdn.devices import PatchPanel, Switch, LineCard, Port
from pysdn.utils import CablingMatrix

def main():

    # cross-co
    po1 = PatchPanel(connector=Port.SC, place='BETA R-2 left', u=1, name='tiroir operateur', size=12)
    po2 = PatchPanel(connector=Port.SC, place='BETA R-2 left', u=2, name='tiroir operateur', size=12)
    p1 = PatchPanel(connector=Port.LC, place='BETA R-2 right', u=3, name='tiroir2', size=24)
    p2 = PatchPanel(connector=Port.LC, place='ALPHA R+3',u=1, name='tiroir1', size=6)
    p3 = PatchPanel(connector=Port.LC, place='ALPHA R+4a', u=1, name='tiroir1', size=6)
    p4 = PatchPanel(connector=Port.LC, place='ALPHA R+4b', u=1, name='tiroir1', size=6)

    p1.multi_x_connect(position=1, peer=p2, peerPosition=1, size=6)
    p1.multi_x_connect(position=7, peer=p3, peerPosition=1, size=6)
    p1.multi_x_connect(position=13, peer=p4, peerPosition=1, size=6)

    # -2
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

    # r+3
    r3s1 = Switch(place='ALPHA R+3', u=9, name='1')
    r3s1.add_line_card(LineCard(connector=Port.LC, name='', portprefix='port', size=24))
    r3s2 = Switch(place='ALPHA R+3', u=11, name='2')
    r3s2.add_line_card(LineCard(connector=Port.LC, name='', portprefix='port', size=24))
    r3s3 = Switch(place='ALPHA R+3', u=13, name='3')
    r3s3.add_line_card(LineCard(connector=Port.LC, name='', portprefix='port', size=24))
    r3s4 = Switch(place='ALPHA R+3', u=15, name='4')
    r3s4.add_line_card(LineCard(connector=Port.LC, name='', portprefix='port', size=24))

    r3s1.cards[0].ports[22].connect(p2.ports[0])
    r3s1.cards[0].ports[23].connect(p2.ports[1])
    r3s2.cards[0].ports[22].connect(p2.ports[2])
    r3s2.cards[0].ports[23].connect(p2.ports[3])
    r3s3.cards[0].ports[23].connect(p2.ports[4])
    r3s4.cards[0].ports[23].connect(p2.ports[5])

    # r+4a
    r4as1 = Switch(place='BETA R+4a', u=9, name='1')
    r4as1.add_line_card(LineCard(connector=Port.LC, name='', portprefix='port', size=24))
    r4as2 = Switch(place='BETA R+4a', u=11, name='2')
    r4as2.add_line_card(LineCard(connector=Port.LC, name='', portprefix='port', size=24))
    r4as3 = Switch(place='BETA R+4a', u=13, name='3')
    r4as3.add_line_card(LineCard(connector=Port.LC, name='', portprefix='port', size=24))

    r4as1.cards[0].ports[22].connect(p3.ports[0])
    r4as1.cards[0].ports[23].connect(p3.ports[1])
    r4as2.cards[0].ports[22].connect(p3.ports[2])
    r4as2.cards[0].ports[23].connect(p3.ports[3])
    r4as3.cards[0].ports[22].connect(p3.ports[4])
    r4as3.cards[0].ports[23].connect(p3.ports[5])

    # r+4b
    r4bs1 = Switch(place='BETA R+4b', u=7, name='1')
    r4bs1.add_line_card(LineCard(connector=Port.LC, name='', portprefix='port', size=24))
    r4bs2 = Switch(place='BETA R+4b', u=9, name='2')
    r4bs2.add_line_card(LineCard(connector=Port.LC, name='', portprefix='port', size=24))

    r4bs1.cards[0].ports[22].connect(p4.ports[0])
    r4bs1.cards[0].ports[23].connect(p4.ports[1])
    r4bs2.cards[0].ports[22].connect(p4.ports[2])
    r4bs2.cards[0].ports[23].connect(p4.ports[3])

    # creating cabling matrix
    m = CablingMatrix()
    m.add_switch(s1)
    m.add_switch(s2)
    m.add_switch(r1)
    m.add_switch(r2)

    m.dump()

if __name__ == '__main__':
    main()





