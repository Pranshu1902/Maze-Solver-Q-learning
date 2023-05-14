# Maze Solver using Q-Learning

class Maze:
    def __init__(self):
        # 2 means target, 3 means start, 0 means path, -1 means wall
        self.maze = [
            [2, 0, 0, -1, -1],
            [0, 0, -1, -1, -1],
            [-1, 0, -1, -1, -1],
            [-1, 0, 0, 0, 3]
        ]
        self.length = 5
        self.height = 4
        self.q = []
        self.visited = []
        self.pointer = {}
        self.learningRate = 0.1

        self.original_maze = [
            [2, 0, 0, -1, -1],
            [0, 0, -1, -1, -1],
            [-1, 0, -1, -1, -1],
            [-1, 0, 0, 0, 3]
        ]
        
        for i in range(self.height):
            arr = []
            for j in range(self.length):
                arr.append(0.0)
            self.q.append(arr)
    
    def get_moves(self, x, y):
        moves = [[x-1, y], [x, y-1], [x, y+1], [x+1, y]]
        if x == 0:
            moves.remove([x-1, y])
        elif x == self.height-1:
            moves.remove([x+1, y])
        
        if y == 0:
            moves.remove([x, y-1])
        elif y == self.length-1:
            moves.remove([x, y+1])
        
        return moves
    
    def reward(self, state, action):
        """Get the reward for an action on a given state"""
        if state[action[0]][action[1]] == 2:
            return 10.0
        elif state[action[0]][action[1]] == 1:
            return 0.0
        elif state[action[0]][action[1]] == 0:
            return 5.0
        else:
            return -1.0

    def explore(self):
        self.currentX = 3
        self.currentY = 4

        self.recursion(self.currentX, self.currentY)
        
    
    def recursion(self, X, Y):
        if X == 0 and Y == 0:
            return
        moves = self.get_moves(X, Y)

        for x,y in moves:
            # Q = Q + alpha*reward
            self.q[x][y] += self.learningRate * self.reward(self.maze, [x, y])
            self.maze[X][Y] = 1

            if self.maze[x][y] != 1:
                self.recursion(x, y)
    
    def show(self, path):
        for x in range(self.height):
            for y in range(self.length):
                if self.original_maze[x][y] == 2:
                    print("B", end='')
                elif self.original_maze[x][y] == 3:
                    print("A", end='')
                elif self.original_maze[x][y] == -1:
                    print("#", end='')
                elif [x, y] in path:
                    print(" ", end='')
                else:
                    print("-", end='')
            print()

    def print_path(self):
        self.currentX = 3
        self.currentY = 4
        path = [[self.currentX, self.currentY]]
        while self.currentX != 0 or self.currentY != 0:
            # index with highest q value among the neighbours
            if self.q[self.currentX][self.currentY-1] > self.q[self.currentX-1][self.currentY]:
                path.append([self.currentX, self.currentY-1])
                self.currentY -= 1
            else:
                path.append([self.currentX-1, self.currentY])
                self.currentX -= 1

        print("Q-Learning table:\n")
        for i in self.q:
            print(i)
        
        print("\n\nMaze:\n")
        self.show(path)

ai = Maze()
ai.explore()
ai.print_path()
