import random
import math
import collections


class Maze(object):
    """
    Create the maze, and also the solution
    """

    def __init__(self, row=41, col=41):
        # make sure its odd number
        self.row_size = int(row / 2) * 2 + 1
        self.col_size = int(col / 2) * 2 + 1
        # init maze map, a two dimension list with the row_size and col_size
        self.maze_map = [[0 for x in range(self.col_size)] for y in range(self.row_size)]
        # create the maze map
        self.init_map()
        self.make_row()
        (self.start_p, self.end_p) = self.start_end_point()


    def display(self):
        """
        You can print a maze at terminal
        :return:
        """
        for i in self.maze_map:
            print(i)


    def init_map(self):
        """
        create a m*m list(array) as maze
        :return:
        """
        for row in range(self.col_size):
            for col in range(self.row_size):
                if row % 2 == 0 or col % 2 == 0:
                    self.maze_map[col][row] = 1


    def make_row(self):
        """
        implement dfs to create the maze
        """
        stack = []
        self.visted = [] # visited point
        rp = self.random_point(self.col_size, self.row_size) # random point
        stack.append(((1,1)))
         # when stack is not empty
        while stack:
            cp = stack.pop()
            # create more interesection, make the game harder
            if random.random() < 0.8:
                self.visted.append(cp)
            # create path, new point
            np = self.get_next_point(cp)
            if np:
                stack.append(cp)
                stack.append(np)


    def get_next_point(self, p):
        """
        get a random neighbout of point 'p'
        """
        x, y = p[0], p[1]
        directions = list(range(4))
        random.shuffle(directions)
        for i in directions:
            # the point after the next-point
            (a, b) = self.get_arround(x, y, i, 2)
            if not a or a >= self.row_size or a <= 0 or b >= self.col_size or b <= 0:  # if valid
                continue
            if (a, b) in self.visted:  # if visited
                continue
            # if satisfied the both condition, create a path, and return it
            (c, d) = self.get_arround(x, y, i, 1)
            self.maze_map[c][d] = 0
            return (a, b) # return
        return None


    def get_arround(self, x, y, direction, distance=1):
        """
        get point, at (x,y) from 'direction'
        """
        a, b = 0, 0
        if direction == 0:
            a, b = x, y - distance
        elif direction == 1:
            a, b = x + distance, y
        elif direction == 2:
            a, b = x, y + distance
        elif direction == 3:
            a, b = x - distance, y
        if a >= self.row_size or a <= 0 or b >= self.col_size or b <= 0:  # with in the row and col size
            return None, None
        else:
            return (a, b)


    def adj(self, x, y):
        """
        get adj(not wall)
        """
        ls = []
        for d in range(4):
            np = self.get_arround(x, y, d, 1) # get point at (x,y) from 'd'
            if np[0] is None:
                continue
            elif self.maze_map[np[0]][np[1]] != 1:
                ls.append(np)
        return ls


    def random_point(self, row, col):
        """
        generate a point between 'row' and 'col', coulbe be either path or wall
        """
        return (random.randint(0, row - 1), random.randint(0, col - 1))


    def start_end_point(self):
        """
        create entrance and exit
        """
        while True:
            while True:
                start_p = self.random_point(self.row_size, self.col_size)
                if self.maze_map[start_p[0]][start_p[1]] == 0:
                    break
            while True:
                end_p = self.random_point(self.row_size, self.col_size)
                if self.maze_map[end_p[0]][end_p[1]] == 0:
                    break
            dy = math.fabs(start_p[1] - end_p[1])
            dx = math.fabs(start_p[0] - end_p[0])
            if dx + dy > (self.col_size + self.row_size) / 2:
                return (start_p, end_p)


    def solve(self, start_point):
        '''Solve a path from certain point to exit
        for 'coint path' - red block - bonus
        '''
        queue = []
        father = {}
        visted = []
        queue.append(start_point)
        while True:
            cp = queue.pop(0)
            visted.append(cp)
            if cp == self.end_p:
                break
            for np in self.adj(*cp):
                if np and np not in visted:
                    queue.append(np)
                    father[np] = cp
        cp = self.end_p
        for i in range(len(father)):
            fp = father.get(cp)
            if fp == self.start_p:
                break
            else:
                cp = fp
                if cp:
                    self.maze_map[cp[0]][cp[1]] = 7


# for testing only!!
if __name__ == "__main__":
    m = Maze(20, 20)
    # path = m.solve_bf(m.start_p)
    # m.display() # print the map at terminal
