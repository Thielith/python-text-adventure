import time
import utils, controls, gameItem, gameMap, gameInventory

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
    print(input)
    print(controls.mapMoveDown)

    if input == 'q':
        global stopGame
        stopGame = True
        return

    if input == 'g':
        currMap.data[playerPos[1]][playerPos[0]] = 'o'

    # map movement
    mapMoveInputs = [controls.mapMoveUp, controls.mapMoveLeft, controls.mapMoveDown, controls.mapMoveRight]
    for key in mapMoveInputs:
        if input == key:
            navigate(key)
    # map inventory
    if input == controls.mapEnterInventory:
        playerInventory.view()

# navigation for moving around map
def navigate(input):
    inputToNum = {controls.mapMoveUp: 0, controls.mapMoveLeft: 1, controls.mapMoveDown: 2, controls.mapMoveRight: 3}
    direction = inputToNum[input]
    gameMap.move_map(currMap, direction, playerPos)

def setConfig():
    utils.border = border;
    gameInventory.ctrlUse = controls.inventoryUse
    gameInventory.ctrlUp = controls.inventoryUp
    gameInventory.ctrlDown = controls.inventoryDown
    gameInventory.ctrlExit = controls.inventoryExit
    gameInventory.cursorChar = inventoryCursor
    gameInventory.info = inventoryInputInfo
    gameInventory.windowLength = viewportWidth*2+1
    gameInventory.seperator = inventorySeperator
    gameInventory.ctrlScrollDesc = controls.inventoryScrollDesc

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    utils.clearScreen()
    main()
