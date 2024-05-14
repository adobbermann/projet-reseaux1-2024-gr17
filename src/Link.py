class Link:
    def __init__(self, connected_nodes, propagation_speed=2e8, transmission_rate=1000):
        self.connected_nodes = connected_nodes
        self.propagation_speed = propagation_speed
        self.transmission_rate = transmission_rate

    def propagation_delay(self):
        return sum([1 / self.propagation_speed for _ in self.connected_nodes])

    def transmission_delay(self, packets):
        bits = 0
        # print(f'packets: {packets[0]}')
        if (len(packets) > 1):
            for packet in packets:
                bits += len(packet)*8
        else:
            bits += len(packets[0])*8

        return bits / self.transmission_rate

    def get_nodes(self):
        return self.connected_nodes
