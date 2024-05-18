import AIMD as a
import time


class TCP:
    def __init__(self, host_id, simulator, packets=[]):
        self.host_id = host_id
        self.simulator = simulator
        self.cwnd = a.AIMD_CongestionControl()
        self.packets = packets
        self.packet_id = 0

    def start_transmission(self, is_aimd, total_delay):
        print("----------------------------------------------------------------")

        print("Starting transmission TCP+AIMD...")
        print(f'Remaining packet(s): {self.packets}')

        packets_flow = []

        nodes = []
        for link_id, obj in self.simulator.links.items():
            link = self.simulator.links[link_id]
            nodes.extend(link.get_nodes())

        if (len(self.packets) == 1):
            packets_flow.append(self.packets[0])

        if (self.cwnd.window_size <= len(self.packets)):
            for idx in range(self.cwnd.window_size):
                packets_flow.append(self.packets[0])
                self.packets.pop(0)
        else:
            packets_flow.extend(self.packets)
            self.packets.clear()

        print(f"Congestion window size: {self.cwnd.window_size}")
        print(f"Sending packet(s): {packets_flow}\n")

        if (len(packets_flow) > 1):
            print(f"Launching pipelining...\n")

        # envoyer le paquet à chaque nœud du chemin
        for node_id, node_type, side in nodes:
            if node_type == 'router' and side == 'r':
                print(f'PACKETS FLOW: {packets_flow}')

                router = self.simulator.routers[node_id]
                total_delay = router.receive_packet_tcp(
                    (self.cwnd, total_delay, packets_flow, is_aimd))

                if (self.simulator.res[-1].strip() == 'Yes'):
                    self.simulator.res.extend(["No ", "-.-- \n"])
                    break

            else:
                # pid du packet
                if (node_type == 'host' and side == 's'):
                    self.simulator.res.extend(
                        [f'{self.packet_id} ', f'{total_delay:.2f} '])
                    self.packet_id += 1

                if (node_type == 'host' and side == 'r'):
                    # calculer l'heure d'arrivée et de départ des hôtes
                    last_node = nodes[-1]
                    last_node_id = last_node[0]

                    if last_node_id == node_id:
                        # imprimer les acks
                        if (self.simulator.res[-1].strip() == 'Yes'):
                            self.simulator.res.extend(["No ", "-.-- \n"])
                            break
                        else:
                            self.simulator.res.append("Yes ")
                            if (is_aimd):
                                self.cwnd.increase_window()
                            # temps d'arrivée
                            self.simulator.res.append(
                                f'{total_delay+0.2:.2f}\n')

                        break

        if (len(self.packets) > 0):
            self.start_transmission(is_aimd, total_delay)
