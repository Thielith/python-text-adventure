import utils, gameItem

ctrlUse:str
ctrlUp:str
ctrlDown:str
ctrlExit:str
ctrlScrollDesc:str
cursorChar:str
info:str
windowLength:int
seperator:str
maxVisibleItemNameLength:int = 13
descriptionOffset:int = 0

class Inventory():
    def __init__(self, limit:int = 0, items:list = []):
        self.items:list[int] = items
        self.limit:int = limit

    def addItem(self, itemID:int):
        self.items.append(itemID)

    def removeItem(self, itemID:int):
        self.items.remove(itemID)

    def useItem(self, itemID:int):
        itemToUse = gameItem.itemDict[itemID]

        # Consumable
        if itemToUse.type == 0:
            pass

        # Equipable (Armor, Weapon)
        if itemToUse.type in [1, 2]:
            pass

        self.removeItem(itemID)

    def view(self):
        input:str = ''
        index:int = 0
        while not input == ctrlExit:
            global descriptionOffset
            utils.clearScreen()
            generateInventoryWindow(self, index)

            print(info)
            input = utils.getInput()

            # selecting
            if input == ctrlUp: index -= 1
            elif input == ctrlDown: index += 1
            elif input == ctrlScrollDesc: descriptionOffset += 1

            ### OOB checking
            if index < 0:
                index = 0
            elif index > len(self.items)-1:
                index = len(self.items)-1

            # item use
            if input == ctrlUse and not len(self.items) == 0:
                self.useItem(self.items[index])

# inventory menu
def generateInventoryWindow(inventory:Inventory, selectedIndex:int):
    global descriptionOffset
    selectedItem = inventory.items[selectedIndex]
    cursorChar = '+'
    seperatorLength = len(seperator)

    # get length of item with longest name
    # longestItemNameLength:int = 0
    # for item in inventory.items:
    #     itemName = gameItem.itemDict[item].name
    #     if len(itemName) > longestItemNameLength:
    #         longestItemNameLength = len(itemName)

    # split item description into chunks
    description = gameItem.itemDict[selectedItem].desc
    slicedDescription = []
    descriptionWidth = windowLength - 3 - maxVisibleItemNameLength - seperatorLength - 1
    #                  window  -   bullet    -     name        -       seperator  - right padding
    if descriptionWidth < 0:  descriptionWidth = windowLength

    descCopy = description[:]
    chunkIndex = 0
    while len(descCopy) > descriptionWidth:
        slicedDescription.append(descCopy[:descriptionWidth])
        descCopy = descCopy[descriptionWidth:]
        chunkIndex += 1
    if len(descCopy) < descriptionWidth:
        for i in range(0, descriptionWidth-len(descCopy)):
            descCopy += ' '
    slicedDescription.append(descCopy)
    if descriptionOffset > chunkIndex:  descriptionOffset = 0

    # generate inventory window
    invView:list[str] = []

    index:int = 0
    for item in inventory.items:
        itemName = gameItem.itemDict[item].name

        # list bullet
        entry = " "
        if index == selectedIndex: entry += cursorChar
        else: entry += '-'
        entry += " "

        # item name
        itemNameLength = len(itemName)
        if itemNameLength > maxVisibleItemNameLength:  itemNameLength = maxVisibleItemNameLength
        for i in range(0, itemNameLength):
            entry += itemName[i]

        # adjusting item names to fit within width
        if itemNameLength < maxVisibleItemNameLength:
            for i in range(0, maxVisibleItemNameLength - len(itemName)):
                entry += ' '
        else:
            entry = entry[:-3] + "..."
        entry += seperator

        # description
        if index + descriptionOffset <= chunkIndex:
            entry += slicedDescription[index + descriptionOffset]
        else:
            for i in range(0, descriptionWidth):
                entry += ' '
        entry += ' '

        invView.append(entry)
        index += 1

    # description cutoff
    if invView[-1][-2] != ' ':
        invView[-1] = invView[-1][:-4] + "... "

    utils.generateBorder(invView, windowLength, len(invView))
