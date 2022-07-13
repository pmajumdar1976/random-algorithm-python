from typing import List, Optional

from unit_test_framework import CommandExec, TestExec
import rate_limiter as baseCode

class RateLimiterExec(CommandExec):
    DEFAULT_MAX_ALLOWED = 1
    DEFAULT_PERIOD      = 5
    def __init__(self):
        super(RateLimiterExec, self).__init__(name="RateLimiter", needsObj=False, returnsObj=True)

    def __call__(self, args: List) -> baseCode.RateLimiter:
        if len(args) >= 1:
            maxAllowed = args[0]
            if len(args) >= 2:
                period = args[1]
            else:
                period = RateLimiterExec.DEFAULT_PERIOD
        else:
            maxAllowed = RateLimiterExec.DEFAULT_MAX_ALLOWED
            period     = RateLimiterExec.DEFAULT_PERIOD

        return baseCode.RateLimiter(maxAllowed, period)

class shouldAllowExec(CommandExec):
    def __init__(self):
        super(shouldAllowExec, self).__init__(name="shouldAllow", needsObj=True, returnsObj=False)

    def __call__(self, args: List) -> bool:
        if len(args):
            obj = args [0]
            if len(args) > 1:
                timeStamp = args[1]
                return obj.shouldAllow(timeStamp)
            else:
                return False
        else:
            return False

if __name__ == "__main__":
    execs = []
    execs.append(RateLimiterExec())
    execs.append(shouldAllowExec())

    testCases = [
        (["RateLimiter", "shouldAllow", "shouldAllow", "shouldAllow", "shouldAllow",
          "shouldAllow", "shouldAllow", "shouldAllow", "shouldAllow", "shouldAllow",
          "shouldAllow", "shouldAllow", "shouldAllow", "shouldAllow", "shouldAllow",
          "shouldAllow", "shouldAllow", "shouldAllow", "shouldAllow", "shouldAllow"],
         [[16,12],       [38],          [42],          [48],          [50],
          [50],          [50],          [50],          [50],          [50],
          [50],          [50],          [50],          [50],          [50],
          [50],          [50],          [50],          [50],          [50]]),
    ]

    t = TestExec (execs)
    t(testCases)
