import sys

global mapMoveUp
global mapMoveDown
global mapMoveLeft
global mapMoveRight
global mapEnterInventory
global inventoryUp
global inventoryDown
global inventoryUse
global inventoryExit
global inventoryScrollDesc

if 'linux' in sys.platform:
    mapMoveUp = '\x1b[A'    # arrow up
    mapMoveDown = '\x1b[B'  # arrow down
    mapMoveLeft = '\x1b[D'  # arrow left
    mapMoveRight = '\x1b[C' # arrow right
    mapEnterInventory = 'i'
    inventoryUp = '\x1b[A'    # arrow up
    inventoryDown = '\x1b[B'  # arrow down
    inventoryUse = ' '
    inventoryExit = 'e'
    inventoryScrollDesc = 'l'
elif 'win32' in sys.platform:
    mapMoveUp = 'w'    # arrow up
    mapMoveDown = 's'  # arrow down
    mapMoveLeft = 'a'  # arrow left
    mapMoveRight = 'd' # arrow right
    mapEnterInventory = 'i'
    inventoryUp = 'w'    # arrow up
    inventoryDown = 's'  # arrow down
    inventoryUse = ' '
    inventoryExit = 'e'
    inventoryScrollDesc = 'l'
