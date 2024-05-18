
import Simulator as s


def main():
    simulator = s.Simulator()

    # ajouter des hôtes
    simulator.add_host(1)
    simulator.add_host(2)

    # ajouter des routeurs
    simulator.add_router(1, queue_size=5)
    simulator.add_router(2, queue_size=5)

    # ajouter des liens
    simulator.add_link(1, [(1, 'host', 's'), (1, 'router', 'r')], 5)
    # simulator.add_link(2, [(1, 'router', 's'), (2, 'router', 'r')], 3)
    simulator.add_link(2, [(1, 'router', 's'), (2, 'host', 'r')], 2)
    simulator.hosts[1].send_packet(2, ["Hello", "World"], False, False)

    # simulation
    simulator.run_simulation()


if __name__ == '__main__':
    main()
