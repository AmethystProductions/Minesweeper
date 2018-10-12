import random
import math
grid = []
mines = []
minesCount = 0
flags = []
size = 0

def Init():
    ClearAll()
    return

def GameLoop():
    """
    The Main game loops, handles inputs and passes them on to the necessary calculations
    """
    GenerateMines()
    GenerateGrid()
    while True:
        DisplayGrid()
        print("Input location: 'x y' to sweep OR 'x y f' to flag")
        try:
            IN = GetXY()
            if len(IN) >= 3 and IN[3] == 'f':
                Flag(int(IN[0]), int(IN[1]))
            else:
                CalculateHit(int(IN[0]), int(IN[1]))
        except:
            print("Please input data in the correct format.")
    DisplayGrid()

def GenerateMines():
    """
    Generate the mines accoring to `size`^2 and `minesCount`
    Stored as an array of tuples in `mines`
    """
    rand = random.sample(range(0, size**2-1), minesCount)
    for i in rand:
        x = math.floor(i / size)
        y = i % size
        mines.append((x,y))
    print(mines)

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
    if (x, y) in flags:
        flags.remove(x, y)
    else:
        flags.append(x, y)


def CalculateHit(x, y):
    if (x, y) in flags:
        print("That position is flagged, you must unflag it first!")
    elif (x,y) in mines:
        Die()
    else:
        # Calcucate proximity to mines here
        print("")

def Die():
    return


def DisplayGrid():
    gridDisplay = ""
    padding = len(str(size))+1
    for i in range(size+1):
        for j in range(size+1):
            if i == 0:
                a = " " if j == 0 else j
            elif j == 0:
                a = i
            else:
                a = grid[i-1][j-1]
            gridDisplay += "{0:<{padding}}".format(a, padding=padding)
        gridDisplay += "\n"
    print(gridDisplay)

def ClearAll():
    grid = []
    mines = []
    hit = []
    return

def GetXY():
    IN = input()
    IN = list(map(lambda x: x.strip(), IN.split(" ")))
    return IN


while True:
    print("size mines")
    IN = GetXY()
    size = int(IN[0])
    minesCount = int(IN[1])

    GameLoop()
    
    print("Do you want to restart? y/n")
    IN = input()
    if IN.lower() != "y":
        break
