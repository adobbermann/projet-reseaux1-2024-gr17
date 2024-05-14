import Event as e
import time


class Router:
    def __init__(self, router_id, queue_size, simulator):
        self.router_id = router_id
        self.queue_size = queue_size
        self.queue = []
        self.simulator = simulator

    def get_router_size(self):
        return len(self.queue)

    def receive_packet(self, packet_data):
        # print(f'\nrouter{self.router_id} receiving a packet(s)...')
        # print(f'packet: {packet}')

        start = time.process_time()
        transmission_delay, packet, is_tcp = packet_data

        self.queue.append(packet)

        arrival_time_ms = start + transmission_delay
        self.simulator.res.append(f"{arrival_time_ms:.2f} ")

        # print(f'len(self.queue): {len(self.queue)}')
        # print(f'len(packets): {len(packets)}')

        if len(self.queue) <= self.queue_size and len(self.queue) > 0:
            self.process_packet()
        else:
            departure_time = time.process_time()
            self.simulator.res.append(f"{departure_time:.2f} ")
            self.simulator.res.extend(['- ', "Yes "])

    def process_packet(self):
        # print(f'\nrouter processing a packet(s)...')

        departure_time = time.process_time()
        self.simulator.res.append(f"{departure_time:.2f} ")

        pos = len(self.queue)
        dropped = "Yes " if pos > self.queue_size else "No "
        self.simulator.res.extend([f'{pos-1} {dropped} '])
