from utils import *
from grid import *
"""
This file will hold all search functions and the point expansion function
"""
def Valid_Move(node, enclosures):
    for polygon in enclosures:
        poly_points = {point.to_tuple() for point in polygon}

        if node.to_tuple() in poly_points:
            return False
    for dx, dy in [ (0,1), (1,0), (0, -1), (-1, 0), (1,1), (1,-1), (-1,1), (-1,-1) ]:
        if (node.x + dx, node.y + dy) in poly_points:
            return False
    
    return True

def Expand(point, enclosures):
    directions = [ Point(0, 1), Point(1, 0), Point(0, -1), Point(-1, 0) ]
    children = []
    for d in directions:
        child = Point(point.x + d.x, point.y + d.y)
        
        if Valid_Move(child, enclosures):
            children.append(child)
    return children

def ActionCost(point, action, next_point):
    # if next_point not on or in obstacle: return 1
    # if next_point on or inside of turf: return 1.5
    pass

def BFS(source, dest, enclosures, turfs): # this works, but need to make sure that the path avoids enclosures
    frontier = Queue()
    frontier.push([source]) # store the paths instead of just a point
    visited = set()
    visited.add( source.to_tuple() )

    while not frontier.isEmpty():# while the frontier queue aint empty...

        path = frontier.pop() # pop the next Point
        node = path[-1]

        if node == dest:
            return path
        
        for child in Expand(node, enclosures):
            
            if child.to_tuple() not in visited:
                visited.add( child.to_tuple() )
                frontier.push(path + [child] )

    return None


def DepthFirstSearch():
    pass

def GreedyBFS():
    pass

def A_Star():
    pass