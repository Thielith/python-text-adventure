import os, sys

if 'linux' in sys.platform:
    from getch import getch
elif 'win32' in sys.platform:
    from msvcrt import getwch as getch

border:list[str]

# basic functions for basic things
def clearScreen():
    if 'linux' in sys.platform:
        os.system("clear")
    elif 'win32' in sys.platform:
        os.system("cls")


def getInput() -> str:
    char = getch()
    if char == '\x1b':
        return (char + getch() + getch())
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
