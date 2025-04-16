from utils import *
from grid import *
import math

"""
This file will hold all search functions and the point expansion function
"""


def Summarize(algo, pathcost, expansions):
    '''
    This function updates the summary.txt file. Appends information such as which search algorithm
    was used and how many nodes were expanded during the search and the path cost.
    '''
    with open('summary.txt', 'a') as summary:
        summary.write(f'\n{algo}:\nPath Cost: {pathcost}\nNodes Expanded: {expansions}\n')


def point_on_segment(p, p1, p2, eps=1e-10):
    '''
    Checks if current point is on polygon segment.
    '''
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
    '''
    Checks if a point is currently located on/in a polygon
    '''
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
        
        new_x, new_y = point.x + d.x, point.y + d.y

        if 0 <= new_x < 50 and 0 <= new_y < 50:
            child = Point(new_x, new_y)

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
    frontier.push((source, [source]))
    visited = set( source.to_tuple() )
    nodes_expanded = 0
    path_cost = 0.0

    while frontier:

        curr_point, path = frontier.pop()
        nodes_expanded += 1

        for child in Expand(curr_point, enc):

            if child.to_tuple() not in visited:

                new_path = path + [child]

                if child == dest:

                    for i in range(1, len(path)):
                        path_cost += ActionCost(path[i], turfs)
                    Summarize('BFS', path_cost, nodes_expanded)

                    return new_path
                
                visited.add(child.to_tuple())
                frontier.push((child, new_path))
            
    
    return []


def DFS(source, dest, enc, turfs):
    
    frontier = Stack()
    frontier.push( (source, [source]) )
    visited = set( source.to_tuple() )
    nodes_expanded = 0
    path_cost = 0.0

    while frontier:
        curr_point, path = frontier.pop()
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
                frontier.push( (child, new_path) )
    
    return []


def heuristic(node, dest):
    '''
    Find distance to destination from current node
    '''
    rx = node.x - dest.x
    ry = node.y - dest.y
    
    return math.sqrt( rx*rx + ry*ry ) # returns hypotenus = sqrt(rx^2 + ry^2)


def GreedyBFS(source, dest, enc, turfs):
    '''
    Greedy best firat search
    Pops nodes from the frontier with the minimum h(n) value and expands it
    adding valid children nodes to the frontier as well as their respective h(n) val.
    This search algo does not take into account the cost, thus far, of the current path
    it only cares about how small the heuristic value is.
    '''
    frontier = PriorityQueue()
    visited = set()
    expansion_count = 0
    path_cost = 0.0

    frontier.push( [source], heuristic(source, dest) ) # frontier takes tuple( path, heuristic )
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
        
        for child in Expand(current, enc): # expand the popped node and find valid children
            if child.to_tuple() not in visited:

                visited.add(child.to_tuple())
                new_path = path + [child]
                heuristic_val = heuristic(child, dest)
                frontier.push( new_path, heuristic_val )
    return []


def A_Star(source, dest, enc, turfs):
    '''
    A-Star algorithm finds the most efficient path. It takes into account the total path 
    cost and takes the path with minimum cost to the destination. Uses a formula f(n) = g(n) + h(n)
    g(n) => the exact accumulated path cost from the start point to the current point or node
    h(n) => estimated minimum cost from current point or node to the destination

    The algorithm stores the points in the frontier and their g(n) value as a tuple in the frontier PQ 
    and chooses the node with the minimum g(n) value aka cost when deciding which point to pop next
    from the frontier and subsequently exploring
    '''
    frontier = PriorityQueue()
    optimal_costs = {}
    start_cost = 0.0
    node_expansions = 0
    path_cost = 0.0

    # initialize the frontier
    frontier.push( ([source], start_cost), (start_cost + heuristic(source, dest)) )
    optimal_costs[source.to_tuple()] = 0.0


    while frontier:
        # the frontier takes tuple input
        (path, cost) = frontier.pop()
        node_expansions += 1

        # current position is the end of the current path
        current = path[-1]

        # if current point is the destination
        if current == dest:
            for i in range(1, len(path)):
                path_cost += ActionCost(path[i], turfs)
            
            Summarize('A-Star', path_cost, node_expansions)
            return path
        
        # for each child in the current point
        for child in Expand(current, enc):
            coord = child.to_tuple() # get position of current possible move
            next_price = ActionCost(child, turfs) # compute the action cost of moving to this point
            new_cost = cost + next_price # compute total price of moving to the current child point from the start; g(n)

            if coord not in optimal_costs or new_cost < optimal_costs[coord]:
                optimal_costs[coord] = new_cost
                new_path = path + [child]
                f_val = new_cost + heuristic(child, dest) # g(n) + h(n)
                frontier.push( (new_path, new_cost), f_val )