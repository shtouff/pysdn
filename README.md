

Some examples. Create 2 patch panels in different racks:

```python
from pysdn.devices import PatchPanel, Switch, LineCard, Port
from pysdn.utils import available_ports

po1 = PatchPanel(connector=Port.SC, place='rack1', u=1, name='patch panel', size=12)
po2 = PatchPanel(connector=Port.SC, place='rack2', u=1, name='patch panel', size=12)
```

Cross-connect them, with a breakout of 6 duplex:

```python
po1.multi_x_connect(position=1, peer=po2, peerPosition=1, size=6)
```

Add a switch on each rack, with a 24 SFP capacity:

```python
s1 = Switch(place='rack1', u=10, name='switch1')
s1.add_line_card(LineCard(connector=Port.LC, name='', portprefix='Gi0/', base=0, size=24))

s2 = Switch(place='rack2', u=10, name='switch2')
s2.add_line_card(LineCard(connector=Port.LC, name='', portprefix='Gi0/', base=0, size=24))
```

Connect them via the first cross-connect available, and using the last switching port

```python
sw_ports = available_ports(need=1, devices=(s1, ))
sw_ports[-1].connect(po1.ports[0])

sw_ports = available_ports(need=1, devices=(s2, ))
sw_ports[-1].connect(po2.ports[0])
```

Creates a cabling matrix from these switches, and dump it, using CSV:

```python
from pysdn.utils import CablingMatrix

m = CablingMatrix()
m.add_switch(s1)
m.add_switch(s2)

m.dump()
```

That will produce:

    rack;U;switch;port;rack;U;panel;port;<==>;rack;U;panel;port;rack;U;switch;port
    rack1;U10;switch1;Gi0/23;rack1;U1;patch panel;port1;<==>;rack2;U1;patch panel;port1;rack2;U10;switch2;Gi0/23
