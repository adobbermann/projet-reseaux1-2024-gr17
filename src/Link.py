class Link:
    def __init__(self, distance, propagation_speed=2e8, transmission_rate=1000):
        self.distance = distance
        self.propagation_speed = propagation_speed
        self.transmission_rate = transmission_rate

    # l/r
    def transmission_delay(self, packet_size):
        return packet_size / self.transmission_rate

    # d/s | s = 2e8
    def propagation_delay(self):
        return self.distance / self.propagation_speed
