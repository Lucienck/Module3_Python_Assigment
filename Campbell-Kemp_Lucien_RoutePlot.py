from os.path import exists

# Function to read the starting coordinates and directions to calculate the drone's postions
# and pouplate a 2D array (list) with the route to be pliotted
def populate_grid(filename, coord_list):
    grid = []

    ## Create storage for grid and pre-populates each cell with a space (ASCII 32)
    for x in range (13):
        grid.append([' ' for y in range(13)])

    # Get starting coords from file
    # Open file using "with" to ensure automatic closure after all data has been read from it
    with open(filename, 'r') as routefile:
        # Read initial X and Y coordinates
        x = int(routefile.readline())
        y = int(routefile.readline())

        # Populate cell in 2D list specified by y,x 
        grid[y][x] = 'x'
        # Append read X and Y coordinates as a coordinate string to coord_list (for subsequent printing)
        coord_list.append("({}, {})".format(x,y))

        ## Now read the directions from the remainder of the file
        for direction in routefile:
            direction = direction.strip()   # Remove trailing CR as we only want to match the letter representing the compass direction
            # Alter the coordinate in X or Y according to the compass direction
            match direction:
                case 'N':
                    y += 1
                case 'E':
                    x += 1
                case 'S':
                    y -= 1
                case 'W':
                    x -= 1

            # If any coord is outside of the grid in X or Y then we need set grid to "error" and return it
            if x < 0 or x > 12 or y < 0 or y > 12:
                grid = "error"
                return grid
 
            # Populate cell in 2D list specified by y,x 
            grid[y][x] = 'x'
            # Append read X and Y coordinates as a coordinate string to coord_list (for subsequent printing)
            coord_list.append("({}, {})".format(x,y))
    
    return grid

# Function to print all of the coordinates of the plotted route
def print_coords(coord_list):
    print("Coordinates")
    for coord in coord_list:
        print(coord)


def plot_file(filename):
    ## 2D list (array) to populate with plotted positions
    grid = []
    blank_line = ""
    colon_line = "   :" * 13
    cell_divder = ("---:" * 13) + "---"
    coord_list = []

    # Call populate_grid function to read the starting coordinates and directions from the supplied file and populate "grid" (2D list)
    grid = populate_grid(filename, coord_list)

    # Display the filename from which the coordinates have been read
    print(filename)
    print(blank_line)

    if grid == "error":
        print("Error: the route is outside of the grid")
        return
 
    ## Print out completed grid
    print("Grid Layout")
    print(colon_line)

    # Print all rows from the top-down (reverse order in the "grid" array)
    for row in range(len(grid)-1, 0, -1):
        print(cell_divder)
        print(f"{row:3}", end='')

        # Print each cell (and colon separator) acoording to the value stored in grid[row][col]
        for col in range(1, len(grid[row])):
            print(": {} ".format(grid[row][col]) , end='')

        print(blank_line)

    # Print final line to show X coordinates
    print(cell_divder)
    print("   : 1 : 2 : 3 : 4 : 5 : 6 : 7 : 8 : 9 :10 :11 :12 :")
   
    # Print blank line
    print(blank_line)

    # Call the print_coords function to print out all the coordinates of the plotted route
    print_coords(coord_list)
    
    # Print blank line
    print(blank_line)


# MAIN code
answer = ""
## Ask user for filename or the "STOP" command
while True:
    # Get uset input into the answer variable
    answer = input("Enter the next route instructions file, or enter STOP to finish: ")
    if answer == "STOP":    # then break out i.e. end program
        break
    else:
        if not exists(answer):
            # File does not exist
            print("File not found")
        else:
            # The file exits - calll the plot_file function to read the data, plot the route, and display the coordinates
            plot_file(answer)
