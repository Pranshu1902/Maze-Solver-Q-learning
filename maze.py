# Maze Solver using Q-Learning

class Maze:
    def __init__(self, maze, original_maze, length, height, startX, startY):
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
            self.q[x][y] += self.learningRate * self.reward(self.maze, [x, y])
            self.maze[X][Y] = 1

            if self.maze[x][y] == -1:
                print("Epoch: " + str(self.epochs))
                self.epochs += 1
                self.show(path)
                # self.print_path()
                # return

            elif self.maze[x][y] != 1:
                path.append([x, y])
                self.recursion(x, y, path)
    
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
                    print("X", end='')
            print()
        print("\n\n")


    def print_path(self):
        path = [[self.currentX, self.currentY]]
        visited = [[self.currentX, self.currentY]]
        while self.currentX != 0 or self.currentY != 0:
            # index with highest q value among the neighbours
            
            # x, y-1 is best move
            # if self.currentY>0 and (self.currentX > 0 and self.q[self.currentX][self.currentY-1] > self.q[self.currentX-1][self.currentY]) and (
            #     self.currentX < self.height-1 and self.q[self.currentX][self.currentY-1] > self.q[self.currentX+1][self.currentY] 
            # ) and (
            #     self.currentY < self.length-1 and self.q[self.currentX][self.currentY-1] > self.q[self.currentX][self.currentY+1] 
            # ):
            #     path.append([self.currentX, self.currentY-1])
            #     self.currentY -= 1
            
            # # x, y+1 is best move
            # elif self.currentY<self.length-1 and (self.currentX > 0 and self.q[self.currentX][self.currentY+1] > self.q[self.currentX-1][self.currentY]) and (
            #     self.currentX < self.height-1 and self.q[self.currentX][self.currentY+1] > self.q[self.currentX+1][self.currentY] 
            # ) and (
            #     self.currentY < self.height-1 and self.q[self.currentX][self.currentY+1] > self.q[self.currentX][self.currentY+1] 
            # ):
            #     path.append([self.currentX, self.currentY-1])
            #     self.currentY += 1
            
            # # x-1, y is best move
            # elif self.currentX>0 and (
            #     self.currentY < self.length-1 and self.q[self.currentX-1][self.currentY] > self.q[self.currentX][self.currentY+1] 
            # ) and (
            #     self.currentY > 0 and self.q[self.currentX-1][self.currentY] > self.q[self.currentX][self.currentY-1] 
            # ) and (
            #     self.currentX <self.height-1 and self.q[self.currentX-1][self.currentY] > self.q[self.currentX+1][self.currentY] 
            # ):
            #     path.append([self.currentX, self.currentY-1])
            #     self.currentX -= 1
            
            # # x+1, y is best move
            # else:
            #     path.append([self.currentX-1, self.currentY])
            #     self.currentX += 1
            
            # 2nd approach
            d = {}
            
            if self.currentX > 0:
                d[(self.currentX-1, self.currentY)] = self.q[self.currentX-1][self.currentY]
            
            if self.currentX < self.height-1:
                d[(self.currentX+1, self.currentY)] = self.q[self.currentX+1][self.currentY]
            
            if self.currentY > 0:
                d[(self.currentX, self.currentY-1)] = self.q[self.currentX][self.currentY-1]
            
            if self.currentY < self.length-1:
                d[(self.currentX, self.currentY+1)] = self.q[self.currentX][self.currentY+1]

            nextQ = max(d.values())

            for k,v in d.items():
                if v == nextQ and [k[0], k[1]] not in visited:
                    # print(k[0], k[1])
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

# 3 -> start
# 2 -> end
# -1 -> wall
# 0 -> path

maze = [
    [2, 0, 0, -1, -1],
    [0, 0, -1, -1, -1],
    [-1, 0, -1, -1, -1],
    [-1, 0, 0, 0, -1],
    [0, 0, 0, -1, 3],
    [0, 0, -1, 0, 0],
    [-1, 0, -1, 0, -1],
    [-1, 0, 0, 0, -1]
]

original_maze = [
    [2, 0, 0, -1, -1],
    [0, 0, -1, -1, -1],
    [-1, 0, -1, -1, -1],
    [-1, 0, 0, 0, -1],
    [0, 0, 0, -1, 3],
    [0, 0, -1, 0, 0],
    [-1, 0, -1, 0, -1],
    [-1, 0, 0, 0, -1]
]

length = len(maze[0])
height = len(maze)

startX = startY = 0
for i in range(len(maze)):
    if 3 in maze[i]:
        startX = i
        startY = maze[i].index(3)
        break


ai = Maze(maze, original_maze, length, height, startX, startY)
ai.explore()

# ai.train()

# ai.print_path()
