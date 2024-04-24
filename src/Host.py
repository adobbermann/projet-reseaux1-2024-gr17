import time


class Host:
    def __init__(self, id):
        self.id = id

    def send_packet(self, packet, router):
        print(f"SYN: SENDING PACKET {packet} \nrouter: {router}")

        if router.enqueue(packet):
            print("Waiting for ACK...")
            #  timer de ACK reception
            timeout = 3  # seconds
            timer = time.time()
            while time.time() - timer < timeout:
                if self.receive_ack():
                    return True  # ACK reçu

            print("Timeout! Retransmitting packet...")
            return self.send_packet(packet, router)
        else:
            print("Packet dropped!")
            return False

    def receive_packet(self, packet):
        # packet received
        print(f"ACK: HOST {self.id} RECIEVED A PACKET: {packet.data}")
        return True
