from utils import *
from grid import *

"""
This file will hold all search functions and the point expansion function
"""
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

def ActionCost(point, action, next_point):
    pass

def Breadth_First_Search(source, dest, enc):
    if source == dest:
        return [source]

    frontier = Queue()
    frontier.push((source, [source]))
    visited = set( [source.to_tuple()] )

    while frontier:

        curr_point, path = frontier.pop()

        for child in Expand(curr_point, enc):

            if child.to_tuple() in visited:
                continue

            new_path = path + [child]

            if child == dest:
                return new_path
            
            visited.add(child.to_tuple())
            frontier.push((child, new_path))
    
    return []


def Depth_First_Search(source, dest, enc):
    if source == dest:
        return [source]
    
    frontier = Stack()
    frontier.push( (source, [source]) )
    visited = set( [source.to_tuple()] )

    while frontier:
        curr_point, path = frontier.pop()

        if curr_point == dest:
            return path
        
        for child in Expand(curr_point, enc):
            
            if child.to_tuple() in visited:
                continue
            
            new_path = path + [child]

            visited.add(child.to_tuple())
            frontier.push( (child, new_path) )
    
    return []


def GreedyBFS(source, dest, enc, turf):
    if source == dest:
        return [source]

    frontier = Queue()
    frontier.push((source, [source]))
    visited = set( [source.to_tuple()] )
    path_cost = 0 # 
    expanded_node = 0 # 

    while frontier:

        curr_point, path = frontier.pop()
        expanded_node += 1 # 

        for child in Expand(curr_point, enc):

            if child.to_tuple() in visited:
                continue

            new_path = path + [child]

            if child == dest:
                for i in range(1, len(new_path)):
                    path_cost += self.ActionCost()
                return new_path
            
            visited.add(child.to_tuple())
            frontier.push((child, new_path))
    
    return []

def A_Star(source, dest, enc, turf):
    pass