import utils

solids:list[str] = [' ', 'T', 'R', '#']

class Map():
    def __init__(self):
        self.data:list[list[str]]
        self.width:int
        self.height:int
        self.padding:int

# movement input for map
def move_map(currMap:Map, direction:int, playerPos:list[int]):
    # no switch case =(
    oldX:int = playerPos[0]
    oldY:int = playerPos[1]

    # move player
    if direction == 0:    # up
        playerPos[1] -= 1
    elif direction == 1:  # left
        playerPos[0] -= 1
    elif direction == 2:  # down
        playerPos[1] += 1
    elif direction == 3:  # right
        playerPos[0] += 1

    # move player within the bounds of the map if needed
    playerPos[0] = max(min(playerPos[0], currMap.width-1), 0)
    playerPos[1] = max(min(playerPos[1], currMap.height-1), 0)

    # check if player is on a solid.  if so, move them back
    if currMap.data[playerPos[1]][playerPos[0]] in solids:
        playerPos[0] = oldX
        playerPos[1] = oldY

# generate map
def generate_map(width:int, height:int, padding:int = 0, paddingChar = ' ') -> list[list[str]]:
    rows = []

    # actual area
    for row in range(0, height):
        cols:list[str] = []

        for col in range(0, width):
            cols.append('░')
        rows.append(cols)

    # padding
    if not padding == 0:
        # middle
        for row in range(0, height):
            for pad in range(0, padding):
                rows[row].insert(0, paddingChar)
                rows[row].append(paddingChar)
        # top and bottom
        for pad in range(0, padding):
            padRow:list[str] = []
            for col in range(0, padding*2 + width):
                padRow.append(paddingChar)
            rows.insert(0, padRow)
            rows.append(padRow.copy())

    return rows

# view area around you
def viewMap(currMap:Map, coords:list[int], viewW:int, viewH:int, centerChar:str = 'H', paddingChar:str = ' '):
    view:list[list[str]] = []
    fullViewW = viewW*2+1
    fullViewH = viewH*2+1
    paddingX = int((fullViewW - currMap.width)/2)+1
    paddingY = int((fullViewH - currMap.height)/2)+1

    # makes sure it doesnt read data OOBs
    tlCornerX = min(max(0, coords[0] - viewW), currMap.width-fullViewW)
    tlCornerY = min(max(0, coords[1] - viewH), currMap.height-fullViewH)
    playerOffsetX = min(0, coords[0] - viewW)
    playerOffsetY = min(0, coords[1] - viewH)

    # generates what we can see with the viewport
    rangeX = min(fullViewW, currMap.width)
    rangeY = min(fullViewH, currMap.height)

    for row in range(0, rangeY):
        cols:list[str] = []
        for col in range(0, rangeX):
            cursorX = max(col, tlCornerX + col)
            cursorY = max(row, tlCornerY + row)

            if cursorX == coords[0] and cursorY == coords[1]:
                cols.append(centerChar)
                continue

            cols.append(currMap.data[cursorY][cursorX])
        view.append(cols)

    # if viewport is bigger than map, then center map and apply padding
    if fullViewW > currMap.width:
        for row in view:
            for pad in range(0, paddingX):
                row.insert(0, paddingChar)
                row.append(paddingChar)
    if fullViewH > currMap.height:
        for pad in range(0, paddingY):
            padRow:list[str] = []
            for cols in range(0, fullViewW):
                padRow.append(paddingChar)
            view.insert(0, padRow)
            view.append(padRow.copy())

    utils.generateBorder(view, fullViewW, fullViewH)
