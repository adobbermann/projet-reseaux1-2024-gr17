
import Simulator as s


def main():
    simulator = s.Simulator()

    # ajouter des hôtes
    simulator.add_host(1)
    simulator.add_host(2)

    # ajouter des routeurs
    simulator.add_router(1, queue_size=5)

    # ajouter des liens | connected_nodes, distance, propagation_speed, transmission_rate
    simulator.add_link(1, [(1, 'host', 's'), (1, 'router', 'r')], 5, 2e8, 100)
    simulator.add_link(2, [(1, 'router', 's'), (2, 'host', 'r')], 3, 2e8, 50)

    # destination, packets, is_tcp, is_aimd, interval_enabled
    simulator.hosts[1].send_packet(
        2, ["Hello", "world"], False, False, False)

    # simulation
    simulator.run_simulation()


if __name__ == '__main__':
    main()
