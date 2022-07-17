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
            t = TestCase(self, tc[0], tc[1])
            start = timer()
            r = t()
            end = timer()
            print("Result: {} found in {} time".format(r,timedelta(seconds=end - start)))

class TestCase:
    def __init__(self, executor: TestExec, fns: List[str], args: List[List]):
        self.execs = [executor.execMap[fn] for fn in fns]
        self.args  = list(args)

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
                    r = e(nArg)
            else:
                print("=== Calling {}({}) ===>".format(e.name, arg))
                r = e(arg)
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
