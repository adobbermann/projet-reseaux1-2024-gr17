import Host as h
import Router as r
import Link as l


import heapq


class Simulator:
    def __init__(self):
        self.hosts = {}
        self.routers = {}
        self.links = {}
        self.event_queue = []
        self.current_time = 0

        self.columns = []
        self.res = []

    def time(self):
        return self.current_time

    def schedule_event(self, event, args=()):
        heapq.heappush(self.event_queue, (event.t, event.func, args))

    def run_simulation(self):
        while self.event_queue:

            time, func, args = heapq.heappop(self.event_queue)
            print(f'func>>>{func}')

            self.current_time = time
            func(*args)

        print(' '.join(self.columns))
        print(''.join(self.res))

    def add_host(self, host_id):
        self.hosts[host_id] = h.Host(host_id, self)

    def add_router(self, router_id, queue_size):
        self.routers[router_id] = r.Router(router_id, queue_size, self)

    def add_link(self, link_id, connected_nodes, propagation_speed=2e8, transmission_rate=1000):
        self.links[link_id] = l.Link(
            connected_nodes, propagation_speed, transmission_rate)
