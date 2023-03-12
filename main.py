from pynput import keyboard
import time, os

# navigation area                    | done
#   travel                           | done
# inventory                          |
# combat                             |
#   enemy movement                   |
#   encounter checking               |
# subareas                           |
# random terrain feature generation  |
# dungeon generation                 |

# library stuff. move to another file eventually
itemTypeDict:dict = {
    0: "consumable",
    1: "armor",
    2: "weapon",
    3: "keyItem",
    4: "test"
}
weaponTypeDict:dict = {
    0: "all",
    1: "melee",
    2: "ranged",
    3: "magic"
}
elementTypeDic:dict = {
    0: "basic",
    1: "hot",
    2: "cold",
    3: "rock",
    4: "tool",
    5: "order",
    6: "chaos"
}

class Item:  # don't use. use the other ones.
    def __init__(self, name:str, ELEM:int, quality:int, desc:str):
        self.type:int = -1
        self.name:str = name
        self.ELEM:int = ELEM
        self.quality:int = quality
        self.desc:str = desc
class Consumable(Item):
    def __init__(self, name:str = "Eatable?", HP:int = 0, STAM:int = 0,
                 desc:str = "Oops! No description.", ELEM:int = 0, quality:int = 0):
        super().__init__(name, ELEM, quality, desc)
        self.type:int = 0
        self.restoreHP:int = HP
        self.restoreSTAM:int = STAM
class Armor(Item):
    def __init__(self, name:str = "Wearable?", DEF:int = 0, DEF_ELEM:int = 0,
                 desc:str = "Oops! No description.", ELEM:int = 0, quality:int = 0):
        super().__init__(name, ELEM, quality, desc)
        self.type:int = 1
        self.DEF:int = DEF
        self.DEF_ELEM:int = DEF_ELEM
class Weapon(Item):
    def __init__(self, name:str = "Hurtable?", ATK:int = 1, ATK_ELEM:int = 0, classType:int = 0,
                 desc:str = "Oops! No description.", ELEM:int = 0, quality:int = 0):
        super().__init__(name, ELEM, quality, desc)
        self.type:int = 2
        self.ATK:int = ATK
class KeyItem(Item):
    def __init__(self, name:str = "Arbitrary.", questID:int = -1,
                 desc:str = "Oops! No description.", ELEM:int = 0, quality:int = 0):
        super().__init__(name, ELEM, quality, desc)
        self.type:int = 3
        self.questID:int = questID

class Map():
    def __init__(self):
        self.data:list[list[str]]
        self.width:int
        self.height:int
        print("Its a map.")

# game data
mapInputInfo:str = "Movement (WASD) | Inventory (I)\n"
solids:list[str] = ['T', 'R', '#']
itemDict = {
    0: Consumable("Apple", 5, 0, "It's an apple."),
    1: Consumable("Apple1", 5, 0, "It's also an apple."),
    2: Armor("Shirt", 1, 0, "Shirt-ly"),
    3: Weapon("Sharp Apple", 5, 0, 1, "It's an apple?"),
    4: Consumable("Apple4", 5, 0, "Where'd the other two go?"),
    5: Consumable("Apple5", 5, 0, "Replaced.")
}

# save file stuff. not in a file cause i'm not doing that yet
playerChar:str = 'P'
border:list[str] = ['═', '║', '╔', '╗', '╚', '╝']
doubleView:bool = False

playerX:int = 3
playerY:int = 3
playerInventory:list[int] = [0, 1, 2, 3, 4, 5]

viewportWidth = 20
viewportHeight = 5

stopGame:bool = False
curMap:Map = Map()
inputDelay:float = 0.1

def main():
    global curMap
    w:int = 50
    h:int = 50
    curMap.width = w
    curMap.height = h
    curMap.data = generate_map(w, h)

    #gameMap[39][39] = 'x'
    #gameMap[49][49] = '#'

    """
    for row in range(0, h):
        for col in range(0, w):
            print(map[row][col], end='')
        print()
    """
    while not stopGame:
        viewMap(playerX, playerY)
        print(mapInputInfo)
        time.sleep(inputDelay)
        handleInput()
        os.system("clear")  # cross-platoform support:  clear --> [windows] cls


def handleInput():
    with keyboard.Events() as events:
        # Block for as much as possible
        event = events.get(1e6)
        if event.key == keyboard.KeyCode.from_char('q'):
            global stopGame
            stopGame = True
            return

        movementInputs = ['w', 'a', 's', 'd']

        # map movement
        for key in movementInputs:
            if event.key == keyboard.KeyCode.from_char(key):
                navigate(key)

    """
    choice = input(mapInputInfo).lower()
    while choice != 'q':
        if choice in ['w', 'a', 's', 'd']:
            navigate(choice, gameMap)

        elif choice == 'i':
            pass

        choice = input(mapInputInfo).lower()
    """

# inventory menu
def inventory():
    pass

# navigation for moving around map
def navigate(input:str):
    inputToNum = {'w': 0, 'a': 1, 's': 2, 'd': 3}
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
    playerX = max(min(playerX, curMap.width-1), 0)
    playerY = max(min(playerY, curMap.height-1), 0)

    # check if player is on a solid.  if so, move them back
    if curMap.data[playerY][playerX] in solids:
        playerX = oldX
        playerY = oldY

# generate map
def generate_map(width:int, height:int) -> list[list[str]]:
    rows = []

    for i in range(0, height):
        cols:list[str] = []
        for j in range(0, width):
            cols.append('░')
        rows.append(cols)

    return rows

# view area around you
# x and y are the player's coordinates
def viewMap(x:int, y:int, viewX:int = viewportWidth, viewY:int = viewportHeight):
    fillW:int = curMap.width - 1
    fillH:int = curMap.height - 1
    # making sure it doesnt try to load O.o.B data
    tlCorY:int = y - viewY
    tlCorX:int = x - viewX
    brCorY:int = y + viewY
    brCorX:int = x + viewX
    # offsetting player icon if in corners of map
    pViewOffX:int = 0
    pViewOffY:int = 0

    if tlCorY < 0:
        pViewOffY = tlCorY
        tlCorY = 0
        brCorY = viewY*2
    if tlCorX < 0:
        pViewOffX = tlCorX
        tlCorX = 0
        brCorX = viewX*2
    if brCorY > fillH:
        pViewOffY = brCorY - fillH
        brCorY = fillH
        tlCorY = fillH - viewY*2
    if brCorX > fillW:
        pViewOffX = brCorX - fillW
        brCorX = fillW
        tlCorX = fillW - viewX*2

    # store data of viewable area
    view:list[list[str]] = []

    for i in range(0, viewY*2+1):
        cols: list[str] = []
        for j in range(0, viewX*2+1):
            if i == viewY+pViewOffY and j == viewX+pViewOffX:
                cols.append(playerChar)
            else:
                cols.append(curMap.data[tlCorY + i][tlCorX + j])
        view.append(cols)

    # top
    print(border[2], end='')
    for i in range(0, viewX*2+1):
        print(border[0], end='')
        if doubleView: print(border[0], end='')
    print(border[3], end='\n')

    # middle
    for i in range(0, viewY*2+1):
        print(border[1], end='')
        for j in range(0, viewX*2+1):
            print(view[i][j], end='')
            if doubleView: print(view[i][j], end='')
        print(border[1], end='\n')

    # bottom
    print(border[4], end='')
    for i in range(0, viewX*2+1):
        print(border[0], end='')
        if doubleView: print(border[0], end='')
    print(border[5], end='\n')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
