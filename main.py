import time, os, getch
import gameItem, gameMap, gameInventory

# navigation area                    | done
#   travel                           | done
# inventory                          | doneish
# combat                             |
#   enemy movement                   |
#   encounter checking               |
# subareas                           |
# random terrain feature generation  |
# dungeon generation                 |

# game data
mapInputInfo:str = "Movement (Arrows) | Inventory (I)\n"
inventoryInputInfo:str = "Navigate (Arrows)\n"

# save file stuff. not in a file cause i'm not doing that yet
playerChar:str = 'P'
border:list[str] = ['═', '║', '╔', '╗', '╚', '╝']
doubleView:bool = False
viewportWidth:int = 40
viewportHeight:int = 10
mapPaddingChar = ' '

### controls
ctrlMapMoveUp = '\x1b[A'    # arrow up
ctrlMapMoveDown = '\x1b[B'  # arrow down
ctrlMapMoveLeft = '\x1b[D'  # arrow left
ctrlMapMoveRight = '\x1b[C' # arrow right
ctrlMapEnterInventory = 'i'
ctrlInventoryUp = '\x1b[A'    # arrow up
ctrlInventoryDown = '\x1b[B'  # arrow down
ctrlInventoryUse = ' '
ctrlInventoryExit = 'e'

playerX:int = 1
playerY:int = 1
playerInventory:gameInventory.Inventory = gameInventory.Inventory(10, [0, 1, 2, 3, 4, 5])

stopGame:bool = False
currMap:gameMap.Map = gameMap.Map()

# basic functions for basic things
def clearScreen():
    os.system("clear")  # cross-platoform support:  clear --> [windows] cls
def getInput() -> str:
    char = getch.getch()
    if char == '\x1b':
        return (char + getch.getch() + getch.getch())
    return char
def generateBorder(fill:list, fillWidth:int, fillHeight:int):
    #top
    print(border[2], end='')
    for row in range(0, fillWidth):
        print(border[0], end='')
    print(border[3])

    #middle
    for row in range(0, fillHeight):
        print(border[1], end='')
        for col in range(0, fillWidth):
            print(fill[row][col], end='')
        print(border[1])

    #bottom
    print(border[4], end='')
    for row in range(0, fillWidth):
        print(border[0], end='')
    print(border[5])

# initialization
def main():
    global currMap
    w:int = 50
    h:int = 50
    p:int = 0
    currMap.width = w + 2*p
    currMap.height = h + 2*p
    currMap.data = generate_map(w, h, p)

    currMap.data[0][0] = 'x'
    currMap.data[0][1] = 'y'
    currMap.data[w-1][h-1] = 'x'

    while not stopGame:
        viewMap(playerX, playerY)
        print(mapInputInfo)
        handleInput()
        clearScreen()

# input
def handleInput():
    input = getInput()

    if input == 'q':
        global stopGame
        stopGame = True
        return

    if input == 'g':
        currMap.data[playerY][playerX] = 'o'

    # map movement
    mapMoveInputs = [ctrlMapMoveUp, ctrlMapMoveLeft, ctrlMapMoveDown, ctrlMapMoveRight]
    for key in mapMoveInputs:
        if input == key:
            navigate(key)
    # map inventory
    if input == ctrlMapEnterInventory:
        inventory()

# inventory menu
def generateInventoryWindow(selectedIndex:int):
    cursorChar = '+'

    # get length of item with longest name
    longestItemNameLength:int = 0
    for item in playerInventory.items:
        itemName = gameItem.itemDict[item].name
        if len(itemName) > longestItemNameLength:
            longestItemNameLength = len(itemName)

    # generate inventory window
    invView:List[str] = []

    index:int = 0
    for item in playerInventory.items:
        # list bullet
        entry = " "
        if index == selectedIndex: entry += cursorChar
        else: entry += '-'
        entry += " " + gameItem.itemDict[item].name

        if len(entry) < longestItemNameLength:
            for i in range(0, longestItemNameLength):
                entry += ' '
        entry += " | "
        invView.append(entry)
        index += 1

    generateBorder(invView, longestItemNameLength+4, len(invView))
def inventory():
    input = ''
    index:int = 0
    while not input == ctrlInventoryExit:
        clearScreen()
        viewMap(playerX, playerY)
        generateInventoryWindow(index)

        print(inventoryInputInfo)
        input = getInput()

        # navigation
        if input == ctrlInventoryUp: index -= 1
        elif input == ctrlInventoryDown: index += 1
        ### OOB checking
        if index < 0:
            index = 0
        elif index > len(playerInventory.items)-1:
            index = len(playerInventory.items)-1

        # item use
        if input == ctrlInventoryUse and not len(playerInventory.items) == 0:
            playerInventory.useItem(playerInventory.items[index])

# navigation for moving around map
def navigate(input):
    inputToNum = {ctrlMapMoveUp: 0, ctrlMapMoveLeft: 1, ctrlMapMoveDown: 2, ctrlMapMoveRight: 3}
    direction = inputToNum[input]
    move_map(direction)

# movement input for map
def move_map(direction:int):
    # no switch case =(
    global playerX, playerY
    oldX:int = playerX
    oldY:int = playerY

    # move player
    if direction == 0:    # up
        playerY -= 1
    elif direction == 1:  # left
        playerX -= 1
    elif direction == 2:  # down
        playerY += 1
    elif direction == 3:  # right
        playerX += 1

    # move player within the bounds of the map if needed
    playerX = max(min(playerX, currMap.width-1), 0)
    playerY = max(min(playerY, currMap.height-1), 0)

    # check if player is on a solid.  if so, move them back
    if currMap.data[playerY][playerX] in gameMap.solids:
        playerX = oldX
        playerY = oldY

# generate map
def generate_map(width:int, height:int, padding:int = 0) -> list[list[str]]:
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
                rows[row].insert(0, mapPaddingChar)
                rows[row].append(mapPaddingChar)
        # top and bottom
        for pad in range(0, padding):
            padRow:list[str] = []
            for col in range(0, padding*2 + width):
                padRow.append(mapPaddingChar)
            rows.insert(0, padRow)
            rows.append(padRow.copy())

    return rows

# view area around you
def viewMap(x:int, y:int, viewW:int = viewportWidth, viewH:int = viewportHeight):
    view:list[list[str]] = []
    fullViewW = viewW*2+1
    fullViewH = viewH*2+1
    paddingX = int((fullViewW - currMap.width)/2)+1
    paddingY = int((fullViewH - currMap.height)/2)+1

    # makes sure it doesnt read data OOBs
    tlCornerX = min(max(0, x - viewW), currMap.width-fullViewW)
    tlCornerY = min(max(0, y - viewH), currMap.height-fullViewH)
    playerOffsetX = min(0, x - viewW)
    playerOffsetY = min(0, y - viewH)

    # generates what we can see with the viewport
    rangeX = min(fullViewW, currMap.width)
    rangeY = min(fullViewH, currMap.height)

    for row in range(0, rangeY):
        cols:list[str] = []
        for col in range(0, rangeX):
            cursorX = max(col, tlCornerX + col)
            cursorY = max(row, tlCornerY + row)

            if cursorX == x and cursorY == y:
                cols.append(playerChar)
                continue

            cols.append(currMap.data[cursorY][cursorX])
        view.append(cols)

    # if viewport is bigger than map, then center map and apply padding
    if fullViewW > currMap.width:
        for row in view:
            for pad in range(0, paddingX):
                row.insert(0, mapPaddingChar)
                row.append(mapPaddingChar)
    if fullViewH > currMap.height:
        for pad in range(0, paddingY):
            padRow:list[str] = []
            for cols in range(0, fullViewW):
                padRow.append(mapPaddingChar)
            view.insert(0, padRow)
            view.append(padRow.copy())

    generateBorder(view, fullViewW, fullViewH)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    clearScreen()
    main()
