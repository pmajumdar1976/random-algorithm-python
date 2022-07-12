import random
from typing import List, Set, Optional

class ConsistentHashing:
    MAX_NODE_REPEAT = 1
    MAX_NODE        = 1000
    MAX_SLOT        = MAX_NODE_REPEAT * MAX_NODE

    class Node:
        def __init__(self, nodeId: int, __hash):
            self.id    = nodeId
            self.hash  = __hash
            self.keys  = {}
            self.slots = []

        def hashes(self, seeds: List[int]) -> List[int]:
            r = []
            for s in seeds:
                r.append(ConsistentHashing.intHash(self.id, s))
            return r
        
        def addKeys(self, keys: Set[int], preferredSlot: int) -> Optional:
            self.hash.log('addKeys({}) to Node {} @slot {}'.format(keys, self.id, preferredSlot))
            for k in keys:
                self.hash.keys[k] = self
            if preferredSlot in self.keys:
                self.keys[preferredSlot] = self.keys[preferredSlot].union(keys)
            else:
                self.keys[preferredSlot] = keys

    @staticmethod
    def __xorShift__(key: int, numBits: int):
        return key ^ (key >> numBits)

    @staticmethod
    def intHash (key: int, seed: int):
        p = 0x5555555555555555
        h = seed * ConsistentHashing.__xorShift__(p * ConsistentHashing.__xorShift__(key, 32), 32)
        return int(h) % ConsistentHashing.MAX_SLOT

    @staticmethod
    def SlotInRange(start: int, end: int, slot: int) -> bool: # Excludes end
        if end - start:
            return ((start <= slot) and (slot < end))
        else:
            reutn ((end > slot) or (slot >= start))

    def __init__(self, initialNodes: int):
        self.logEnabled  = True
        self.log('ConsistentHashing: initialNodes = {}'.format(initialNodes))
        self.nextNodeID  = 1
        self.randomSeeds = [0] * (ConsistentHashing.MAX_NODE_REPEAT + 1)
        self.slots       = [None] * ConsistentHashing.MAX_SLOT
        self.nodeMap     = {}
        self.keys        = {}

        for i in range(ConsistentHashing.MAX_NODE_REPEAT + 1):
            self.randomSeeds[i] = random.randrange(2^32)

        while initialNodes:
            self.addNode()
            initialNodes -= 1

    def log(self, msg: str) -> Optional:
        if self.logEnabled:
            print(msg)

    def keyHash(self, key: int):
        return ConsistentHashing.intHash(key, self.randomSeeds[0])

    def newNode (self) -> Node:
        n = ConsistentHashing.Node(self.nextNodeID, self)
        self.nextNodeID += 1
        self.nodeMap[n.id] = n
        return n

    def findNextEmptySlot(self, slot):
        nextSlot = (slot + 1) % ConsistentHashing.MAX_SLOT
        while nextSlot != slot:
            if self.slots[nextSlot] == None:
                return nextSlot
            nextSlot = (nextSlot + 1) % ConsistentHashing.MAX_SLOT
        return nextSlot

    def findPrevNonEmptySlot(self, slot):
        prevSlot = slot - 1
        while prevSlot > (slot - self.MAX_SLOT):
            if self.slots[prevSlot]:
                return prevSlot + self.MAX_SLOT if prevSlot < 0 else prevSlot
            prevSlot -= 1
        return slot

    def assignNodeToSlot(self, node: Node, slot: int) -> Node:
        self.log("Assigning Node {} on slot {}".format(node.id, slot))
        self.slots[slot] = node
        node.slots.append(slot)
        prevSlot = self.findPrevNonEmptySlot(slot)
        prevNode = self.slots[prevSlot]

        for s in list(prevNode.keys.keys()):
            if not ConsistentHashing.SlotInRange(prevSlot, slot, s):
                k = prevNode.keys[s]
                self.log('Moving keys {} in slot {} from node {} to node {}'.format(k, s, prevNode.id, node.id))
                node.addKeys (k, s)
                #del prevNode.keys[s]  --> should we open it for getting rid of unnecessary copies

        return prevNode

    def assignNode(self, node) -> List[Node]:
        prevNodes = []
        hashes = node.hashes(self.randomSeeds[1:])
        for h in hashes:
            if self.slots[h] == None:
                prevNodes.append(self.assignNodeToSlot(node, h))
                continue
            nextSlot = self.findNextEmptySlot(h)
            if nextSlot != h:
                prevNodes.append(self.assignNodeToSlot(node, nextSlot))
        return prevNodes

    def getNodeForKey(self, key: int) -> int:
        self.log('getNodeForKey: key = {}'.format(key))
        if key in self.keys:
            node = self.keys[key]
            self.log('Returning node.id {}'.format(node.id))
            return node.id

        slot = self.keyHash(key)
        self.log("key = {}, preferredSlot = {}".format(key, slot))
        node = self.slots[slot]
        if node:
            node.addKeys({key}, slot)
            self.log('Returning node.id {}'.format(node.id))
            return node.id

        prevSlot = self.findPrevNonEmptySlot(slot)
        if slot != prevSlot:
            node = self.slots[prevSlot]
            node.addKeys({key}, slot)
            self.log('Returning node.id {}'.format(node.id))
            return node.id

        self.log('Returning node.id {}'.format(-1))
        return -1
        

    def removeNode(self, nodeID: int) -> int:
        self.log('removeNode: nodeID = {}'.format(nodeID))
        otherNodes = set({})
        if nodeID in self.nodeMap:
            node = self.nodeMap[nodeID]
            del self.nodeMap[nodeID]
            for s in node.slots:
                self.log('Cleaning slot {}'.format(s))
                self.slots[s] = None
            for s, k in node.keys.items():
                self.log('Assigning keys {} for slot {} to some other node'.format(k, s))
                otherNode = self.slots[s]
                if otherNode:
                    otherNode.addKeys(k, s)
                    otherNodes.add(otherNode.id)
                else:
                    self.log('Looking for previous slot')
                    prevSlot = self.findPrevNonEmptySlot(s)
                    self.log('previous slot is found at {}'.format(prevSlot))
                    if prevSlot != s:
                        otherNode = self.slots[prevSlot]
                        otherNode.addKeys(k, s)
                        otherNodes.add(otherNode.id)
            if len(otherNodes) == 0:
                for s in node.slots:
                    prevSlot = self.findPrevNonEmptySlot(s)
                    if prevSlot != s:
                        otherNodes.add(self.slots[prevSlot].id)
                        break

        r = list(otherNodes)[0] if len(otherNodes) > 0 else -1
        self.log('removeNode({}) returning {}'.format(nodeID, r))
        return r

    def addNode(self) -> List[int]:
        self.log('addNode')
        n = self.newNode()
        prevNodes = self.assignNode(n)
        r = [n.id, prevNodes[0].id] if len(prevNodes) > 0 else [n.id, n.id]
        self.log('addNode returning {}'.format(r))
        return r

    def getKeysInNode(self, nodeID: int) -> List[int]:
        self.log('getKeysInNode: nodeID = {}'.format(nodeID))
        if nodeID not in self.nodeMap:
            self.log('Unknown nodeID = {}'.format(nodeID))
            return []
        
        node = self.nodeMap[nodeID]
        result = set({})
        for k in node.keys.values():
            result = result.union(k)
        self.log('getKeysInNode({}) returning keys: {}'.format(nodeID, result))
        return list(result)
