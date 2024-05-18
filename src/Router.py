import Event as e
import random


class Router:
    def __init__(self, router_id, queue_size, simulator):
        # par défaut
        self.router_id = router_id
        self.queue_size = queue_size
        self.queue = []
        self.simulator = simulator

        # tcp mechanism
        self.pos = 0

    def get_router_size(self):
        return len(self.queue)

    def receive_packet(self, packet_data):

        processing_time = 0.05
        total_delay, packet = packet_data
        self.queue.append(packet)

        total_delay += processing_time

        l1 = self.simulator.links[1]
        bitrate = l1.transmission_rate
        for link_id, obj in self.simulator.links.items():
            link = self.simulator.links[link_id]
            bitrate = min(bitrate, link.transmission_rate)

        transmission_delay = link.transmission_delay(self.queue, bitrate)
        propagation_delay = link.propagation_delay()

        # temps d'arrivée
        total_delay += transmission_delay + \
            propagation_delay + (0.02 * len(self.queue))
        self.simulator.res.append(f'{total_delay:.2f} ')

        # temps de départ
        total_delay += random.uniform(0.10, 0.15)
        self.simulator.res.append(f'{total_delay:.2f}   ')

        total_delay += processing_time

        if len(self.queue) <= self.queue_size and len(self.queue) > 0:
            self.process_packet()
        else:
            print(f"Router{self.router_id} is full! dropping packet...")
            print(f"Dropped packet: {packet}\n")

            self.simulator.res.extend(['-   ', "Yes "])
        return total_delay

    def process_packet(self):

        pos = len(self.queue)
        self.simulator.res.extend([f'{pos}   No '])

    def receive_packet_tcp(self, packet_data):
        processing_time = random.uniform(0.04, 0.08)
        cwnd, total_delay, packets, is_aimd = packet_data
        print(f'ROUTER: {self.router_id}')

        drp_packets = []
        if (self.queue_size < len(packets)):
            i = 0
            for packet in packets:
                if (len(self.queue) < self.queue_size):
                    print(f'QUEUE | QUEUE_SIZE:{i} {
                          len(self.queue)}  {self.queue_size}')

                    self.queue.append(packet)
                else:
                    drp_packets.append(packet)
                    if (is_aimd):
                        cwnd.decrease_window()

        else:
            self.queue.extend(packets)

        print(f'Dropped packet(s): {drp_packets}')
        print(f'Congestion window size: {
              cwnd.window_size} at time: {total_delay:.2f} seconds')

        print(f'QUEUE: {self.queue}\n')

        l1 = self.simulator.links[1]
        bitrate = l1.transmission_rate
        for link_id, obj in self.simulator.links.items():
            link = self.simulator.links[link_id]
            bitrate = min(bitrate, link.transmission_rate)

        transmission_delay = link.transmission_delay(self.queue, bitrate)
        propagation_delay = link.propagation_delay()

        # temps d'arrivée
        total_delay += transmission_delay + \
            propagation_delay + (0.02 * len(self.queue))
        self.simulator.res.append(f'{total_delay:.2f} ')

        # temps de départ
        total_delay += random.uniform(0.10, 0.15)
        self.simulator.res.append(f'{total_delay:.2f}   ')

        total_delay += processing_time

        # la position du paquet dans la file d’attente et si le paquet a été jeté
        self.process_packet_tcp()

        self.queue.clear()

        # Retransmissions
        if (len(drp_packets)):
            print(f"Retransmissiting packet(s): {drp_packets}")
            self.simulator.res.append(f"\n \t\t\t  ")
            self.receive_packet_tcp((cwnd, total_delay, drp_packets, is_aimd))

        return total_delay

    def process_packet_tcp(self):

        self.simulator.res.extend([f'{self.pos}   No '])
        self.pos += 1
