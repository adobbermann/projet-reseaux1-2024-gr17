import Host as h
import Router as r
import Link as l
import time


class Simulator:

    # définition du réseau 
    def __init__(self):
        #Instanciation de liste vides (hôtes, routeurs, liens) => permettant de définir le réseau 
        self.hosts = {}
        self.routers = {}
        self.links = {}

    # méthode permettant d'ajouter un hôte au réseau
    def add_host(self, host_id):
        self.hosts[host_id] = h.Host(host_id)

    # méthode permettant d'ajouter un routeur au réseau
    def add_router(self, router_id, queue_size):
        self.routers[router_id] = r.Router(router_id, queue_size)
        print(
            f'router {router_id} has been added: \nrouter_id: {router_id} \nqueue_size:{queue_size}\n')

     # méthode permettant d'ajouter un lien au réseau
    def add_link(self, link_id, distance, propagation_delay=1000, transmission_delay=1000):
        self.links[link_id] = l.Link(
            distance, propagation_delay, transmission_delay)
        print(f'link {link_id} has been added: \ndistance: {
              distance} \npropagation_delay: {propagation_delay}bps \ntransmission_delay: {transmission_delay}bps\n')

    # méthode permettant l'envoie de packet d'un 
    def send_packet(self, source, destination, packet):
        print(f'destination: {destination}')
        print(f'routers: {self.routers}')
        print(f'hosts: {self.hosts}\n')

        if source not in self.hosts:
            print(f"source {source} doesn't exist:(")
            return
        if destination not in self.hosts:
            print(f"destination {destination} doesn't exist:(")
            return

        path = self.compute_path(source, destination)
        print(f'path: {path}')
        print(f'links: {self.links}\n')

        if not path:
            print(f"no path found from {source} to {destination}.")
            return

        for link_id in path:
            link = self.links[link_id]

            transmission_delay = link.transmission_delay(packet.size)
            propagation_delay = link.propagation_delay()
            time.sleep(transmission_delay + propagation_delay)

            if link_id in self.routers:
                if not self.routers[link_id].enqueue(packet):
                    print("packet is dropped!\nCause: full queue.\n")
                    break
            elif link_id in self.hosts:
                self.hosts[link_id].receive_packet(packet)

    def compute_path(self, source, destination):
        return [1, 2]
