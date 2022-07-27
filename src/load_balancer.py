import heapq
from typing import List, Set, Optional

class DCLoadBalancer:
    class Machine:
        def __init__(self, machineId: int, capacity: int):
            self.id       = machineId
            self.capacity = capacity
            self.apps     = []

        def __repr__(self):
            return '{{ .id = {}, .capacity = {} }}'.format(self.id, self.capacity)

        def __lt__(self, other):
            return self.id < other.id

        def addApplication(self, app):
            if app.loadUse < self.capacity:
                self.capacity -= app.loadUse
                self.apps.append(app)
                app.machine = self

        def removeApplication(self, app):
            self.capacity += app.loadUse
            self.apps.remove(app)
            app.machine    = None

    class Application:
        def __init__(self, appId: int, loadUse: int):
            self.id      = appId
            self.loadUse = loadUse
            self.machine = None

        def __repr__(self):
            return '\{ .id = {}, .loadUse = {} \}'.format(self.id, self.loadUse)

        def __lt__(self, other):
            return self.loadUse < other.loadUse
            

    def __init__(self):
        self.logEnabled = True
        self.machines         = {}
        self.machineCapcities = {}
        self.apps             = {}
        self.capacityPQ       = []
        

    def log(self, msg: str) -> None:
        if self.logEnabled:
            print(msg)


    def addCapacity(self, capacity: int, machine: Machine) -> None:
        if capacity in self.machineCapcities:
            heapq.heappush(self.machineCapcities[capacity], machine)
        else:
            self.machineCapcities[capacity] = [machine]
            heapq.heappush(self.capacityPQ, capacity * -1)

    def removeCapacity(self, capacity: int, machine: Machine) -> None:
        if capacity in self.machineCapcities:
            mHeap = self.machineCapcities[capacity]
            try:
                i = mHeap.index(machine)
                mHeap[i] = mHeap[-1]
                mHeap.pop()
                if len(mHeap) > 0:
                    heapq.heapify(mHeap)
                else:
                    del self.machineCapcities[capacity]
                    try:
                        i = self.capacityPQ.index(capacity * -1)
                        self.capacityPQ[i] = self.capacityPQ[-1]
                        self.capacityPQ.pop()
                        heapq.heapify(self.capacityPQ)
                    except ValueError:
                        pass
            except ValueError:
                pass

    def addMachine(self, machineId: int, capacity: int) -> None:
        if machineId in self.machines:
            return self.machines[machineId]
        m = DCLoadBalancer.Machine(machineId, capacity)
        self.machines [machineId] = m
        self.addCapacity(capacity, m)
        #self.log('self.capacityPQ = {}'.format([capacity * (-1) for capacity in self.capacityPQ]))
        #self.log('self.machineCapcities = {}'.format(self.machineCapcities))
        

    def removeMachine(self, machineId: int) -> None:
        if machineId not in self.machines:
            return
        m = self.machines [machineId]
        del self.machines [machineId]
        self.removeCapacity(m.capacity, m)

        for app in m.apps:
            #self.log('Removing app {}'.format(app.id))
            self.assignApplication(app)

        self.log('self.capacityPQ = {}'.format([capacity * (-1) for capacity in self.capacityPQ]))
        self.log('self.machineCapcities = {}'.format(self.machineCapcities))
        

    def assignApplication(self, app: Application) -> None:
        if len(self.capacityPQ) == 0:
            return -1

        maxCapacity = self.capacityPQ[0] * (-1)
        if maxCapacity < app.loadUse:
            return -1

        mHeap       = self.machineCapcities[maxCapacity]
        if len(mHeap) == 0:
            return -1

        m           = mHeap[0]
        self.removeCapacity(maxCapacity, m)
        m.addApplication(app)
        self.addCapacity(m.capacity, m)

        #self.log('after assign: self.capacityPQ = {}'.format([capacity * (-1) for capacity in self.capacityPQ]))
        #self.log('after assign: self.machineCapcities = {}'.format(self.machineCapcities))

        return m.id

    def addApplication(self, appId: int, loadUse: int) -> int:
        if appId in self.apps:
            return self.apps[appId]

        app = DCLoadBalancer.Application(appId, loadUse)
        self.apps[appId] = app
        return self.assignApplication(app)
        

    def stopApplication(self, appId: int) -> None:
        if appId not in self.apps:
            return

        app = self.apps[appId]
        del self.apps[appId]
        m   = app.machine
        if m:
            self.removeCapacity(m.capacity, m)
            m.removeApplication(app)
            self.addCapacity(m.capacity, m)


    def getApplications(self, machineId: int) -> List[int]:
        if machineId not in self.machines:
            return []
        m = self.machines[machineId]
        return [app.id for app in m.apps[:10]]
