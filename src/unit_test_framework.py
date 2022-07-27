from timeit import default_timer as timer
from datetime import timedelta
from typing import List, Tuple, Optional

class CommandExec:
    def __init__(self, name: str, needsObj: bool, returnsObj: bool):
        self.name       = name
        self.needsObj   = needsObj
        self.returnsObj = returnsObj

    def __call__(self, args: List) -> Optional:
        return None

class TestExec:
    def __init__(self, cmdExecs: List[CommandExec]):
        self.execMap = {}
        for e in cmdExecs:
            self.execMap[e.name] = e

    def __call__(self, inputs:List[Tuple[List[str], List[List]]]):
        for tc in inputs:
            print('Number of executable: {}'.format(len(tc[0])))
            expected = tc[2]
            t = TestCase(self, tc[0], tc[1])
            start = timer()
            r = t()
            end = timer()
            print("Result: {}\n\t...found in {} time".format(r,timedelta(seconds=end - start)))
            for fn, stat in t.timeStats.items():
                print('{} Call latency: {}'.format(fn, stat))
            for i in range(len(r)):
                if r[i] != expected[i]:
                    print('Incorrect result @call #{} for {}({}). Expected result: {}. Actual result: {}.'.format(i, tc[0][i], tc[1][i], r[i], expected[i]))
                    break

class TimeAccumulator:
    def __init__(self):
        self.time = 0
        self.count = 0

    def __repr__(self):
        return '{}({}/{})'.format(timedelta(seconds=self.time/self.count) if self.count else 0, timedelta(seconds=self.time), self.count)

class TestCase:
    def __init__(self, executor: TestExec, fns: List[str], args: List[List]):
        self.execs     = [executor.execMap[fn] for fn in fns]
        self.args      = list(args)
        self.timeStats = {}
        for fn in executor.execMap.keys():
            self.timeStats[fn] = TimeAccumulator()

    def __call__(self) -> List:
        obj = None
        results = []
        for i, e in enumerate(self.execs):
            arg = self.args[i]
            if e.needsObj:
                if obj:
                    nArg  = [obj]
                    nArg += arg
                    print("=== Calling {}({}) ===>".format(e.name, arg))
                    start = timer()
                    r = e(nArg)
                    end = timer()
                    self.timeStats[e.name].time  += (end - start)
                    self.timeStats[e.name].count += 1
            else:
                print("=== Calling {}({}) ===>".format(e.name, arg))
                start = timer()
                r = e(arg)
                end = timer()
                self.timeStats[e.name].time  += (end - start)
                self.timeStats[e.name].count += 1
            print("<=== Returned {} ===\n".format(r))
            if r != None:
                if e.returnsObj:
                    obj = r
                    results.append('null')
                else:
                    results.append(r)
            else:
                results.append('null')

        return results
