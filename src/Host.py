import Event as e
import Router as r
import time


class Host:
    def __init__(self, host_id, simulator):
        self.host_id = host_id
        self.packet = None
        self.simulator = simulator
        self.res = []

    def send_packet(self,  destination, packets, is_tcp=True):
        event = e.Event(self.simulator.time(), self.start_transmission)
        self.simulator.schedule_event(
            event, (destination, packets, is_tcp))

    def tcp(self, destination, total_delay):
        self.end_transmission(destination, total_delay)

    def start_transmission(self, destination, packets, is_tcp):
        self.simulator.columns.extend([f"\nk", f"dép{self.host_id}"])

        nodes = []
        for link_id, obj in self.simulator.links.items():
            link = self.simulator.links[link_id]
            nodes.extend(link.get_nodes())
        self.create_columns(nodes)

        for pid, packet in enumerate(packets):
            # calculer le délai de transmission et de propagation
            transmission_delay = link.transmission_delay([packet])
            propagation_delay = link.propagation_delay()
            total_delay = transmission_delay + propagation_delay

            # ajouter l'index du paquet et le délai total au résultat
            self.simulator.res.extend([f'{pid} ', f'{total_delay:.2f} '])

            # envoyer le paquet à chaque nœud du chemin
            for node_id, node_type, side in nodes:
                if node_type == 'router' and side == 'r':
                    router = self.simulator.routers[node_id]
                    router.receive_packet(
                        (total_delay, packet, is_tcp))
                else:
                    # calculer l'heure d'arrivée et de départ des hôtes
                    last_node = nodes[-1]
                    last_node_id = last_node[0]
                    start_time = time.process_time()
                    arrival_time = start_time + transmission_delay

                    # s'il s'agit du dernier nœud, ajouter l'heure d'arrivée et interrompre l'opération
                    if last_node_id == node_id:
                        self.simulator.res.append(f'{arrival_time:.2f}\n')
                        break

                    # s'il s'agit d'un routeur, calculer l'heure de départ et ajouter l'heure d'arrivée
                    if side == 'r':
                        departure_time = time.process_time()
                        self.simulator.res.extend(
                            [f"{arrival_time:.2f}", f"{departure_time:.2f}"])

    def create_columns(self, nodes):
        for node_id, node_type, side in nodes:
            if node_type == 'router' and side == 'r':
                self.simulator.columns.extend(
                    [f"arR{node_id}", f"dépR{node_id}", "pos", "drp"])
            else:
                last_node = nodes[-1]
                last_node_id = last_node[0]
                if (last_node_id == node_id):
                    self.simulator.columns.append(f'ar{last_node_id}')
                    return
                if side == 'r':
                    self.simulator.columns.extend(
                        [f"ar{node_id}", f"dép{node_id}"])

    def end_transmission(self, destination, total_delay):

        destination_host = self.simulator.hosts[destination]
        destination_host.receive_packet(total_delay)

    def receive_packet(self, host_id, total_delay='-'):
        self.simulator.columns.append(f"ar{host_id}")

        if (self.simulator.res[-1] == "Yes"):
            self.simulator.res.append("-.-- \n")
        else:
            self.simulator.res.append(f"{total_delay:.2f}")
        print(''.join(self.res))
