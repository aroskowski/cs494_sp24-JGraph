#!/usr/bin/env python3
import sys
import re 


#=============================================================================
#                           Globals
#=============================================================================
jgr = open("floorplan.jgr", "w")
jgr.write("newgraph\nxaxis min -1 max 25 nodraw\nyaxis min -1 max 25 nodraw\n\n")
pts = []
roompts = []
#=============================================================================
#                       JGraph Interaction Functions
#=============================================================================
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
    jgr.write(f"pts {org[0]} {org[1]}\n") 
#=============================================================================
#                       Calculation Functions
#=============================================================================
def perimeter(org, uin): 
    #e10n4e2n6w12s10
    points = []
    points.append((int(org[0]), int(org[1])));

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

#=============================================================================
#                       Main Function
#=============================================================================
org = input("Enter the orgin point (x y): ");
org = org.split(" ");
uin = input("Enter Exterior Dimensions: ");
test, pts = perimeter(org, uin)
if(not test):
    print("Invalid input.\nEnter directions to walk the perimeter of the building using n (north), e (east), s (south), or w (west) followed by the number of feet to continue in this direction before another turn.\n", file=sys.stderr);

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

print("\nPossible components to place are: door\nOr enter \"quit\" to complete the floorplan.");
while(True):
    comp = input("Enter component to place: ")
    if (comp == "quit"):
        break;
    elif (comp == "door"):
        org = input("Enter the orgin point of the door hinge: ");
        org = org.split(" ");
        angle = input("Direction of the door to open (n,e,s,w): ");
        place_door(org, angle)
    else:
        print("Not a valid component.\n");
