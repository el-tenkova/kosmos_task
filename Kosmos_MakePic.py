#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
import getopt
import fileinput
import string

import matplotlib
import Tkinter

from pylab import figure
from matplotlib.collections import PolyCollection

import matplotlib.pyplot as plt

def get_points(line):
    points = [] # vertices
    pairs = line.split(",")
    for pair in pairs:
        XY = pair.strip("() ").split(" ");
        points.append([float(XY[0]), float(XY[1])])
    return points

def get_polygons(line):
    polygons = [] # output array
    parts = [] # parts of line
    if line.startswith("MULTIPOLYGON"):
        line = line.strip("MULTIPOLYGON ()")
        parts = line.split("((")
    elif line.startswith("POLYGON"):
       line = line.strip("POLYGON ()")
       parts = [line]
    for item in parts:
        item = item.strip(" )(,")
        points = get_points(item) # get vertices
        if len(points):
            polygons.append(points)
    return polygons

def read_poligons(files):
    poly_coll = [] # collection of polygons
    for line in fileinput.input(files): # read lines from file
        line = line.rstrip()
        parts = line.split("\t")
        if len(parts) != 3:
            print "Format error in data.txt :", line
            continue
         # get polygons from line and add them to collection
        poly_coll = poly_coll + get_polygons(parts[2])
    return poly_coll
    
def main(args):
    opts, files = getopt.getopt(args[1:], '')
    # read data.txt, fill polygons collection
    poly_coll = read_poligons(files)
    
    root = Tkinter.Tk() # get size of screen
    sw = root.winfo_screenmmwidth() / 25
    sh = root.winfo_screenmmheight() / 25
    # start drawing
    fig, ax = plt.subplots()
    fig.set_size_inches(sw, sh)

    ax.add_collection(PolyCollection(poly_coll, alpha=0.05, color='#0099FF'), autolim=True)
    ax.autoscale_view()
    ax.grid(b=True)

    # save to PNG
    fig.savefig("task_data.png")

main(sys.argv) 
