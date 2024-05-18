class AIMD_CongestionControl:
    def __init__(self, initial_window_size=1, max_window_size=10, min_window_size=1):
        self.window_size = initial_window_size
        self.max_window_size = max_window_size
        self.min_window_size = min_window_size

    def increase_window(self):
        self.window_size = int(self.window_size + 1)

    def decrease_window(self):
        self.window_size = int(self.window_size / 2)
