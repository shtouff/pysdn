from pysdn.devices import ActiveNetworkDevice, L3Switch, Switch, Port, PatchPort, PatchPanel, Rack
from pysdn.exceptions import InsufficientAvailablePorts, InsufficientAvailableIPv4Space, InsufficientAvailableVLANSpace

from ipaddress import IPv4Network

class IntercoMatrix(object):

    ipv4_space = []
    vlan_space = []
    seenports = []

    def __init__(self, **kwargs):
        if 'cabling_matrix' in kwargs:
            self.set_cabling_matrix(kwargs['cabling_matrix'])

        if 'ipv4_space' in kwargs:
            self.set_ipv4_space(kwargs['ipv4_space'])

        if 'vlan_space' in kwargs:
            self.set_vlan_space(kwargs['vlan_space'])

    def set_cabling_matrix(self, cm):
        if not isinstance(cm, CablingMatrix):
            raise Exception('CablinMatric expected')

        self.cabling_matrix = cm

    def set_vlan_space(self, vlans):
        self.vlan_space = vlans

    def add_vlan_space(self, vlan):
        self.vlan_space.append(vlan)

    def get_next_vlan(self):
        try:
            return self.vlan_space.pop(0)
        except IndexError as e:
            raise InsufficientAvailableVLANSpace()

    def set_ipv4_space(self, network):
        if not isinstance(network, IPv4Network):
            raise Exception('IPv4Network expected')

        self.ipv4_space = []
        self.add_ipv4_space(network)

    def add_ipv4_space(self, network):
        if not isinstance(network, IPv4Network):
            raise Exception('IPv4Network expected')

        for subnet in network.subnets(new_prefix=30):
            self.ipv4_space.append(subnet)

    def get_next_interco(self):
        try:
            return self.ipv4_space.pop(0)
        except IndexError as e:
            raise InsufficientAvailableIPv4Space()

    def dump(self):
        print('rack;U;switch;port;<==>;rack;U;switch;port;interco /30;vlan;ospf active;ospf cost')
        for device in self.cabling_matrix.devices:
            if isinstance(device, L3Switch):
                self.dump_switch(device)

    def dump_switch_port(self, port):
        if port in self.seenports:
            return
        if port.p_port is None:
            return

        portA = port
        cardA = portA.owner
        switchA = cardA.owner
        rackA = switchA.owner
        ret = '{};U{};{};{}{}'.format(rackA, switchA.u, switchA.name, cardA, portA)
        self.seenports.append(portA)

        if isinstance(portA.p_port, PatchPort):
            if portA.p_port.x_port is None:
                return
            else:
                portB = portA.p_port.x_port.p_port
        else:
            portB = portA.p_port

        cardB = portB.owner
        switchB = cardB.owner
        rackB = switchB.owner

        if not isinstance(switchB, L3Switch):
            return

        ret += ';<==>;{};U{};{};{}{}'.format(rackB, switchB.u, switchB.name, cardB, portB)
        self.seenports.append(portB)

        ret += ';{};{};active;10'.format(self.get_next_interco(), self.get_next_vlan())

        print(ret)

    def dump_switch(self, switch):
        for card in switch.cards:
            for port in card.ports:
                self.dump_switch_port(port)

class CablingMatrix(object):

    def __init__(self):
        self.seenports = []
        self.devices = []

    def add_switch(self, switch):
        self.add_device(switch)

    def add_device(self, device):
        if not isinstance(device, ActiveNetworkDevice):
            raise Exception('ActiveNetworkDevice expected')

        self.devices.append(device)

    def add_rack(self, rack):
        if not isinstance(rack, Rack):
            raise Exception('Rack expected')

        for device in rack.devices.values():
            self.devices.append(device)

    def dump(self):
        print('rack;U;switch;port;rack;U;panel;port;<==>;rack;U;panel;port;rack;U;switch;port')
        for device in self.devices:
            if isinstance(device, ActiveNetworkDevice):
                self.dump_switch(device)

    def dump_patch_port(self, port):

        portA = port
        panelA = portA.owner
        rackA = panelA.owner
        print(';{};U{};{};{}'.format(rackA, panelA.u, panelA.name, portA), end='')
        print(';<==>', end='')

        portB = portA.x_port
        if portB is None:
            print(';;;;', end='')
        else:
            panelB = portB.owner
            rackB = panelB.owner
            print(';{};U{};{};{}'.format(rackB, panelB.u, panelB.name, portB), end='')

    def dump_switch_port(self, port):
        if port in self.seenports:
            return
        if port.p_port is None:
            return

        portA = port
        cardA = portA.owner
        switchA = cardA.owner
        rackA = switchA.owner
        print('{};U{};{};{}{}'.format(rackA, switchA.u, switchA.name, cardA, portA), end='')
        self.seenports.append(portA)

        if isinstance(portA.p_port, PatchPort):
            self.dump_patch_port(portA.p_port)

            if portA.p_port.x_port is None:
                print(';;;;')
                return
            else:
                portB = portA.p_port.x_port.p_port
        else:
            print(';;;;', end='')
            print(';<==>', end='')
            print(';;;;', end='')
            portB = portA.p_port

        if portB is None:
            raise Exception('this port is not connected')
        cardB = portB.owner
        switchB = cardB.owner
        rackB = switchB.owner
        print(';{};U{};{};{}{}'.format(rackB, switchB.u, switchB.name, cardB, portB))
        self.seenports.append(portB)

    def dump_switch(self, switch):
        for card in switch.cards.values():
            for port in card.ports:
                self.dump_switch_port(port)

def available_ports(need, devices):

    avail = []
    for device in devices:
        if isinstance(device, ActiveNetworkDevice):
            for card in device.cards:
                for port in card.ports:
                    if port.p_port is None:
                        avail.append(port)
        elif isinstance(device, PatchPanel):
            for port in device.ports:
                if port.p_port is None:
                    avail.append(port)

    if len(avail) < need:
        raise InsufficientAvailablePorts()

    return avail

