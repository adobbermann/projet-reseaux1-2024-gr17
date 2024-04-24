import Host as h
from Packet import Packet
import Router as r
import Link as l
import time
import math


class Simulator:

    # définition du réseau
    def __init__(self):
        # Instanciation de liste vides (hôtes, routeurs, liens) => permettant de définir le réseau
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
<<<<<<< HEAD
        print(f'link {link_id} has been added: \ndistance: {distance}\n')
=======
        print(f"""link {link_id} has been added: \ndistance: {
              distance} \npropagation_delay: {propagation_delay}bps \ntransmission_delay: {transmission_delay}bps\n""")
>>>>>>> 546c85c2ff372ec59a21b987805f5072562c158c

    # TCP mécanisme

    def tcp_mechanism(self, packet, link, link_id, tcp_reno=True, congestion_size=3):
        # Determine the size of each mini packet
        print(f'packet.size: {packet.size}b')
        mini_packet_size = math.ceil(packet.size / link.distance)
        print(f'mini_packet_size: {mini_packet_size*8}b')

        # Split the original packet into mini packets
        packet_segments = [packet.data[i:i + mini_packet_size]
                           for i in range(0, len(packet.data), mini_packet_size)]

        print(f'packet_segments: {packet_segments}')

        # Send mini packets sequentially
        for packet_segment in packet_segments:

            mini_packet = Packet(packet_segment, len(packet_segment))
            transmission_delay = link.transmission_delay(len(packet_segment))
            propagation_delay = link.propagation_delay()
            time.sleep(transmission_delay + propagation_delay)

            if link_id in self.routers:
                print('yoo')

                if tcp_reno:
                    if congestion_size <= packet.size:
                        if not self.routers[link_id].enqueue(mini_packet):
                            print(f"MINI PACKET {
                                mini_packet.data} is dropped!\nCause: full queue.\n")
                            break
            elif link_id in self.hosts:
                self.hosts[link_id].receive_packet(mini_packet)

    # méthode permettant l'envoie de packet d'un
    def send_packet(self, source, destination, packet, tcp=True, tcp_reno=True, congestion_size=3):
        print(f'destination: {destination}')

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

            if (packet.size > link.distance):
<<<<<<< HEAD
                if (tcp is False):
                    print(f"packet size is bigger than l{
                        link_id}: (packet size: {packet.size}, link distance: {link.distance}) \nAborting...")
                    return

                if (tcp):
                    print(f"packet {packet.data} is bigger than l{
                        link_id}: (packet size: {packet.size}, link distance: {link.distance})")

                    print("LAUNCHING PIPELINING...")
                    self.tcp_mechanism(packet, link, link_id, tcp_reno)
                    return
=======
                print(f"""packet size is bigger than l{
                      link_id}: (packet size: {packet.size}, link distance: {link.distance})""")
>>>>>>> 546c85c2ff372ec59a21b987805f5072562c158c

            transmission_delay = link.transmission_delay(packet.size)
            propagation_delay = link.propagation_delay()
            time.sleep(transmission_delay + propagation_delay)
            print(f'routers: {self.routers}')
            if link_id in self.routers:

                if not self.routers[link_id].enqueue(packet):
                    print(
                        f"Packet {packet.data} dropped due to full queue at router {link_id}.")
                    break

            elif link_id in self.hosts:
                self.hosts[link_id].receive_packet(packet)

    def compute_path(self, source, destination):
        return [1, 2]
