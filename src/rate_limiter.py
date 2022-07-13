from typing import List, Optional

class RateLimiter:

    def __init__(self, n: int, t: int):
        self.logEnabled = True
        self.maxAllowed = n
        self.period     = t
        self.allowed    = []


    def log (self, msg: str) -> Optional:
        if self.logEnabled:
            print(msg)

    def shouldAllow(self, timestamp: int) -> bool:
        self.log('1. allowed = {}'.format(self.allowed))
        while self.allowed:
            if self.allowed[0] + self.period <= timestamp:
                self.log('Popping since self.allowed[0] + self.period = {}'.format(self.allowed[0] + self.period))
                self.allowed.pop(0)
            else:
                break
        self.log('2. allowed = {}'.format(self.allowed))
        if len(self.allowed) < self.maxAllowed:
            self.allowed.append(timestamp)
            self.log('3. allowed = {}'.format(self.allowed))
            return True
        else:
            return False
