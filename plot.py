import numpy as np
from timeit import Timer
from coordinates import Coordinate

a = Coordinate(x= 16, y= 5)
b = Coordinate(x= 5, y= -3)
c = Coordinate(x= 14, y= 1)
d = Coordinate(x= 2, y= 8)
e = Coordinate(x= -3, y= 4)
f = Coordinate(x= 15, y= 13)
g = Coordinate(x= 5.65, y= 3.1)
h = Coordinate(x=-15, y=-20)




points = [a,b,c,d,e,f,g,h]

x_coords = []
y_coords = []
for point in points:
    x_coords.append(point['x'])
    y_coords.append(point['y'])

centroid_x = float(sum(x_coords)/len(points))
centroid_y = float(sum(y_coords)/len(points))

centroid = Coordinate(x=centroid_x, y=centroid_y)
print(f'Centroid is: {centroid['x'], centroid['y']}')






































































'''
def insertion_sort(arr, axis):
    # Use an insertion algorithm
    for j in range(len(arr)):
        point = arr[j][axis]
        
        for k in range(j):
            start = arr[k][axis]
            
            if start > point:
                # Make temp the start coordinate pair, NOT just the x-coordinate
                temp = arr[k]
                # Make start the point coordinate
                start_coord = arr[j]
                point_coord = temp
                
                arr[k] = start_coord
                arr[j] = point_coord

    # Return the sorted array
    return(arr)

def merge_points(points, multiplier): 
    #The order of creating the list is very important
    #since the arrays always change when refered to later
    #in the code 

    y_values = insertion_sort(points, 'y')
    y_scale = abs(multiplier * float(y_values[-1]['y'] - y_values[0]['y']))

    # Created second, so now points will be arranged according to x-axis
    # Ideally, just call insertion_sort evertime to stay safe
    x_values= insertion_sort(points, 'x')

    # Define the distance between extremes on x and y axis
    # Notice that ['x'] and ['y'] is still required as I'm using whole coordinates that are just ARRANGED according to x and y 
    # Multiplier is 5% of the total range, the scale by which I decide if 2 points are too close

    x_scale = abs(multiplier * float(x_values[-1]['x'] - x_values[0]['x']))

    # Create an empty merged list and set merged status to false default
    merged_list = []
    merged = False

    # Length of the list
    length = len(x_values)

    # Minus one to offset the end because it's the diff between consecutive elements, so the last one won't work
    for j in range(length - 1):
        start = x_values[j]['x']
        point = x_values[j + 1]['x']

        # Find difference and get absolute value
        x_diff = abs(float(point - start))

        if x_diff <= x_scale:
            # If x is < 5%, then check y to see if it's < 5% too
            start = x_values[j]['y']
            point = x_values[j + 1]['y']

            y_diff = abs(float(point - start))

            if y_diff <= y_scale:
                # Call the midpoint function
                merged_coord = midpoint(x_values[j], x_values[j+1], 0.5)
                x_values[j+1] = merged_coord
                merged_list.append(merged_coord)

                # Set merged status as true
                merged = True

            else:
                if merged == False:
                        #If the y check failed, and the [j] element
                        #isn't a merged one, then replace it with the original
                    org_coord = x_values[j]
                    merged_list.append(org_coord)

                    # Set status to false
                    merged = False
                else:
                    #If [j] element was merged, then no need to
                    #append it so just change the status
                    merged = False

        
        else:
            # Same logic as y but for x here
            if merged == False:
                org_coord = x_values[j]
                merged_list.append(org_coord)
                merged = False
            else:
                merged = False

    # Final one to append the last element if it hasn't been merged
    if merged == False:
        org_coord = x_values[-1]
        merged_list.append(org_coord)

    merge_data = {'list': merged_list, 'multiplier': multiplier}
    return(merge_data)

def plot_centre(data):
    multiplier = data['multiplier']
    list = data['list']

    # Multiplier triples to increase merging and reduce recursive calls
    multiplier *= 3

    # List is the merged list
    east = list[-1]
    west = list[0]

    list = insertion_sort(list, 'y')
    north = list[-1]
    south = list[0]

    points = [north, south, east, west]
 
    points = duplicate(points)

    if len(points) == 2:
        # Straight line
        intersection = midpoint(points[0], points[1], 0.5)

        for item in list:
            if item in points:
                list.remove(item)

    if len(points) == 1:
        # Only one remaining
        intersection = points[0]

        for item in list:
            if item in points:
                list.remove(item)


    if len(points) == 3:
        # Triangle
        AB = midpoint(points[0], points[1], 0.5)
        BC = midpoint(points[1], points[2], 0.5)
        AC = midpoint(points[0], points[2], 0.5)

        for item in list:
            if item in points:
                list.remove(item)
        
        points = [AB, BC, AC]

        intersection = plot_centre(merge_points(points, multiplier))


    if len(points) == 4:
        # Quadrilateral
        NS = midpoint(points[0], points[1], 0.5)
        EW = midpoint(points[2], points[3], 0.5)

        intersection = midpoint(NS, EW, 0.5)

        for item in list:
            if item in points:
                list.remove(item)

    
    if len(list) < 1:
        return intersection

    else:
        list.append(intersection)
        list = insertion_sort(list, 'x')
        # Greater mutliplier to merge points more easily for simplicity and speed
        data = merge_points(list, multiplier)
        intersection = plot_centre(data)

        return intersection




def midpoint(a, b, ratio):
    if not (0 < ratio < 1):
        return AssertionError('Ratio invalid')
    # If ratio is 0.2 (20%) a is considered the one with greater weightage
    # Hence a is 0.8 and b is 0.2
    x1 = float(a['x'])
    x2 = float(b['x'])
    y1 = float(a['y'])
    y2 = float(b['y'])

    x_mid = ((1-ratio) * x1) + (ratio * x2)  
    y_mid = ((1-ratio) * y1) + (ratio * y2)

    mid_coord = Coordinate(x = x_mid, y = y_mid)

    return(mid_coord)
    

def duplicate(list):
     # Create list with only north and south
    filter_list = [list[0], list[1]]
    # Set the values to true. If they become false, they won't be added to the filtered list.
    # East and west check work on the basis that east and west are list[2] and list[3] respectively
    east_check = True
    west_check = True
    # Counter j
    j = 2
    for i in range(2):
        if list[i] == list[i+j]:
            east_check = False

        if list[i] == list[i+j+1]:
            west_check = False
        
        j -= 1

    if east_check == True:
        filter_list.append(list[2])
    if west_check == True:
        filter_list.append(list[3])

    return(filter_list)


# Run the program
data = merge_points(points, 0.05)
middle = plot_centre(data)
x = middle['x']
y = middle['y']
print(f'Coordinates are: ({x}, {y})')


'''


# FIND EXTREMES
    # Implement sort algorithm to find which points are the max and min for x and y

# MERGE POINTS
    # Find diff between max and min x and y values.
    # If diff between two points is 5% or less than that of the max diff on that axis, take note of merge
    # Once one 5% less is found, no need to check the other axis, as merging will ensure to merge points completely anyways if other axis is also 5%
    # Update new number of points, while also updating new extreme values

# PLOT CENTRE
    # Draw lines intersecting NS and EW points to find a midpoint of a quadrilateral.
    # If one point acts as two extremes (i.e NW, SW, NE, SE), draw a triangle.
    # If two points act as two extremes, draw a straight line between the two.
    # If there are no remaining points, exit function since there were only 2-4 points to begin with.
    # Else, call the correct function

# CORRECT FUNCTION
    # Count number of new points, where the original used ones are replaced by the midpoint found previously.
    # Finding new extremes (likely by calling the merge function again).
    # Merge points according to new max and min values.

    # IF no points remaining:
        # Exit

    # ELSE points are still remaining:
        # IF it's only 2-3 points left:
            # Draw line/triangle and find the new midpoint.
            # Find midpoint between new and old midpoints, according to weightage ratio.
            # Exit

        # ELSE there's more than 3 remaining:
            # Run form shape that checks if there are double extremes, finding a new quadrilateral/triangle.
            # Get the new midpoint and check if points remaining (form shape)
            # Repeat steps until no points remaining.


# In essence, there are 3 functions: Merge, Plot, and Correct.
# Merge is seperate.
# Plot uses Merge.
# Correct uses Form.








