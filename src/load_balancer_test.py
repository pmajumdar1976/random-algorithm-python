from typing import List, Optional

from unit_test_framework import CommandExec, TestExec
import load_balancer as baseCode

class DCLoadBalancerExec(CommandExec):
    def __init__(self):
        super(DCLoadBalancerExec, self).__init__(name="DCLoadBalancer", needsObj=False, returnsObj=True)

    def __call__(self, args: List) -> baseCode.DCLoadBalancer:
        return baseCode.DCLoadBalancer();

class addMachineExec(CommandExec):
    def __init__(self):
        super(addMachineExec, self).__init__(name="addMachine", needsObj=True, returnsObj=False)

    def __call__(self, args: List) -> None:
        if len(args) >= 3:
            obj       = args[0]
            machineId = args[1]
            capacity  = args[2]
            obj.addMachine(machineId, capacity)

class removeMachineExec(CommandExec):
    def __init__(self):
        super(removeMachineExec, self).__init__(name="removeMachine", needsObj=True, returnsObj=False)

    def __call__(self, args: List) -> None:
        if len(args) >= 2:
            obj       = args[0]
            machineId = args[1]
            obj.removeMachine(machineId)

class addApplicationExec(CommandExec):
    def __init__(self):
        super(addApplicationExec, self).__init__(name="addApplication", needsObj=True, returnsObj=False)

    def __call__(self, args: List) -> int:
        if len(args) >= 3:
            obj     = args[0]
            appId   = args[1]
            loadUse = args[2]
            return obj.addApplication(appId, loadUse)
        else:
            return (-1)

class stopApplicationExec(CommandExec):
    def __init__(self):
        super(stopApplicationExec, self).__init__(name="stopApplication", needsObj=True, returnsObj=False)

    def __call__(self, args: List) -> None:
        if len(args) >= 2:
            obj   = args[0]
            appId = args[1]
            obj.stopApplication(appId)

class getApplicationsExec(CommandExec):
    def __init__(self):
        super(getApplicationsExec, self).__init__(name="getApplications", needsObj=True, returnsObj=False)

    def __call__(self, args: List) -> List[int]:
        if len(args) >= 2:
            obj       = args[0]
            machineId = args[1]
            return obj.getApplications(machineId)
        else:
            return []

if __name__ == "__main__":
    execs = []
    execs.append(DCLoadBalancerExec())
    execs.append(addMachineExec())
    execs.append(removeMachineExec())
    execs.append(addApplicationExec())
    execs.append(stopApplicationExec())
    execs.append(getApplicationsExec())

    testCases = [
        (["DCLoadBalancer", "addMachine",     "addMachine",      "addMachine",     "addMachine",
          "addApplication", "addApplication", "addApplication",  "addApplication", "getApplications",
          "addMachine",     "addApplication", "stopApplication", "addApplication", "getApplications",
          "removeMachine",  "getApplications"],
         [[],               [1,1],            [2,10],            [3,10],           [4,15],
          [1,3],            [2,11],           [3,6],             [4,5],            [2],
          [5,10],           [5,5],            [3],               [6,5],            [4],
          [4],              [2]]),
    ]

    t = TestExec (execs)
    t(testCases)
