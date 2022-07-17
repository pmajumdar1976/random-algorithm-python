'''
There is an m x n grid with a ball. The ball is initially at the position [startRow, startColumn]. You are allowed to move the ball to one of the four adjacent cells in the grid (possibly out of the grid crossing the grid boundary). You can apply at most maxMove moves to the ball.

Given the five integers m, n, maxMove, startRow, startColumn, return the number of paths to move the ball out of the grid boundary. Since the answer can be very large, return it modulo 10^9 + 7.
'''

from typing import List, Set, Tuple, Optional

class Solution:
    def __init__(self):
        self.memo = {}
    
    def __findPaths(self, m: int, n: int, maxMove: int, startRow: int, startColumn: int) -> int:
        if startRow < 0 or startRow >= m or startColumn < 0 or startColumn >= n:
            return 1

        if maxMove == 0:
            return 0

        args = (startRow, startColumn, maxMove)
        if args in self.memo:
            return self.memo[args]

        pathCount  = self.findPaths(m, n, maxMove - 1, startRow - 1, startColumn)
        pathCount += self.findPaths(m, n, maxMove - 1, startRow, startColumn + 1)
        pathCount += self.findPaths(m, n, maxMove - 1, startRow + 1, startColumn)
        pathCount += self.findPaths(m, n, maxMove - 1, startRow, startColumn - 1)

        self.memo[args] = pathCount
        return pathCount

    def findPaths(self, m: int, n: int, maxMove: int, startRow: int, startColumn: int) -> int:
        pathCount = self.__findPaths(m, n, maxMove, startRow, startColumn)
        return pathCount % (1000000007)

if __name__ == "__main__":
    inputs = [
        #(10, 20, 7, 2, 3),
        #(8, 7, 16, 1, 5),
        (8, 50, 23, 5, 26)
    ]
    for i in inputs:
        m, n, maxMove, startRow, startColumn = i
        s = Solution()
        print('path count @(m = {}, n = {}, maxMove = {}, startRow = {}, startColumn = {}) = {}'.format(m, n, maxMove, startRow, startColumn, s.findPaths(m, n, maxMove, startRow, startColumn)))
