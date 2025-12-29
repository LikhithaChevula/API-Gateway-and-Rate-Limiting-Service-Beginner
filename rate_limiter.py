import time

class RateLimiter:
    def __init__(self, limit, window):
        self.limit = limit  # max requests
        self.window = window  # time in seconds
        self.users = {}

    def allow_request(self, user):
        current_time = time.time()

        if user not in self.users:
            self.users[user] = []

        # keep only recent requests
        self.users[user] = [
            t for t in self.users[user]
            if current_time - t < self.window
        ]

        if len(self.users[user]) < self.limit:
            self.users[user].append(current_time)
            return True

        return False
