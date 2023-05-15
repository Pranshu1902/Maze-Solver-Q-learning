# Maze Solver using Q-Learning

class Maze:
    def __init__(self, maze, original_maze, length, height, startX, startY, endX, endY):
        # 2 means target, 3 means start, 0 means path, -1 means wall
        self.maze = maze
        self.length = length
        self.height = height
        self.q = []
        self.learningRate = 0.1
        self.epochs = 1
        self.original_maze = original_maze
        self.currentX = startX
        self.currentY = startY
        self.endX = endX
        self.endY = endY
        
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
        path = [[self.currentX, self.currentY]]

        self.recursion(self.currentX, self.currentY, path)

        print("Final output: \n")
        self.print_path()
        
    
    def recursion(self, X, Y, path):
        if X == 0 and Y == 0:
            self.show(path)
            print("Epoch: " + str(self.epochs))
            self.epochs += 1
            return
        moves = self.get_moves(X, Y)

        for x,y in moves:
            # Q = Q + alpha*reward
            self.q[x][y] = round(self.q[x][y] + self.learningRate * self.reward(self.maze, [x, y]), 3)
            self.maze[X][Y] = 4

            if self.maze[x][y] == 3:
                print("Epoch: " + str(self.epochs))
                self.epochs += 1
                self.show(path)
                # self.print_path()
                # return

            elif self.maze[x][y] != 4:
                path.append([x, y])
                self.recursion(x, y, path)
    
    def show(self, path):
        for x in range(self.height):
            for y in range(self.length):
                if self.original_maze[x][y] == 1: # start point
                    print("A", end='')
                elif self.original_maze[x][y] == 3: # wall
                    print("#", end='')
                elif self.original_maze[x][y] == 2: # end point
                    print("B", end='')
                elif [x, y] in path: # traversed path
                    print(" ", end='')
                else: # not chosen path
                    print("X", end='')
            print()
        print("\n\n")


    def print_path(self):
        path = [[self.currentX, self.currentY]]
        visited = [[self.currentX, self.currentY]]

        while self.currentX != self.endX or self.currentY != self.endY:
            # index with highest q value among the neighbours
            d = {}
            
            if self.currentX > 0 and self.original_maze[self.currentX-1][self.currentY] != 3:
                d[(self.currentX-1, self.currentY)] = self.q[self.currentX-1][self.currentY]
            
            if self.currentX < self.height-1 and self.original_maze[self.currentX+1][self.currentY] != 3:
                d[(self.currentX+1, self.currentY)] = self.q[self.currentX+1][self.currentY]
            
            if self.currentY > 0 and self.original_maze[self.currentX][self.currentY-1] != 3:
                d[(self.currentX, self.currentY-1)] = self.q[self.currentX][self.currentY-1]
            
            if self.currentY < self.length-1 and self.original_maze[self.currentX][self.currentY+1] != 3:
                d[(self.currentX, self.currentY+1)] = self.q[self.currentX][self.currentY+1]

            # sort the values in descending order
            sorted(d.items(), key=lambda item: item[1], reverse=True)

            for k,v in d.items():
                if [k[0], k[1]] not in visited: # take the first non-visited state with highest q-value
                    self.currentX = k[0]
                    self.currentY = k[1] 
                    path.append([self.currentX, self.currentY])
                    visited.append([self.currentX, self.currentY])
                    break      

        print("Q-Learning table:\n")
        for i in self.q:
            print(i)
        
        print("\n\nMaze:\n")
        self.show(path)
    
    def train(self):
        for epoch in range(1,11):
            print("\n\nEpoch:", str(epoch))
            self.explore()


# data 

# 0 -> path
# 1 -> start
# 2 -> end
# 3 -> wall

maze = [
    [2, 0, 0, 3, 3],
    [0, 0, 3, 3, 3],
    [3, 0, 3, 3, 3],
    [3, 0, 0, 0, 3],
    [0, 0, 0, 3, 1],
    [0, 0, 3, 0, 0],
    [3, 0, 3, 0, 3],
    [3, 0, 0, 0, 3]
]

original_maze = [
    [2, 0, 0, 3, 3],
    [0, 0, 3, 3, 3],
    [3, 0, 3, 3, 3],
    [3, 0, 0, 0, 3],
    [0, 0, 0, 3, 1],
    [0, 0, 3, 0, 0],
    [3, 0, 3, 0, 3],
    [3, 0, 0, 0, 3]
]

length = len(maze[0])
height = len(maze)

startX = startY = 0
for i in range(len(maze)):
    if 1 in maze[i]:
        startX = i
        startY = maze[i].index(1)
        break

endX = endY = 0
for i in range(len(maze)):
    if 2 in maze[i]:
        endX = i
        endY = maze[i].index(2)
        break

ai = Maze(maze, original_maze, length, height, startX, startY, endX, endY)
ai.explore()

# ai.train()

# ai.print_path()
