import numpy as np
from timeit import Timer
from coordinates import Coordinate


a = Coordinate(x=4, y=3)
b = Coordinate(x=8, y=-4)
c = Coordinate(x=12, y=-1)
d = Coordinate(x=0, y=-3)
e = Coordinate(x=7, y=9)
f = Coordinate(x=2, y=-5)
g = Coordinate(x= 4.5, y= 2.5)

points = [a, b, c, d, e, f, g]
# x, y = symbols('x, y')

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

def merge_points(points):
    multiplier = float(0.05)
    ''' The order of creating the list is very important
        since the arrays always change when refered to later
        in the code '''
    y_values = insertion_sort(points, 'y')

    # Created second, so now points will be arranged according to x-axis
    # Ideally, just call insertion_sort evertime to stay safe
    x_values= insertion_sort(points, 'x')

    # Define the distance between extremes on x and y axis
    # Notice that ['x'] and ['y'] is still required as I'm using whole coordinates that are just ARRANGED according to x and y 
    # Multiplier is 5% of the total range, the scale by which I decide if 2 points are too close

    x_scale = abs(multiplier * float(x_values[-1]['x'] - x_values[0]['x']))
    y_scale = abs(multiplier * float(y_values[-1]['y'] - y_values[0]['y']))

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
                # If y < 5% too, find midpoint
                x1 = float(x_values[j]['x'])
                x2 = float(x_values[j + 1]['x'])
                y1 = float(x_values[j]['y'])
                y2 = float(x_values[j + 1]['y'])

                # Midpoint formula
                x_new = (x1 + x2)/2.0
                y_new = (y1 + y2)/2.0
                
                ''' Create merged coord and replace the [j+1] coord with it for 
                    the next loop when [j+1] is compared to [j+2] '''

                merged_coord = Coordinate(x = x_new, y = y_new)
                x_values[j+1] = merged_coord
                merged_list.append(merged_coord)

                # Set merged status as true
                merged = True

            else:
                if merged == False:
                    ''' If the y check failed, and the [j] element
                        isn't a merged one, then replace it with the original'''
                    org_coord = x_values[j]
                    merged_list.append(org_coord)

                    # Set status to false
                    merged = False
                else:
                    ''' If [j] element was merged, then no need to
                        append it so just change the status'''
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

    return(merged_list)

def plot_map(list):
    # List is the merged list
    east = list[-1]
    west = list[0]

    list = insertion_sort(list, 'y')
    north = list[-1]
    south = list[0]

    print('North: ', north)
    print('South: ', south)
    print('East: ', east)
    print('West: ', west)


# Run the program
merged_list = merge_points(points)
plot_map(merged_list)

'''
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
NO NEED FOR Y_LIST TO EXIST, CAN BE SIMPLIFIED TO JUST FINDING
THE EXTREMES FOR Y. X_LIST IS NEEDED SINCE IT IS USED TO MERGE
ELEMENTS, BUT Y HENCE IS NOT REQUIRED. CAN SIMPLIFY CODE THERE.

'''


# FIND EXTREMES
    # Implement sort algorithm to find which points are the max and min for x and y

# MERGE POINTS
    # Find diff between max and min x and y values.
    # If diff between two points is 5% or less than that of the max diff on that axis, take note of merge
    # Once one 5% less is found, no need to check the other axis, as merging will ensure to merge points completely anyways if other axis is also 5%
    # Update new number of points, while also updating new extreme values

# PLOT MAP
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



            
            






























'''
equation_1 = ( ((b[0]-x)**2 + (b[1]-y)**2) - ((a[0]-x)**2 + (a[1]-y)**2))
equation_2 = ( ((c[0]-x)**2 + (c[1]-y)**2) - ((a[0]-x)**2 + (a[1]-y)**2))

equation_1 = simplify(equation_1)
equation_2 = simplify(equation_2)

const1 = -int(equation_1.coeff(x,0)- y*equation_1.coeff(y,1))
const2 = -int(equation_2.coeff(x,0)- y*equation_2.coeff(y,1))

x1 = int(equation_1.coeff(x,1))
y1 = int(equation_1.coeff(y,1))

x2 = int(equation_2.coeff(x,1))
y2 = int(equation_2.coeff(y,1))


A = np.array([[x1, y1], [x2, y2]])


B = np.array([const1, const2])


ans = np.linalg.solve(A,B)


rad = ( ((a[0]-ans[0]) ** 2) + ((a[1]-ans[1]) ** 2) )


final = f'(x - {ans[0]}) ** 2 + (y - {ans[1]}) ** 2 = {rad}'
print(final)
'''






