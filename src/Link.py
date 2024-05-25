class Link:
    def __init__(self, connected_nodes, distance=5, propagation_speed=2e8, transmission_rate=100):
        self.distance = distance
        self.connected_nodes = connected_nodes
        self.propagation_speed = propagation_speed
        self.transmission_rate = transmission_rate

    def propagation_delay(self):
        return self.distance / self.propagation_speed

    def transmission_delay(self, packets, bitrate):
        bits = 0
        # print(f'packets: {packets}')
        if (len(packets) > 1):
            for packet in packets:
                bits += len(packet)*8
        else:
            bits += len(packets[0])*8
        print(f'Packets: {packets} | bits: {bits} | bitrate: {bitrate}')
        return bits / bitrate

    def get_nodes(self):
        return self.connected_nodes
