
import Simulator as s


def main():
    simulator = s.Simulator()

    # ajouter des hôtes
    simulator.add_host(1)
    simulator.add_host(2)
    simulator.add_host(3)

    # ajouter des routeurs
    simulator.add_router(1, queue_size=5)
    simulator.add_router(2, queue_size=2)

    # ajouter des liens
    simulator.add_link(1, [(1, 'host', 's'), (1, 'router', 'r')])
    simulator.add_link(2, [(1, 'router', 's'), (2, 'router', 'r')])
    simulator.add_link(3, [(2, 'router', 's'), (2, 'host', 'r')])
    simulator.hosts[1].send_packet(
        2, ["Hi", "I", "am", "Arno"], is_tcp=True)

    # programmer des événements
    # TODO
    # simulator.hosts[1].send_packet(
    #     2, ["Arno M0uke"], is_tcp=True)

    # simulator.add_link(4, [(1, 'host', 's'), (1, 'router', 'r')])
    # simulator.add_link(5, [(1, 'router', 's'), (2, 'host', 'r')])

    # simulation
    simulator.run_simulation()


if __name__ == '__main__':
    main()
