from utils import *
from grid import *
import math

"""
This file will hold all search functions and the point expansion function
"""
def Summarize(algo, pathcost, expansions):
    with open('summary.txt', 'a') as summary:
        summary.write(f'{algo}:\nPath Cost; {pathcost}\nNodes Expanded: {expansions}\n')

def point_on_segment(p, p1, p2, eps=1e-10):
   
    # Check for collinearity via the cross product.
    cross = (p.y - p1.y) * (p2.x - p1.x) - (p.x - p1.x) * (p2.y - p1.y)
    if abs(cross) > eps:
        return False
    
    # Ensure that p lies between p1 and p2.
    if (min(p1.x, p2.x) - eps <= p.x <= max(p1.x, p2.x) + eps and 
        min(p1.y, p2.y) - eps <= p.y <= max(p1.y, p2.y) + eps):
        return True
    
    return False


def point_in_polygon(point, polygon):
    
    # First, if the point is on any edge, consider it inside.
    n = len(polygon)
    for i in range(n):

        if point_on_segment(point, polygon[i], polygon[(i+1) % n]):
            return True

    # Otherwise, use the ray-casting method.
    inside = False
    x, y = point.x, point.y

    for i in range(n):

        j = (i + n - 1) % n
        xi, yi = polygon[i].x, polygon[i].y
        xj, yj = polygon[j].x, polygon[j].y
        
        if ((yi > y) != (yj > y)):
            x_intersect = (xj - xi) * (y - yi) / (yj - yi + 1e-10) + xi

            if x < x_intersect:
                inside = not inside

    return inside


def Valid_Move(node, enclosures):

    for polygon in enclosures:

        if point_in_polygon(node, polygon):
            return False
        
    return True


def Expand(point, enclosures):
    directions = [
        Point(0, 1), Point(1, 0), Point(0, -1), Point(-1, 0)
    ]

    children = []

    for d in directions:

        child = Point(point.x + d.x, point.y + d.y)

        if Valid_Move(child, enclosures):
            children.append(child)

    return children


def InTurf(point, turfs):
    for polygon in turfs:
        if point_in_polygon(point, polygon):
            return True
        
        return False


def ActionCost(point, turfs):
    if InTurf(point, turfs):
        return 1.5
    else:
        return 1.0


def BFS(source, dest, enc, turfs):
    frontier = Queue()
    frontier.push([source])
    visited = set( [source.to_tuple()] )
    nodes_expanded = 0
    path_cost = 0.0

    while frontier:

        path = frontier.pop()
        curr_point = path[-1]
        nodes_expanded += 1

        for child in Expand(curr_point, enc):

            if child.to_tuple() in visited:
                continue

            new_path = path + [child]

            if child == dest:

                for i in range(1, len(path)):
                    path_cost += ActionCost(path[i], turfs)
                Summarize('GreedyBFS', path_cost, nodes_expanded)

                return new_path
            
            visited.add(child.to_tuple())
            frontier.push((child, new_path))
    
    return []


def DFS(source, dest, enc, turfs):
    
    frontier = Stack()
    frontier.push([source])
    visited = set( [source.to_tuple()] )
    nodes_expanded = 0
    path_cost = 0.0

    while frontier:
        path = frontier.pop()
        curr_point = path[-1]
        nodes_expanded += 1

        if curr_point == dest:

            for i in range(1, len(path)):
                path_cost += ActionCost(path[i], turfs)
            Summarize('DFS', path_cost, nodes_expanded)

            return path
        
        for child in Expand(curr_point, enc):
            
            if child.to_tuple() not in visited:
                
                new_path = path + [child]

                visited.add( child.to_tuple() )
                frontier.push( new_path )
    
    return []


def heuristic(node, dest):
    rx = node.x - dest.x
    ry = node.y - dest.y
    
    return math.sqrt( rx*rx + ry*ry )


def GreedyBFS(source, dest, enc, turfs):
    frontier = PriorityQueue()
    visited = set()
    expansion_count = 0
    path_cost = 0.0

    frontier.push( [source], heuristic(source, dest) )
    visited.add( source.to_tuple() )

    while frontier:
        path = frontier.pop()
        expansion_count += 1
        current = path[-1]

        if current == dest:
            for i in range(1, len(path)):
                path_cost += ActionCost(path[i], turfs)
            Summarize('GreedyBFS', path_cost, expansion_count)
            return path
        
        for child in Expand(current, enc):
            if child.to_tuple() not in visited:

                visited.add(child.to_tuple())
                new_path = path + [child]
                heuristic_val = heuristic(child, dest)
                frontier.push( new_path, heuristic_val )
    return []


def A_Star(source, dest, enc, turfs):
    frontier = PriorityQueue()
    optimal_costs = {}
    start_cost = 0.0
    node_expansions = 0
    path_cost = 0.0

    frontier.push( ([source], start_cost), (start_cost + heuristic(source, dest)) )
    optimal_costs[source.to_tuple()] = 0.0

    while frontier:
        (path, cost) = frontier.pop()
        node_expansions += 1

        current = path[-1]

        if current == dest:
            for i in range(1, len(path)):
                path_cost += ActionCost(path[i], turfs)
            
            Summarize('A-Star', path_cost, node_expansions)
            return path
        
        for child in Expand(current, enc):
            coord = child.to_tuple()
            next_price = ActionCost(child, turfs)
            new_cost = cost + next_price

            if coord not in optimal_costs or new_cost < optimal_costs[coord]:
                optimal_costs[coord] = new_cost
                new_path = path + [child]
                f_val = new_cost + heuristic(child, dest)
                frontier.push( (new_path, new_cost), f_val )