from __future__ import print_function
from heapq import *
import heapq #Hint: Use heappop and heappush

ACTIONS = [(0,1),(1,0),(0,-1),(-1,0)]

class AI:
    def __init__(self, grid, type):
        self.grid = grid
        self.set_type(type)
        self.set_search()

    def set_type(self, type):
        self.final_cost = 0
        self.type = type

    def set_search(self):
        self.final_cost = 0
        self.grid.reset()
        self.finished = False
        self.failed = False
        self.previous = {}

        # Initialization of algorithms goes here
        if self.type == "dfs":
            self.frontier = [self.grid.start]
            self.explored = []
        elif self.type == "bfs":
            self.frontier = [self.grid.start]
            self.explored = []
        elif self.type == "ucs":
            self.frontier = [(0,self.grid.start)]
            self.explored = []
            heapq.heapify(self.frontier)
        elif self.type == "astar":
            dis = abs(self.grid.goal[0] - self.grid.start[0]) +  abs(self.grid.goal[1] - self.grid.start[1])
            self.frontier = [(0 + dis,0,self.grid.start)]
            self.explored = []
            heapq.heapify(self.frontier)
    def get_result(self):
        total_cost = 0
        current = self.grid.goal
        while not current == self.grid.start:
            total_cost += self.grid.nodes[current].cost()
            current = self.previous[current]
            self.grid.nodes[current].color_in_path = True #This turns the color of the node to red
        total_cost += self.grid.nodes[current].cost()
        self.final_cost = total_cost

    def make_step(self):
        if self.type == "dfs":
            self.dfs_step()
        elif self.type == "bfs":
            self.bfs_step()
        elif self.type == "ucs":
            self.ucs_step()
        elif self.type == "astar":
            self.astar_step()
    
    #DFS: BUGGY, fix it first
    def dfs_step(self):
        #check if the frontier is empty or not
        if not self.frontier:
            self.failed = True
            self.finished = True
            print("no path")
            return
        #pops the current node is the frontier
        current = self.frontier.pop()

        # Finishes search if we've found the goal.
        if current == self.grid.goal:
            self.finished = True
            #My line check
            #print("FOUND")
            return
        #adds all of the neighbors
        children = [(current[0]+a[0], current[1]+a[1]) for a in ACTIONS]
        self.grid.nodes[current].color_checked = True
        self.grid.nodes[current].color_frontier = False

        #add node into explored
        self.explored.append(current)
        for n in children:
            if n[0] in range(self.grid.row_range) and n[1] in range(self.grid.col_range):
                if not self.grid.nodes[n].puddle and not n in self.explored and n not in self.frontier:
                    self.previous[n] = current
                    self.frontier.append(n)
                    self.grid.nodes[n].color_frontier = True

    #Implement BFS here (Don't forget to implement initialization at line 23)
    def bfs_step(self):
        #check if the frontier is empty or not
        if not self.frontier:
            self.failed = True
            self.finished = True
            print("no path")
            return
        #main algorithm
        current = self.frontier.pop(0)
        self.explored.append(current)
        #check if goal is found or not
        children = [(current[0]+a[0], current[1]+a[1]) for a in ACTIONS]
        self.grid.nodes[current].color_checked = True
        self.grid.nodes[current].color_frontier = False
        for n in children:
            if n[0] in range(self.grid.row_range) and n[1] in range(self.grid.col_range):
                if not self.grid.nodes[n].puddle and not n in self.explored and not n in self.frontier:
                    self.previous[n] = current
                    if n == self.grid.goal:
                        self.finished = True
                        #My line check
                        #print("FOUND")
                        return
                    self.frontier.append(n)
                    self.grid.nodes[n].color_frontier = True

    #Implement UCS here (Don't forget to implement initialization at line 23)
    def ucs_step(self):
        #check if the frontier is empty or not
        if not self.frontier:
            self.failed = True
            self.finished = True
            print("no path")
            return
        #main algorithm
        poped_Elem = heapq.heappop(self.frontier)
        current = poped_Elem[1]
        current_V = poped_Elem[0]
        if current == self.grid.goal:
            self.finished = True
            #My line check
            #print("FOUND")
            return
        #current node is already seen
        self.explored.append(current)
        #get all of the neighbors
        children = [(current[0]+a[0], current[1]+a[1]) for a in ACTIONS]
        self.grid.nodes[current].color_checked = True
        self.grid.nodes[current].color_frontier = False
        for n in children:
            if n[0] in range(self.grid.row_range) and n[1] in range(self.grid.col_range):
                if not self.grid.nodes[n].puddle:
                    #check if item is in frontier
                    output = [item for item in self.frontier if n in item]
                    cost = 1
                    if self.grid.nodes[n].grass:
                        cost = 10
                    if not n in self.explored and not output:
                        self.previous[n] = current
                        heapq.heappush(self.frontier,(cost + current_V,n))
                        self.grid.nodes[n].color_frontier = True
                    elif output:
                        if output[0][0] > current_V + cost:
                            self.frontier.remove(output[0])
                            heapq.heappush((current_V + cost,n))

    #Implement Astar here (Don't forget to implement initialization at line 23)
    def astar_step(self):
        #check if the frontier is empty or not
        if not self.frontier:
            self.failed = True
            self.finished = True
            print("no path")
            return
        #main algorithm
        poped_Elem = heapq.heappop(self.frontier)
        current = poped_Elem[2]
        current_V = poped_Elem[1]
        if current == self.grid.goal:
            self.finished = True
            #My line check
            #print("FOUND")
            return
        #current node is already seen
        self.explored.append(current)
        #get all of the neighbors
        children = [(current[0]+a[0], current[1]+a[1]) for a in ACTIONS]
        self.grid.nodes[current].color_checked = True
        self.grid.nodes[current].color_frontier = False
        for n in children:
            if n[0] in range(self.grid.row_range) and n[1] in range(self.grid.col_range):
                if not self.grid.nodes[n].puddle:
                    #check if item is in frontier
                    output = [item for item in self.frontier if n in item]
                    cost = 1
                    current_dis = abs(current[0] - self.grid.goal[0]) + abs(current[1] - self.grid.goal[1])
                    distance = abs(n[0] - self.grid.goal[0]) + abs(n[1] - self.grid.goal[1])
                    if self.grid.nodes[n].grass:
                        cost = 10
                    if not n in self.explored and not output:
                        self.previous[n] = current
                        heapq.heappush(self.frontier,(cost + current_V  + distance,current_V + cost,n))
                        self.grid.nodes[n].color_frontier = True
                    elif output:
                        if output[0][0] > current_V  + cost + distance:
                            self.frontier.remove(output[0])
                            heapq.heappush(self.frontier,(current_V  + cost + distance,current_V + cost, n))
        
        
