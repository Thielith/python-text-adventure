import time
import utils, gameItem, gameMap, gameInventory

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
mapInputInfo:str = "Movement (Arrows) | Inventory (I) | Exit (Q)\n"
inventoryInputInfo:str = "Navigate (Arrows) | Scroll Description (L) | Exit (E)\n"

# save file stuff. not in a file cause i'm not doing that yet
playerChar:str = 'P'
border:list[str] = ['═', '║', '╔', '╗', '╚', '╝']
doubleView:bool = False
viewportWidth:int = 40
viewportHeight:int = 10
mapPaddingChar = ' '
inventoryCursor = '+'
inventorySeperator = " | "

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
ctrlInventoryScrollDesc = 'l'

playerPos:list[int] = [1, 1]
playerInventory:gameInventory.Inventory = gameInventory.Inventory(10, [5, 6])

stopGame:bool = False
currMap:gameMap.Map = gameMap.Map()

# initialization
def main():
    setConfig()

    global currMap
    w:int = 50
    h:int = 50
    p:int = 0
    currMap.width = w + 2*p
    currMap.height = h + 2*p
    currMap.data = gameMap.generate_map(w, h, p, mapPaddingChar)

    currMap.data[0][0] = 'x'
    currMap.data[0][1] = 'y'
    currMap.data[w-1][h-1] = 'x'

    while not stopGame:
        gameMap.viewMap(currMap, playerPos, viewportWidth, viewportHeight, playerChar, mapPaddingChar)
        print(mapInputInfo)
        handleInput()
        utils.clearScreen()

# input
def handleInput():
    input = utils.getInput()

    if input == 'q':
        global stopGame
        stopGame = True
        return

    if input == 'g':
        currMap.data[playerPos[1]][playerPos[0]] = 'o'

    # map movement
    mapMoveInputs = [ctrlMapMoveUp, ctrlMapMoveLeft, ctrlMapMoveDown, ctrlMapMoveRight]
    for key in mapMoveInputs:
        if input == key:
            navigate(key)
    # map inventory
    if input == ctrlMapEnterInventory:
        playerInventory.view()

# navigation for moving around map
def navigate(input):
    inputToNum = {ctrlMapMoveUp: 0, ctrlMapMoveLeft: 1, ctrlMapMoveDown: 2, ctrlMapMoveRight: 3}
    direction = inputToNum[input]
    gameMap.move_map(currMap, direction, playerPos)

def setConfig():
    utils.border = border;
    gameInventory.ctrlUse = ctrlInventoryUse
    gameInventory.ctrlUp = ctrlInventoryUp
    gameInventory.ctrlDown = ctrlInventoryDown
    gameInventory.ctrlExit = ctrlInventoryExit
    gameInventory.cursorChar = inventoryCursor
    gameInventory.info = inventoryInputInfo
    gameInventory.windowLength = viewportWidth*2+1
    gameInventory.seperator = inventorySeperator
    gameInventory.ctrlScrollDesc = ctrlInventoryScrollDesc

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    utils.clearScreen()
    main()
