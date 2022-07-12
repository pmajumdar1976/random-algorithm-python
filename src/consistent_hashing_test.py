from typing import List, Optional

from unit_test_framework import CommandExec, TestExec
import consistent_hashing as baseCode

class ConsistentHashingExec(CommandExec):
    def __init__(self):
        super(ConsistentHashingExec, self).__init__(name="ConsistentHashing", needsObj=False, returnsObj=True)

    def __call__(self, args: List) -> baseCode.ConsistentHashing:
        if len(args):
            initialNodes = args[0]
        else:
            initialNodes = 10
        return baseCode.ConsistentHashing(initialNodes)

class getNodeForKeyExec(CommandExec):
    def __init__(self):
        super(getNodeForKeyExec, self).__init__(name="getNodeForKey", needsObj=True, returnsObj=False)

    def __call__(self, args: List) -> int:
        if len(args):
            obj = args [0]
            if len(args) > 1:
                key = args[1]
            else:
                key = 1
            return obj.getNodeForKey(key)
        else:
            return -1

class addNodeExec(CommandExec):
    def __init__(self):
        super(addNodeExec, self).__init__(name="addNode", needsObj=True, returnsObj=False)

    def __call__(self, args: List) -> List[int]:
        if len(args):
            obj = args[0]
            return obj.addNode()
        else:
            return []

class removeNodeExec(CommandExec):
    def __init__(self):
        super(removeNodeExec, self).__init__(name="removeNode", needsObj=True, returnsObj=False)

    def __call__(self, args: List) -> int:
        if len(args):
            obj = args[0]
            if len(args) > 1:
                nodeID = args[1]
            else:
                nodeID = 1
            return obj.removeNode(nodeID)
        else:
            return -1

class getKeysInNodeExec(CommandExec):
    def __init__(self):
        super(getKeysInNodeExec, self).__init__(name="getKeysInNode", needsObj=True, returnsObj=False)

    def __call__(self, args: List) -> List[int]:
        if len(args):
            obj = args[0]
            if len(args) > 1:
                nodeID = args[1]
            else:
                nodeID = 1
            return obj.getKeysInNode(nodeID)
        else:
            return []

if __name__ == "__main__":
    execs = []
    execs.append(ConsistentHashingExec())
    execs.append(getNodeForKeyExec())
    execs.append(addNodeExec())
    execs.append(removeNodeExec())
    execs.append(getKeysInNodeExec())

    execMap = {}
    for e in execs:
        execMap[e.name] = e

    testCases = [
        (["ConsistentHashing",    "addNode",       "getKeysInNode", "getKeysInNode",
          "getKeysInNode",        "removeNode",    "getNodeForKey", "getNodeForKey",
          "addNode",              "getKeysInNode", "removeNode",    "getKeysInNode",
          "getKeysInNode",        "addNode",       "getKeysInNode", "getKeysInNode",
          "addNode",              "addNode",       "getNodeForKey", "getNodeForKey",
          "getNodeForKey",        "removeNode",    "addNode",       "getKeysInNode",
          "getKeysInNode",        "addNode",       "removeNode",    "getKeysInNode",
          "removeNode",           "addNode",       "addNode",       "addNode",
          "getKeysInNode",        "getNodeForKey", "addNode",       "getKeysInNode",
          "addNode",              "getNodeForKey", "getNodeForKey", "getNodeForKey",
          "getNodeForKey",        "addNode",       "getKeysInNode", "removeNode",
          "addNode",              "addNode",       "getNodeForKey", "removeNode",
          "getKeysInNode",        "addNode",       "removeNode",    "removeNode",
          "getKeysInNode",        "getKeysInNode", "getKeysInNode", "getKeysInNode",
          "addNode",              "addNode",       "getKeysInNode", "getKeysInNode",
          "removeNode",           "addNode",       "getKeysInNode", "getKeysInNode",
          "addNode",              "addNode",       "getNodeForKey", "getKeysInNode",
          "getNodeForKey",        "addNode",       "getNodeForKey", "removeNode",
          "addNode",              "getKeysInNode", "addNode",       "getNodeForKey",
          "getKeysInNode",        "addNode",       "removeNode",    "addNode",
          "addNode",              "getNodeForKey", "getNodeForKey", "getKeysInNode",
          "getKeysInNode",        "addNode",       "getKeysInNode", "addNode",
          "addNode",              "addNode",       "removeNode",    "addNode",
          "addNode",              "getKeysInNode", "addNode",       "getNodeForKey",
          "getKeysInNode",        "addNode",       "getNodeForKey"],
         [[10],                   [],              [11],            [1],
          [10],                   [5],             [214],           [418],
          [],                     [2],             [12],            [11],
          [6],                    [],              [11],            [2],
          [],                     [],              [724],           [393],
          [625],                  [11],            [],              [1],
          [16],                   [],              [13],            [6],
          [3],                    [],              [],              [],
          [1],                    [613],           [],              [19],
          [],                     [717],           [497],           [977],
          [740],                  [],              [14],            [19],
          [],                     [],              [466],           [10],
          [2],                    [],              [2],             [24],
          [8],                    [4],             [22],            [23],
          [],                     [],              [27],            [21],
          [20],                   [],              [9],             [18],
          [],                     [],              [336],           [21],
          [719],                  [],              [64],            [1],
          [],                     [28],            [],              [984],
          [30],                   [],              [18],            [],
          [],                     [948],           [699],           [36],
          [33],                   [],              [37],            [],
          [],                     [],              [4],             [],
          [],                     [8],             [],              [146],
          [32],                   [],              [403]]),
          #[null,                 [11,10],         [],              [],
          #[],                    1,               1,               1,
          #[12,11],               [],              1,               [],
          #[],                    [13,11],         [],              [],
          #[14,13],               [15,14],         1,               1,
          #1,                     1,               [16,15],         [214,418,724,393,625],
          #[],                    [17,16],         1,               [],
          #1,                     [18,17],         [19,18],         [20,19],
          #[214,418,724,393,625], 1,               [21,20],         [],
          #[22,21],               1,               1,               1,
          #1,                     [23,22],         [],              1,
          #[24,23],               [25,24],         1,               1,
          #[],                    [26,25],         1,               1,
          #[],                    [],              [],              [],
          #[27,26],               [28,27],         [],              [],
          #1,                     [29,28],         [],              [],
          #[30,29],               [31,30],         1,               [],
          #1,                     [32,31],         1,               4,
          #[33,32],               [],              [34,33],         4,
          #[],                    [35,34],         4,               [36,35],
          #[37,36],               4,               4,               [],
          #[],                    [38,37],         [],              [39,38],
          #[40,39],               [41,40],         6,               [42,41],
          #[43,42],               [],              [44,43],         6,
          #[],                    [45,44],         6]
        #(["ConsistentHashing","getNodeForKey", "getNodeForKey", "getNodeForKey",
        # "getNodeForKey",    "getNodeForKey", "getNodeForKey", "removeNode",
        # "getNodeForKey",    "getNodeForKey", "addNode",       "getNodeForKey",
        # "getNodeForKey",    "getNodeForKey", "getKeysInNode"],
        # [[6],[10],[20],[30],[40],[50],[10],[2],[40],[30],[],[10],[20],[30],[1]]),
        #(["ConsistentHashing", "getNodeForKey", "getNodeForKey", "getNodeForKey",
        #  "removeNode",        "getNodeForKey", "getNodeForKey", "addNode",
        #  "getNodeForKey",     "getNodeForKey"],
        # [[5],[8],[12],[18],[1],[12],[8],[],[8],[18]])
    ]

    t = TestExec (execs)
    t(testCases)
