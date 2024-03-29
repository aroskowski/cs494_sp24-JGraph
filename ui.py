#!/usr/bin/env python3
import sys
import re 


#=============================================================================
#                           Globals
#=============================================================================
jgr = open("floorplan.jgr", "w")
#jgr.write(f"newgraph\nxaxis nodraw\nyaxis nodraw\n\n");
pts = []
roompts = []

#=============================================================================
#                       Calculation Functions
#=============================================================================
def perimeter(org, uin): 
    #e10n4e2n6w12s10
    points = []
    points.append((float(org[0]), float(org[1])));

    #regular expression looking for (char)(ints)
    for i in re.findall(r"([a-z]+)([0-9]+)", uin): 
        x = points[len(points)-1][0]; #get x & y coords
        y = points[len(points)-1][1];
        
        #edit points based on direction
        if "n" in i[0]:
            y += int(i[1])
        elif "e" in i[0]:
            x += int(i[1])
        elif "s" in i[0]:
            y -= int(i[1])
        elif "w" in i[0]:
            x -= int(i[1])
        points.append((x,y)); #add to list of points

    if(points[len(points) - 1] != points[0]):
        return (False, points);
    return (True, points);
def find_min_max(points):
    x_vals = [];
    y_vals = [];
    for i in points:
        x_vals.append(i[0]);
        y_vals.append(i[1]);
    return (max(x_vals), min(x_vals), max(y_vals), min(y_vals))

#=============================================================================
#                       JGraph Interaction Functions
#=============================================================================
def jgraph_setup(points):
    xmax, xmin, ymax, ymin = find_min_max(points);
    xmin -= 2;
    ymin -= 2;
    xmax += 2;
    ymax += 2;
    jgr.write(f"newgraph\nxaxis min {xmin} max {xmax} nodraw\nyaxis min {ymin} max {ymax} nodraw\n\n");

def print_external(points):
    jgr.write("newline linethickness 2 color 0 0 0 pts\n")
    for i in points:
        jgr.write(f"{i[0]} {i[1]}\n")
    jgr.write("\n")

def print_internal(roompts):
    jgr.write("newline linethickness 2 color .3 .3 .3 pts\n")
    for i in roompts:
        jgr.write(f"{i[0]} {i[1]}\n")
    jgr.write("\n")

def place_door(org, angle):
    jgr.write("newcurve eps ./entities/door.ps ");
    if(angle == 'w'):
        jgr.write("marksize -13 15 ")
    else:
        jgr.write("marksize 13 15 ")
    if(angle == 'n'):
        jgr.write("mrotate 90 ")
    elif(angle == 's'): 
        jgr.write("mrotate -90 ")
    jgr.write(f"pts {org[0]} {org[1]}\n\n") 

def place_windows(org, uin):
    points = [];
    test, points = perimeter(org, uin);
    jgr.write("newline linethickness 2.2 color .2 .3 1 pts\n");
    for i in points:
        jgr.write(f"{i[0]} {i[1]}\n")
    jgr.write("\n")

def place_label(org, uin):
    jgr.write(f"newstring hjc vjc x {org[0]} y {org[1]} fontsize 12 : {uin}\n\n");

#=============================================================================
#                       Main Function
#=============================================================================
org = input("Enter the orgin point (x y): ");
org = org.split(" ");
uin = input("Enter Exterior Dimensions: ");
test, pts = perimeter(org, uin)
if(not test):
    print("Invalid input.\nEnter directions to walk the perimeter of the building using n (north), e (east), s (south), or w (west) followed by the number of feet to continue in this direction before another turn.\n", file=sys.stderr);

jgraph_setup(pts);

num = int(input("Enter number of rooms: "));
for i in range(num):
    org = input("Enter the orgin point for the room (x y): ");
    org = org.split(" ");
    uin = input("Enter Interior Dimesions: ");
    test, roompts = perimeter(org, uin);
    if (not test):
        print("Room error. pts did not line up", file=sys.stderr);
    print_internal(roompts);
print_external(pts);

print("\nPossible components to place are: window, door, or label\nOr enter \"quit\" to complete the floorplan.\n");
while(True):
    comp = input("Enter component to place: ")
    if (comp == "quit"):
        break;
    elif (comp == "door"):
        org = input("Enter the orgin point of the door hinge: ");
        org = org.split(" ");
        angle = input("Direction of the door to open (n,e,s,w): ");
        place_door(org, angle);
    elif (comp == "window"):
        org = input("Enter the orgin point of the window: ");
        org = org.split(" ");
        uin = input("Enter window dimensions: ");
        place_windows(org, uin);
    elif (comp == "label"):
        org = input("Enter the center point of the label: ");
        org = org.split(" ");
        uin = input("Enter the label to add: ");
        place_label(org, uin);
    else:
        print("Not a valid component.\n");
