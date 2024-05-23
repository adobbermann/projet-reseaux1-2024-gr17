import Event as e
import Router as r
import TCP as t
import time


class Host:
    def __init__(self, host_id, simulator):
        self.host_id = host_id
        self.packet = None
        self.simulator = simulator
        self.total_delay = 0

    def send_packet(self,  destination, packets, is_tcp=True, is_aimd=True):
        event = e.Event(self.simulator.time(), self.start_transmission)
        self.simulator.schedule_event(
            event, (destination, packets, is_tcp, is_aimd))

    def tcp(self, packets, is_aimd):
        tcp = t.TCP(self.host_id, self.simulator)
        tcp.start_transmission(is_aimd, self.total_delay, packets)

    def start_transmission(self, destination, packets, is_tcp=True, is_aimd=True):

        self.create_columns(is_tcp)
        # tcp mechanism
        if (is_tcp):
            self.tcp(packets, is_aimd)
            return

        print("\nStarting transmission...")
        print(f'Packet(s): {packets}\n')

        l1 = self.simulator.links[1]
        bitrate = l1.transmission_rate
        nodes = []
        for link_id, obj in self.simulator.links.items():
            link = self.simulator.links[link_id]
            bitrate = min(bitrate, link.transmission_rate)
            nodes.extend(link.get_nodes())

        total_delay = 0
        for pid, packet in enumerate(packets):
            transmission_delay = link.transmission_delay([packet], bitrate)
            propagation_delay = link.propagation_delay()

            # ajouter l'index du paquet et le délai total au résultat
            self.simulator.res.extend([f'{pid} ', f'{total_delay:.2f} '])

            # envoyer le paquet à chaque nœud du chemin
            for node_id, node_type, side in nodes:

                if node_type == 'router' and side == 'r':
                    router = self.simulator.routers[node_id]
                    total_delay = router.receive_packet((total_delay, packet))

                    if (self.simulator.res[-1].strip() == "Yes"):
                        self.end_transmission(destination, total_delay)
                        break
                else:
                    if (node_type == 'host' and side == 'r'):
                        # calculer l'heure d'arrivée et de départ des hôtes
                        last_node = nodes[-1]
                        last_node_id = last_node[0]

                        # s'il s'agit du dernier nœud, ajouter l'heure d'arrivée et interrompre l'opération
                        if last_node_id == node_id:
                            self.end_transmission(destination, total_delay)
                            break

            total_delay = transmission_delay + propagation_delay + 0.02

    def end_transmission(self, destination, total_delay):

        destination_host = self.simulator.hosts[destination]
        destination_host.receive_packet(total_delay)

    def receive_packet(self, total_delay=0):

        if (self.simulator.res[-1].strip() == "Yes"):
            self.simulator.res.append("-.-- \n")
        else:
            self.simulator.res.append(f"{total_delay+0.20:.2f}\n")

    def create_columns(self, is_tcp):

        nodes = []
        for link_id, obj in self.simulator.links.items():
            link = self.simulator.links[link_id]
            nodes.extend(link.get_nodes())

        idx = 0
        is_dep = []
        for (node_id, node_type, side) in nodes:

            if (idx == 0):
                self.simulator.columns.extend([f"\nk", f"dép{node_id}"])
            else:
                if (node_type == 'router'):
                    if (side == "r"):
                        self.simulator.columns.append(f"arR{node_id}")
                    elif (side == "s" and (node_id not in is_dep)):
                        self.simulator.columns.extend(
                            [f"dépR{node_id}", "pos", "drp"])
                        is_dep.append(node_id)

                if (node_type == 'host'):
                    if (side == "s"):
                        self.simulator.columns.append(f"dép{node_id}")
                    elif (side == "r"):
                        if (is_tcp):
                            self.simulator.columns.append(f'ack ar{node_id}')
                        else:
                            self.simulator.columns.append(f"ar{node_id}")

            idx += 1
