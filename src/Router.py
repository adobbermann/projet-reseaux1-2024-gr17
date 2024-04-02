import queue


class Router:
    def __init__(self, queue_size, lifo=False):
        self.queue = queue.LifoQueue(
            queue_size) if lifo else queue.Queue(queue_size)

    def enqueue(self, packet):
        try:
            self.queue.put_nowait(packet)
            return True
        except queue.Full:
            return False

    def dequeue(self):
        return self.queue.get() if not self.queue.empty() else None
