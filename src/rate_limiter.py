from typing import List, Optional

class RateLimiter:

    def __init__(self, n: int, t: int):
        self.maxAllowed = n
        self.period     = t
        self.allowed    = []
        

    def shouldAllow(self, timestamp: int) -> bool:
        while self.allowed:
            if self.allowed[0] + self.period <= timestamp:
                self.allowed.pop(0)
            else:
                break
        if len(self.allowed) < self.maxAllowed:
            self.allowed.append(timestamp)
            return True
        else:
            return False
