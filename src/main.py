import Packet as p
import Simulator as s


def main():
    simulator = s.Simulator()
    simulator.add_host(1)
    simulator.add_host(2)

    simulator.add_router(1, queue_size=10)

    simulator.add_link(1, distance=100)
    simulator.add_link(2, distance=50)

    packet1 = p.Packet("packet1", size=(len("packet1")*8))

# send_packet(source, destination, packet, tcp, tcp_reno,congestion_size=3):
    simulator.send_packet(1, 2, packet1, True, False)
    simulator.send_packet(1, 2, packet1, True, False)
    simulator.send_packet(1, 2, packet1, True, False)
    
    # simulator.send_packet(1, 2, packet1, is_tcp=True)
    # simulator.send_packet(1, 2, packet1, is_tcp=True)
    # simulator.send_packet(1, 2, packet1, is_tcp=True)


if __name__ == '__main__':
    main()
