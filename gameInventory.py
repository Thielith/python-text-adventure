import gameItem

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
