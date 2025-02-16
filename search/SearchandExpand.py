from utils import *
from grid import *
"""
This file will hold all search functions and the point expansion function
"""
def Valid_Move():
    pass 

def Expand(point):
    directions = [ Point(0, 1), Point(1, 0), Point(0, -1), Point(-1, 0) ]
    children = []
    for d in directions:
        child = Point(point.x + d.x, point.y + d.y)
        if Valid_Move(child):
            children.append(child)
    return children


def BreadthFirstSearch(source, dest):
    node = source
    if node == dest:
        return node
    
    frontier = Queue()
    reached = set()
    reached.add(node)
    frontier.append(node)

    while not frontier.isEmpty():
        node = frontier.pop()
        for child in Expand(node):
            s = child
            if s == dest:
                return child
            if s not in reached:
                reached.add(s)
                frontier.push(child)
    return []

def DepthFirstSearch():
    pass

def GreedyBFS():
    pass

def A_Star():
    pass