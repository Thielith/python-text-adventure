# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

playerChar:str = 'P'
border:list[str] = ['═', '║', '╔', '╗', '╚', '╝']
doubleView:bool = False

playerX:int = 20
playerY:int = 20
solids:list[str] = ['T', 'R', '#']
mapInputInfo:str = "Movement (WASD) | Inventory (I)\n"

def main():
    w:int = 50
    h:int = 50
    map:list[list[str]] = generate_map(w, h)

    map[19][19] = '#'

    """
    for row in range(0, h):
        for col in range(0, w):
            print(map[row][col], end='')
        print()
    """

    viewMap(map, w, h, playerX, playerY)
    choice = input(mapInputInfo).lower()
    while choice != 'q':
        if choice in ['w', 'a', 's', 'd']:
            move_map(choice, map, w, h)
            viewMap(map, w, h, playerX, playerY)
            choice = input(mapInputInfo).lower()
        elif choice == 'i':
            pass


# main menu
def menu():
    pass

# navigation area                    | done
#   travel                           | done
# inventory                          |
# combat                             |
#   enemy movement                   |
#   encounter checking               |
# subareas                           |
# random terrarin feature generation |
# dungeon generation                 |

# See PyCharm help at https://www.jetbrains.com/help/pycharm/


# movement input for map
def move_map(input:str, map:list[list[str]], mapW:int, mapH:int):
    # no switch case =(
    global playerX, playerY
    oldX:int = playerX
    oldY:int = playerY

    # move player
    if input == 'w':
        playerY -= 1
    elif input == 'a':
        playerX -= 1
    elif input == 's':
        playerY += 1
    elif input == 'd':
        playerX += 1

    # move player within the bounds of the map if needed
    playerX = max(min(playerX, mapW), 0)
    playerY = max(min(playerY, mapH), 0)

    # check if player is on a solid.  if so, move them back
    if map[playerY][playerX] in solids:
        playerX = oldX
        playerY = oldY

# generate map
# oh you can't do pointers in python...
def generate_map(width:int, height:int) -> list[list[str]]:
    rows = []

    for i in range(0, height):
        cols:list[str] = []
        for j in range(0, width):
            cols.append('░')
        rows.append(cols)

    return rows

# view area around you
# x and y are where the player will be
def viewMap(fill:list[list[str]], fillW:int, fillH:int, x:int, y:int, viewRadius:int = 5):
    # making sure it doesnt try to load O.o.B data
    tlCorY:int = y - viewRadius
    tlCorX:int = x - viewRadius
    brCorY:int = y + viewRadius
    brCorX:int = x + viewRadius

    if tlCorY < 0:
        tlCorY = 0
        brCorY = viewRadius*2
    if tlCorX < 0:
        tlCorX = 0
        brCorX = viewRadius*2
    if brCorY > fillH:
        brCorY = fillH
        tlCorY = fillH - viewRadius*2
    if brCorX > fillW:
        brCorX = fillW
        tlCorX = fillW - viewRadius*2

    # store data of viewable area
    view:list[list[str]] = []

    for i in range(0, tlCorY):
        cols: list[str] = []
        for j in range(0, tlCorX):
            if i == viewRadius and j == viewRadius:
                cols.append(playerChar)
            else:
                cols.append(fill[tlCorY + i][tlCorX + j])
        view.append(cols)

    # top
    print(border[2], end='')
    for i in range(0, viewRadius*2+1):
        print(border[0], end='')
        if doubleView: print(border[0], end='')
    print(border[3], end='\n')

    # middle
    for i in range(0, viewRadius*2+1):
        print(border[1], end='')
        for j in range(0, viewRadius*2+1):
            print(view[i][j], end='')
            if doubleView: print(view[i][j], end='')
        print(border[1], end='\n')

    # bottom
    print(border[4], end='')
    for i in range(0, viewRadius*2+1):
        print(border[0], end='')
        if doubleView: print(border[0], end='')
    print(border[5], end='\n')

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
