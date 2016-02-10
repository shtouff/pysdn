from pysdn.devices import Switch, Port, PatchPort

class CablingMatrix(object):

    def __init__(self):
        self.seenports = []
        self.devices = []

    def add_switch(self, switch):
        if not isinstance(switch, Switch):
            raise Exception('Switch expected')

        self.devices.append(switch)

    def dump(self):
        print('rack;U;switch;port;rack;U;panel;port;<==>;rack;U;panel;port;rack;U;switch;port')
        for device in self.devices:
            if isinstance(device, Switch):
                self.dump_switch(device)

    def dump_patch_port(self, port):

        portA = port
        panelA = portA.owner
        print(';{};{};{};{}'.format(panelA.place, panelA.u, panelA.name, portA), end='')
        print(';<==>', end='')

        portB = portA.x_port
        if portB is None:
            print(';;;;', end='')
        else:
            panelB = portB.owner
            print(';{};{};{};{}'.format(panelB.place, panelB.u, panelB.name, portB), end='')

    def dump_switch_port(self, port):
        if port in self.seenports:
            return
        if port.p_port is None:
            return

        portA = port
        cardA = portA.owner
        switchA = cardA.owner
        print('{};{};{};{}{}'.format(switchA.place, switchA.u, switchA.name, cardA, portA), end='')
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

        cardB = portB.owner
        switchB = cardB.owner
        print(';{};{};{};{}{}'.format(switchB.place, switchB.u, switchB.name, cardB, portB))
        self.seenports.append(portB)

    def dump_switch(self, switch):
        for card in switch.cards:
            for port in card.ports:
                self.dump_switch_port(port)
