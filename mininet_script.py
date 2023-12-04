from mininet.topo import Topo

class Star(Topo):
    def build(self):
        q = [self.addHost(f'h{i}') for i in range(4)]
        s = [self.addSwitch(f's{i}') for i in range(4)]
        l = [self.addLink(f'h{i}', f's{i}') for i in range(4)]
        ss = self.addSwitch('s0x')
        ssl = [self.addLink(f's{i}', 's0x') for i in range(4)]

topos = {'star': (lambda: Star())}