import matplotlib.pyplot as plt
import numpy as np
import time
import matplotlib.animation as animation

from utils import *
from grid import *
from SearchandExpand import *

def gen_polygons(worldfilepath):
    polygons = [] # will hold the shapes for enclosures or turfs
    with open(worldfilepath, "r") as f:# read file line by line
        lines = f.readlines() # take in each line and add it to the array of lines
        lines = [line[:-1] for line in lines] # remove newline char at the end of each line
        for line in lines: # go through each line
            polygon = [] # set a list for something
            pts = line.split(';') # split each line at the semicolon to extract the coordinate tuple and adds them to the list pts
            for pt in pts:
                xy = pt.split(',') # separate each points in pts into onelist of x and y val
                polygon.append(Point(int(xy[0]), int(xy[1]))) # add the point object to the polygon list. one polygon is being created in each outer for loop iteration
            polygons.append(polygon) # add the polygon to the polygonslist
    return polygons # return the set of enclosures or turfs

"""
so the 'node' in this project is 'Point' and it contains X and Y values. When expanding each point, the order is always up, right, down, left
the code should implement the pseudocode
"""

if __name__ == "__main__":

    # reading enclosure and turf coordinate information
    epolygons = gen_polygons('Search/TestingGrid/world1_enclosures.txt')
    tpolygons = gen_polygons('Search/TestingGrid/world1_turfs.txt')

    # set the start and end points
    source = Point(8,10)
    dest = Point(43,45)

    # draw the board, grids, the start point on the grid and the end point on the grid
    fig, ax = draw_board()
    draw_grids(ax)
    draw_source(ax, source.x, source.y)  # source point
    draw_dest(ax, dest.x, dest.y)  # destination point
    
    # Draw enclosure polygons: points first, then the lines to connect the dots
    for polygon in epolygons:
        for p in polygon:
            draw_point(ax, p.x, p.y)
    for polygon in epolygons:
        for i in range(0, len(polygon)):
            draw_line(ax, [polygon[i].x, polygon[(i+1)%len(polygon)].x], [polygon[i].y, polygon[(i+1)%len(polygon)].y])
    
    # Draw turf polygons: first the dots, then the lines to connect
    for polygon in tpolygons:
        for p in polygon:
            draw_green_point(ax, p.x, p.y)
    for polygon in tpolygons:
        for i in range(0, len(polygon)):
            draw_green_line(ax, [polygon[i].x, polygon[(i+1)%len(polygon)].x], [polygon[i].y, polygon[(i+1)%len(polygon)].y])

    #### Here call your search to compute and collect res_path
    # seems like the search is supposed to just collect points. The for loop at the end is drawing the line for the path.
    # the res_path var is a list that holds Point variables

    res_path = DFS(source, dest, epolygons, tpolygons)

    
    for i in range(len(res_path)-1):
        draw_result_line(ax, [res_path[i].x, res_path[i+1].x], [res_path[i].y, res_path[i+1].y])
        plt.pause(0.1)
    
    plt.show()