import Packet as p
import Simulator as s


def main():
    simulator = s.Simulator()
    simulator.add_host(1)
    simulator.add_host(2)

    simulator.add_router(1, queue_size=1)
    # simulator.add_router(4, queue_size=1)

    simulator.add_link(1, distance=100)
    simulator.add_link(2, distance=50)

    packet1 = p.Packet("packet1", size=100)
    # packet2 = p.Packet("packet2", size=100)

    simulator.send_packet(1, 2, packet1)
    simulator.send_packet(1, 2, packet1)
    simulator.send_packet(1, 2, packet1)
    simulator.send_packet(1, 2, packet1)
    simulator.send_packet(1, 2, packet1)
    simulator.send_packet(1, 2, packet1)
    simulator.send_packet(1, 2, packet1)
    
    # simulator.send_packet(1, 3, packet1)
    
    


if __name__ == '__main__':
    main()
