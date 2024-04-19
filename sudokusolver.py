# Running PyGame version: 2.1.2

import pygame

pygame.init()

"""
SETUP __________________________________________________________________________
"""
# TICKRATE is updates/second
TICKRATE = 60


"""
COLORS _________________________________________________________________________
"""
# each 3x3 box in the 9x9 grid will have its own color for distinction,
# C1 through C9.
# possibilities: x <= 2, x <= 5, x <= 8, y <= 2, y <= 5, y <= 8. Any
# combination of x and y yields a specific color.
C1 = (255, 200, 200)
C2 = (200, 255, 200)
C3 = (200, 200, 255)
C4 = (255, 255, 200)
C5 = (200, 255, 255)
C6 = (255, 200, 255)
C7 = (255, 200, 150)
C8 = (150, 255, 200)
C9 = (200, 150, 255)
BACKGROUND = (0, 0, 0)
COLOR_LIST = [
    [C1, C2, C3],   # [0][0-2]
    [C4, C5, C6],   # [1][0-2]
    [C7, C8, C9]    # [2][0-2]
]

def subgrid_color_picker(y, x):
    subgrid_y = y // 3      # go from 0-8 to 0-2 (whole grid to sub grid)
    subgrid_x = x // 3      # go from 0-8 to 0-2 (whole grid to sub grid)
    return COLOR_LIST[subgrid_y][subgrid_x]


"""
FONT ___________________________________________________________________________
"""
font = pygame.font.SysFont('microsoftsansserifttf', 40)


"""
GRID ___________________________________________________________________________
"""
BLOCK_SIZE = 60             # size of length of each block in pixels
BLOCK_MARGINS = 1           # size of width of margins in pixels
BLOCKS_PER_SIDE = 9         # number of blocks per side


# Insert grid below
grid = [
    [8, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 3, 6, 0, 0, 0, 0, 0],
    [0, 7, 0, 0, 9, 0, 2, 0, 0],
    [0, 5, 0, 0, 0, 7, 0, 0, 0],
    [0, 0, 0, 0, 4, 5, 7, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 3, 0],
    [0, 0, 1, 0, 0, 0, 0, 6, 8],
    [0, 0, 8, 5, 0, 0, 0, 1, 0],
    [0, 9, 0, 0, 0, 0, 4, 0, 0]
]
"""
COMPLETED GRID FROM ABOVE:
[8, 1, 2, 7, 5, 3, 6, 4, 9],
[9, 4, 3, 6, 8, 2, 1, 7, 5],
[6, 7, 5, 4, 9, 1, 2, 8, 3],
[1, 5, 4, 2, 3, 7, 8, 9, 6],
[3, 6, 9, 8, 4, 5, 7, 2, 1],
[2, 8, 7, 1, 6, 9, 5, 3, 4],
[5, 2, 1, 9, 7, 4, 3, 6, 8],
[4, 3, 8, 5, 2, 6, 9, 1, 7],
[7, 9, 6, 3, 1, 8, 4, 5, 2]
"""


"""
PRE-LOOP _______________________________________________________________________
"""
GAME_WINDOW_SIZE = (BLOCK_SIZE + BLOCK_MARGINS) * BLOCKS_PER_SIDE +\
    BLOCK_MARGINS
GAME_WINDOW = pygame.display.set_mode((GAME_WINDOW_SIZE, GAME_WINDOW_SIZE))
CLOCK = pygame.time.Clock()
GAME_WINDOW.fill(BACKGROUND)
pygame.display.set_caption("Sudoku Solver Visualizer")

seconds_to_termination = 20
iterations = 0
running = True
run = True


"""
LOGIC __________________________________________________________________________
"""
# If any position's value is not in 0-9, it is defaulted to 0
for y in range(BLOCKS_PER_SIDE):
    for x in range(BLOCKS_PER_SIDE):
        if grid[y][x] < 0 or grid[y][x] > 9:
            grid[y][x] = 0

def printGrid():
    print()
    for row in range(BLOCKS_PER_SIDE):
        print(grid[row])
    print()

# print the initial grid to terminal
printGrid()

# s is the string to print, b is the boolean that signifies success or not. If
    # successful, call printGrid().
def printMessage(s, b):
    global run
    if b:
        printGrid()
    print(s + "\n")
    pygame.display.set_caption(s)
    drawBoard()
    run = False

# check if it's possible to insert n in g[y][x] following the rules:
    # 1. no duplicates of the number n in the row
    # 2. no duplicates of the number n in the column
    # 3. no duplicates of the number n in the subgrid that n is in
def insertable(y, x, n):
    # 1 and 2
    for sweep in range(BLOCKS_PER_SIDE):
        if grid[y][sweep] == n:
            return False
        if grid[sweep][x] == n:
            return False
    # 3
    subgrid_x = (x // 3) * 3
    subgrid_y = (y // 3) * 3
    for i in range(0, 3):
        for j in range(0, 3):
            if grid[subgrid_y + i][subgrid_x + j] == n:
                return False
    # if insertable (all conditions pass), return True
    return True


def drawBoard():
    for y in range(BLOCKS_PER_SIDE):
        for x in range(BLOCKS_PER_SIDE):
            pygame.draw.rect(GAME_WINDOW, subgrid_color_picker(y, x),
                [
                    (BLOCK_SIZE + BLOCK_MARGINS) * x + BLOCK_MARGINS,
                    (BLOCK_SIZE + BLOCK_MARGINS) * y + BLOCK_MARGINS,
                    BLOCK_SIZE,
                    BLOCK_SIZE
                ])
            if grid[y][x] != 0:
                text = font.render(str(grid[y][x]), 1, (0, 0, 0))
                GAME_WINDOW.blit(text,
                    (
                        # the "+ 15" and "+ 10" places the numbers in the center
                        # of their respective grids
                        (BLOCK_SIZE + BLOCK_MARGINS) * \
                            x + BLOCK_MARGINS + 20,
                        (BLOCK_SIZE + BLOCK_MARGINS) * \
                            y + BLOCK_MARGINS + 20
                    )
                )
    # Tick frames/sec and flip (inside drawBoard())
    CLOCK.tick(TICKRATE)
    pygame.display.flip()

# draw the board initially
drawBoard()

# return True at the first instance of a 0 being found, False if no 0s exist.
def zeros_exist():
    for y in range(BLOCKS_PER_SIDE):
        for x in range(BLOCKS_PER_SIDE):
            if grid[y][x] == 0:
                return True
    return False


def check_all_non0_placements_validity():
    global run
    temp = 0
    for y in range(BLOCKS_PER_SIDE):
        for x in range(BLOCKS_PER_SIDE):
            if grid[y][x] != 0:
                temp = grid[y][x]
                grid[y][x] = 0
                if insertable(y, x, temp):
                    grid[y][x] = temp
                else:
                    grid[y][x] = temp
                    printMessage("Invalid", False)
                    return False
    return True

# call only once before solve() to check for validity of all original
    # 0 placements. Return True if at least one 1-9 digit is insertable
    # at any original 0 positon. False if all 1-9 digits are taken in the
    # row, column, or subgrid.
def check_all_0_placements_validity():
    global run
    temp = 0
    insertable_fails = 0
    for y in range(BLOCKS_PER_SIDE):
        for x in range(BLOCKS_PER_SIDE):
            if grid[y][x] == 0:
                for n in range(1, BLOCKS_PER_SIDE + 1):
                    if insertable(y, x, n) == False:
                        insertable_fails += 1
                    if insertable_fails == 9:
                        printMessage(
                            f"Invalid, position (%d, %d) cannot hold any digit 1-9" % (x + 1, y + 1), False)
                        return False
            insertable_fails = 0
    return True


# run the initial checks for all initial 0 and non-0 placements
check_all_non0_placements_validity()
check_all_0_placements_validity()


def zeros_and_validity():
    global run
    if zeros_exist() == False:
        if check_all_non0_placements_validity():
            printMessage("Grid complete", True)
            return
        else:
            printMessage("Invalid", False)
            return
    else:
        if check_all_non0_placements_validity() == False:
            printMessage("Invalid", False)
            return


def solve():
    global run
    global iterations

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                return

        iterations += 1
        # higher iterations value speeds up solve time by updating the board
            # after every x changes in % x instead of every change.
            # Recommend 10 to 50.
        if iterations % 50 == 0:
            drawBoard()

        for y in range(BLOCKS_PER_SIDE):
            for x in range(BLOCKS_PER_SIDE):
                if grid[y][x] == 0:
                    for n in range(1, BLOCKS_PER_SIDE + 1):
                        if insertable(y, x, n):
                            grid[y][x] = n
                            # if no more zeros, print "Invalid", set run to
                            # False, and return out of the loop, ending
                            # solve() and moving on to TICKRATE = 1
                            zeros_and_validity()
                            if zeros_exist() == False:
                                return
                            solve()
                            grid[y][x] = 0
                    return


"""
LOOP ___________________________________________________________________________
"""
while running:

    """
    EXIT USING 'X' BUTTON ______________________________________________________
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    solve()

    TICKRATE = 1

    print(f"%d seconds until termination" % seconds_to_termination)
    if seconds_to_termination == 0:
        running = False
    seconds_to_termination -= 1

    """
    TICK FRAMES/SEC AND FLIP ___________________________________________________
    """
    CLOCK.tick(TICKRATE)
    pygame.display.flip()


pygame.quit()
