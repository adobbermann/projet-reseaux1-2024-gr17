import random
import time


class Router:
    def __init__(self, router_id, queue_size, simulator):
        # par défaut
        self.router_id = router_id
        self.queue_size = queue_size
        self.queue = []
        self.simulator = simulator

        # tcp mechanism
        self.pos = 0
        self.counter = 1
        self.packet_id = 0

    def get_router_size(self):
        return len(self.queue)

    def receive_packet(self, packet_data, is_drp=False):
        self.queue.clear()
        self.counter = 1

        processing_time = random.uniform(0.01, 0.02)
        total_delay, packets, lowest_bitrate = packet_data
        drp_packets = []
        if (self.queue_size >= len(packets)):
            self.queue.extend(packets)
        if (self.queue_size < len(packets)):
            for packet in packets:
                if (len(self.queue) < self.queue_size):
                    self.queue.append(packet)
                elif (len(self.queue) >= self.queue_size):
                    drp_packets.append(packet)

        packet_size = 0
        for packet in self.queue:
            packet_size += (len(packet)*8)

        print(f'Dropped packet(s): {drp_packets}')

        link = self.simulator.links[self.counter]
        bitrate = link.transmission_rate

        transmission_delay = link.transmission_delay(self.queue, bitrate)
        propagation_delay = link.propagation_delay()
        print(f'\nLINK: {self.counter}')
        print(f'Transmission rate: {bitrate}bps')

        print(f'QUEUE: {self.queue}\n')
        for packet in self.queue:

            # ajouter l'index du paquet et le délai total au résultat
            if (self.packet_id != 0):
                total_delay -= random.uniform(0.01, 0.03)
                self.simulator.res.extend(
                    [f'{self.packet_id} ', f'{total_delay:.2f} '])
            else:
                self.simulator.res.extend(
                    [f'{self.packet_id} ', f'{total_delay:.2f} '])

            link = self.simulator.links[self.counter]

            transmission_delay = link.transmission_delay(
                self.queue, link.transmission_rate)/2
            propagation_delay = link.propagation_delay()
            print(f'transmission_delay ::: {transmission_delay}')
            print(f'propagation_delay ::: {propagation_delay}')
            print(
                f'transmission_delay + propagation_delay>>>> {transmission_delay + propagation_delay}')

            # temps d'arrivée
            total_delay += (transmission_delay +
                            propagation_delay)
            self.simulator.res.append(f'{total_delay:.2f} ')

            # temps de départ
            total_delay += processing_time
            self.simulator.res.append(f'{total_delay:.2f}  ')

            if (is_drp):
                self.simulator.res.extend(
                    [f'-  ',   "Yes ", "-.--\n"])
            else:
                total_delay += processing_time
                self.process_packet(total_delay)

            # # la position du paquet dans la file d’attente et si le paquet a été jeté
            if (self.pos < self.queue_size-1):
                self.pos += 1
            else:
                self.pos = 0
            self.packet_id += 1
            self.counter += 1

        if (len(drp_packets)):
            self.receive_packet(
                (total_delay, drp_packets, lowest_bitrate), True)

        return total_delay

    def process_packet(self, total_delay):
        self.simulator.res.extend(
            [f'{self.pos}  ',   "No ", f"{total_delay:.2f}\n"])

    def receive_packet_tcp(self, packet_data):
        processing_time = random.uniform(0.01, 0.08)
        cwnd, total_delay, packets, is_aimd = packet_data
        print(f'ROUTER: {self.router_id}| size: {self.queue_size}')

        drp_packets = []
        if (self.queue_size >= len(packets)):
            self.queue.extend(packets)
        if (self.queue_size < len(packets)):
            for packet in packets:

                if (len(self.queue) < self.queue_size):
                    self.queue.append(packet)
                elif (len(self.queue) >= self.queue_size):
                    drp_packets.append(packet)
                    if (is_aimd):
                        self.pos -= 1
                        if (self.pos == -1):
                            self.pos = 0
                        cwnd.decrease_window()

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
        self.simulator.res.append(f'{total_delay:.2f}  ')

        total_delay += processing_time

        # la position du paquet dans la file d’attente et si le paquet a été jeté
        is_processed = self.process_packet_tcp(drp_packets)
        if (self.pos+1 < self.queue_size):
            self.pos += 1

        self.queue.clear()

        return cwnd, total_delay, drp_packets, is_aimd, is_processed

    def process_packet_tcp(self, drp_packets):
        if (len(drp_packets)):
            self.simulator.res.extend(
                [f'{self.pos}  ',   "Yes ", "-.--\n", "\t\t\t\t      No "])
        else:
            self.simulator.res.extend([f'{self.pos}  ',   "No "])

        return True
