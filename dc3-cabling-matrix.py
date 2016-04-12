#!/usr/bin/env python3

import math

from pysdn.devices import PatchPanel, Router, LineCard, Port, Rack
from pysdn.devices.Cisco import Nexus3064, Nexus3048, ASR9001
from pysdn.devices.Meraki import MS420
from pysdn.utils import CablingMatrix, IntercoMatrix, available_ports

def brasse_la_baie_telecom(matrix, rack):
    s1 = MS420(place='BETA R-2 right', u=10, name='sw-agg-1')
    s1.add_line_card(LineCard(connector=Port.LC, name='', portprefix='port', size=24))
    rack.rack(s1, u=6, height=2)

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

def brasse_le_plus_4a(matrix, uplinks):
    place = 'ALPHA R+4a'
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

    desks = 58
    agg_ports = available_ports(need=desks, devices=(s1, s2, s3, ))
    patch_ports = available_ports(need=desks, devices=(p1, p2, p3, ))

    for i in range(0, desks):
        agg_ports[i].connect(patch_ports[i])

    # patch wifi switch
    sw1 = MerakiMS220(place=place, u=15, name='wifi')
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
    s1 = MerakiMS420(place=place, u=7, name='1')
    s1.add_line_card(LineCard(connector=Port.LC, name='', portprefix='port', size=24))
    s2 = MerakiMS420(place=place, u=9, name='2')
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
    sw1 = MerakiMS220(place=place, u=11, name='wifi')
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
    s1 = MerakiMS420(place=place, u=7, name='1')
    s1.add_line_card(LineCard(connector=Port.LC, name='', portprefix='port', size=24))
    s2 = MerakiMS420(place=place, u=9, name='2')
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
    sw1 = MerakiMS220(place=place, u=11, name='wifi')
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

    # creation des racks
    r1 = Rack(name='DC3/baie-telecom')
    r2 = Rack(name='DC3/baie-srv2')
    r3 = Rack(name='DC3/baie-srv3')
    r4 = Rack(name='DC3/baie-srv4')
    r5 = Rack(name='DC3/baie-srv5')
    r6 = Rack(name='DC3/baie-srv6')
    r7 = Rack(name='DC3/baie-srv7')
    r8 = Rack(name='DC3/baie-srv8')

    ## FO ##
    # 96 FO => 48 duplex
    po1 = PatchPanel(connector=Port.LC, rack=r1, name='tiroir optique', size=96)
    r1.rack(po1, u=1, height=1)

    # 48 FO => 24 duplex
    po2 = PatchPanel(connector=Port.LC, rack=r2, name='tiroir optique', size=24)
    po3 = PatchPanel(connector=Port.LC, rack=r3, name='tiroir optique', size=24)
    po4 = PatchPanel(connector=Port.LC, rack=r3, name='tiroir optique', size=24)
    po5 = PatchPanel(connector=Port.LC, rack=r4, name='tiroir optique', size=24)
    po6 = PatchPanel(connector=Port.LC, rack=r5, name='tiroir optique', size=24)
    po7 = PatchPanel(connector=Port.LC, rack=r6, name='tiroir optique', size=24)
    po8 = PatchPanel(connector=Port.LC, rack=r7, name='tiroir optique', size=24)

    # cross-co telecom vers les baies srv
    po1.multi_x_connect(position=1, peer=po2, peerPosition=1, size=6)
    po1.multi_x_connect(position=7, peer=po3, peerPosition=1, size=6)
    po1.multi_x_connect(position=13, peer=po4, peerPosition=1, size=6)
    po1.multi_x_connect(position=19, peer=po5, peerPosition=1, size=6)
    po1.multi_x_connect(position=25, peer=po6, peerPosition=1, size=6)
    po1.multi_x_connect(position=31, peer=po7, peerPosition=1, size=6)
    po1.multi_x_connect(position=37, peer=po8, peerPosition=1, size=6)

    ## cuivre ##
    pc1 = PatchPanel(connector=Port.RJ45, rack=r1, name='tiroir cuivre', size=48)
    r1.rack(pc1, u=3, height=2)

    pc2 = PatchPanel(connector=Port.RJ45, rack=r2, name='tiroir cuivre', size=24)
    pc3 = PatchPanel(connector=Port.RJ45, rack=r3, name='tiroir cuivre', size=24)
    pc4 = PatchPanel(connector=Port.RJ45, rack=r4, name='tiroir cuivre', size=24)
    pc5 = PatchPanel(connector=Port.RJ45, rack=r5, name='tiroir cuivre', size=24)
    pc6 = PatchPanel(connector=Port.RJ45, rack=r6, name='tiroir cuivre', size=24)
    pc7 = PatchPanel(connector=Port.RJ45, rack=r7, name='tiroir cuivre', size=24)
    pc8 = PatchPanel(connector=Port.RJ45, rack=r8, name='tiroir cuivre', size=24)

    # cross-co telecom vers les baies srv
    pc1.multi_x_connect(position=1, peer=pc2, peerPosition=1, size=4)
    pc1.multi_x_connect(position=5, peer=pc3, peerPosition=1, size=4)
    pc1.multi_x_connect(position=9, peer=pc4, peerPosition=1, size=4)
    pc1.multi_x_connect(position=13, peer=pc5, peerPosition=1, size=4)
    pc1.multi_x_connect(position=17, peer=pc6, peerPosition=1, size=4)
    pc1.multi_x_connect(position=21, peer=pc7, peerPosition=1, size=4)
    pc1.multi_x_connect(position=25, peer=pc8, peerPosition=1, size=4)


    ## brassage ##
    brasse_la_baie_telecom(matrix=m, rack=r1)
    #brasse_le_moins_2(matrix=m, po1=po1, po2=po2, downlinks=(pb2.ports[0:6] + pb2.ports[6:12] + pb2.ports[12:16] + pb1.ports[0:4]))
    #brasse_le_plus_3(matrix=m, uplinks=p2.ports)
    #brasse_le_plus_4a(matrix=m, uplinks=p3.ports)
    #brasse_le_plus_4b(matrix=m, uplinks=p4.ports)
    #brasse_le_rdj(matrix=m, uplinks=p5.ports)

    #m.dump()

if __name__ == '__main__':
    main()

