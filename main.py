import random
import math
grid = []
mines = []
minesCount = 0
flags = []
size = 0
firstClick = True


def Init():
    """
    Initialisation, in case if I want to implement save game function
    """
    ClearAll()
    return


def GameLoop():
    """
    The Main game loops, handles inputs and passes them on to the necessary calculations
    """
    GenerateGrid()
    while True:
        DisplayGrid()
        print("Input location: 'x y' to sweep OR 'x y f' to flag")
        try:
            IN = GetXY()
            IN[0], IN[1] = int(IN[0]), int(IN[1])
            if firstClick:
                GenerateMines((IN[0], IN[1]))
            if len(IN) >= 3 and IN[2] == 'f':
                # I don't actually care if the user submits more than 3 values
                # I might change it to be stricter in the future
                Flag(IN[0], IN[1])
            else:
                CalculateHit(IN[0], IN[1])
        except:
            print("Please input data in the correct format.")
        if IN == []: #DEBUG
            break
    DisplayGrid() # Thinking that I should maybe display grid before the warning texts


def GenerateMines(firstClickXY):
    """
    Generate the mines accoring to `size`^2 and `minesCount`
    Stored as an array of tuples in `mines`
    Occurs upon user picking a spot
    """
    global firstClick
    global mines

    # Generate a list of numbers from 0 up to the grid size
    generationRange = list(range(0, size**2-1))

    # Convert the value of the first click into an integer value within the mines generation range
    firstClickXY = firstClickXY[0] + firstClickXY[1] * size

    # Then remove it from the genration range, to prevent first click error
    generationRange.remove(firstClickXY)

    # Generate a random sample of values 
    # Based on the mines amount that the player dictated at the beginning of the game
    rand = random.sample(generationRange, minesCount)

    # For each value generated, split it into x and y values and store it in `mines` global array
    # x: Which column, gotten through remainder of size / value
    # y: Which row, how many times does size divide into value 
    mines = list(map(lambda value: value%size, math.floor(value/size), rand))

    print(mines) #DEBUG
    firstClick = False


def GenerateGrid():
    """
    Generate a matrix of "o" with size `size`
    """
    global grid
    grid = [["o" for i in range(size)] for j in range(size)]


def Flag(x, y):
    """
    Flags a location so that it can't be hit be mines
    Use it again on the same location to unflag it
    """
    global flags
    global grid
    if (x, y) in flags:
        flags.remove((x, y))
        grid[x][y] = "o"
    elif grid[x][y] == "o":
        flags.append((x, y))
        grid[x][y] = "f"


def CalculateHit(x, y):
    """
    Check if the position is a mine or flagged, if not, calculate what to reveal
    """
    global grid
    if (x, y) in flags:
        print("That position is flagged, you must unflag it first!")
    elif (x, y) in mines:
        Die(x, y)
    else:
        GetSurroundingMines(x, y)


def GetSurroundingMines(x, y):
    """
    Get how many mines are surrounding the current position
    If this is completely clear then recursively get the numbers for the surrounding mines
    """
    surroundingMines = 0
    sx, sy = max(x-1, 0),       max(y-1, 0)     # Start X,  Start Y
    ex, ey = min(x+2, size),    min(y+2, size)  # End X,    End Y

    # Check if any surrounding tile is a mine
    for i in range(sx, ex):
        for j in range(sy, ey):
            surroundingMines += (i, j) in mines 

    # If there's 0 mines in the surrounding tiles, then use "." instead
    grid[x][y] = surroundingMines or "."

    # If every tile surrounding it is empty, then automatically open them up as well
    if surroundingMines == 0:
        for i in range(sx, ex):
            for j in range(sy, ey):
                # Only do it if they haven't been opened up alreadys
                if grid[i][j] == "o":
                    GetSurroundingMines(i, j)


def Die(x, y):
    """
    When the player hits a mine, the game ends
    """
    global grid
    for mine in mines:
        if mine in flags:
            grid[mine[0]][mine[1]] = "F" # Flagged Mine
        else:
            grid[mine[0]][mine[2]] = "M" # Unflagged Mine
    
    grid[x][y] = "X" # Death Hit
    print("X is the hit, M is unflagged mine, F is flagged mine")
    print("DEBUG: You hit a mine!") #DEBUG
    return


def Win():
    """
    When the player sucessfully reveals all the tiles without mines, they win
    """
    print("DEBUG: YOU WIN!") #DEBUG
    return


def DisplayGrid():
    """
    Displays the current gamestate, with numbers on the side to help keep track
    """
    gridDisplay = ""

    # The amount of digit of the largest number + 1 for padding
    padding = len(str(size))+1 

    for i in range(size+1):
        for j in range(size+1):
            if i == 0:
                a = " " if j == 0 else j
            elif j == 0:
                a = i
            else:
                a = grid[i-1][j-1]
            # a is what to display
            # and then after displaying a, pad it until it's the right with (using padding)
            gridDisplay += "{0:<{padding}}".format(a, padding=padding)
        gridDisplay += "\n"
    print(gridDisplay)


def ClearAll():
    """
    Clear all global variables
    """
    global grid, mines, flags, minesCount, size
    grid = mines, flags = []
    minesCount = size = 0


def GetXY():
    """
    Gets the input and splits them into array
    """
    IN = input()
    IN = IN.split() # Splits by all whitespace chunks
    return IN



while True:
    print("Input the size of the map and the amount of mines: 'size mines'")
    IN = GetXY()
    size = int(IN[0])
    minesCount = int(IN[1])

    GameLoop()
    
    print("Do you want to restart? y/n")
    IN = input()
    if IN.lower() != "y":
        break
