class Host:
    def __init__(self, id):
        self.id = id

    def send_packet(self, packet, router):
        print(f"SYN: SENDING PACKET {packet} \nrouter: {router}")
        return router.enqueue(packet)

    def receive_packet(self, packet):
        print(f"ACK: HOST {self.id} RECIEVED A PACKET: {packet.data}")
