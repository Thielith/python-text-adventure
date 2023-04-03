import os, getch

border:list[str]

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
