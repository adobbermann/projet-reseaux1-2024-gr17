import AIMD as a
import TCP as t


class TCP:
    def __init__(self, host_id, simulator, packets=[]):
        self.host_id = host_id
        self.simulator = simulator
        self.cwnd = a.AIMD_CongestionControl()
        self.packet_id = 0
        self.drp_packets = []

    def start_retransmission(self, is_aimd, total_delay, nodes, drp_packets=[]):
        print("Starting REtransmission TCP+AIMD...")
        print(f'Remaining packet(s): {drp_packets}')

        packets_flow = []

        if (self.cwnd.window_size <= len(drp_packets)):
            for idx in range(self.cwnd.window_size):
                packets_flow.append(drp_packets[0])
                drp_packets.pop(0)
        else:
            packets_flow.extend(drp_packets)
            drp_packets.clear()

        print(f"Congestion window size: {self.cwnd.window_size}")
        print(f"Sending packet(s): {packets_flow}\n")

        if (len(packets_flow) > 1):
            print(f"Launching pipelining...\n")

        # envoyer le paquet à chaque nœud du chemin
        for node_id, node_type, side in nodes:

            if node_type == 'router' and side == 'r':
                print(f'PACKETS FLOW: {packets_flow}')
                router = self.simulator.routers[node_id]

                cwnd, td, drp_packets, is_aimd, is_processed = router.receive_packet_tcp(
                    (self.cwnd, total_delay, packets_flow, is_aimd))
                total_delay = td
            else:

                # pid du packet
                if (node_type == 'host' and side == 's'):
                    self.simulator.res.extend(
                        [f'  ', f'{total_delay:.2f} '])

                if (node_type == 'host' and side == 'r'):

                    # imprimer les acks
                    self.simulator.res.append(
                        f'Yes {total_delay + 0.35:.2f} ')

                    # temps d'arrivée
                    last_node = nodes[-1]
                    last_node_id = last_node[0]

                    if (last_node_id == node_id):
                        if (is_aimd):
                            self.cwnd.increase_window()
                        self.simulator.res.append('\n')

        if (len(drp_packets) > 0):
            self.start_transmission(is_aimd, total_delay, drp_packets)

        return total_delay

    def start_transmission(self, is_aimd, total_delay, packets):
        print("----------------------------------------------------------------")

        print("Starting transmission TCP+AIMD...")
        print(f'Remaining packet(s): {packets}')

        packets_flow = []

        nodes = []
        for link_id, obj in self.simulator.links.items():
            link = self.simulator.links[link_id]
            nodes.extend(link.get_nodes())

        if (self.cwnd.window_size <= len(packets)):
            for idx in range(self.cwnd.window_size):
                packets_flow.append(packets[0])
                packets.pop(0)
        else:
            packets_flow.extend(packets)
            packets.clear()

        print(f"Congestion window size: {self.cwnd.window_size}")
        print(f"Sending packet(s): {packets_flow}\n")

        if (len(packets_flow) > 1):
            print(f"Launching pipelining...\n")
        drp = []
        node = ()
        # envoyer le paquet à chaque nœud du chemin
        for id, type, s in nodes:
            if type == 'router' and s == 'r':
                print(f'PACKETS FLOW: {packets_flow}')
                router = self.simulator.routers[id]

                cwnd, total_delay, drp_packets, is_aimd, is_processed = router.receive_packet_tcp(
                    (self.cwnd, total_delay, packets_flow, is_aimd))
                drp = drp_packets
                if (len(drp)):
                    node = (id, type, s)

            else:

                if (len(self.simulator.res) > 0 and self.simulator.res[-1].strip() == 'Yes'):
                    self.simulator.res.extend(["No ", "-.-- \n"])
                    break

                # pid du packet
                if (type == 'host' and s == 's'):
                    self.simulator.res.extend(
                        [f'{self.packet_id} ', f'{total_delay:.2f} '])
                    self.packet_id += 1

                if (type == 'host' and s == 'r'):

                    # imprimer les acks
                    self.simulator.res.append(
                        f'Yes {total_delay+0.2:.2f} ')

                    # temps d'arrivée
                    last_node = nodes[-1]
                    last_node_id = last_node[0]

                    if (last_node_id == id):
                        if (is_aimd):
                            self.cwnd.increase_window()
                        self.simulator.res.append('\n')

        if (len(drp)):
            total_delay = self.start_retransmission(
                is_aimd, total_delay, nodes, drp)

        if (len(packets) > 0):
            self.start_transmission(is_aimd, total_delay, packets)
