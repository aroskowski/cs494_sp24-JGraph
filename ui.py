#!/usr/bin/env python3
import sys
import re 

#=============================================================================
#                       Print Functions
#=============================================================================
def print_external(points):
    print("newline linethickness 2 color 0 0 0 " + points);
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
        return False;
    return True;

#=============================================================================
#                       Main Function
#=============================================================================
org = input("Enter the orgin point (x y): ");
org = org.split(" ");
uin = input("Enter Exterior Dimensions: ");
if(not perimeter(org, uin)):
    print("Invalid input.\nEnter directions to walk the perimeter of the building using n (north), e (east), s (south), or w (west) followed by the number of feet to continue in this direction before another turn.\n", file=sys.stderr);

