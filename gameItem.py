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
elementTypeDict:dict = {
    0: "basic",
    1: "hot",
    2: "cold",
    3: "rock",
    4: "tool",
    5: "order",
    6: "chaos"
}


class Item:  # don't use. use the other ones.
    def __init__(self, name:str, ELEM:int, quality:int, desc:str, amount:int):
        self.type:int = -1
        self.name:str = name
        self.ELEM:int = ELEM
        self.quality:int = quality
        self.desc:str = desc
        self.amount:int = amount

class Consumable(Item):
    def __init__(self, name:str = "Eatable?", HP:int = 0, STAM:int = 0,
                 desc:str = "Oops! No description.", amount:int = 0, ELEM:int = 0, quality:int = 0):
        super().__init__(name, ELEM, quality, desc, amount)
        self.type:int = 0
        self.restoreHP:int = HP
        self.restoreSTAM:int = STAM

class Armor(Item):
    def __init__(self, name:str = "Wearable?", DEF:int = 0, DEF_ELEM:int = 0,
                 desc:str = "Oops! No description.", ELEM:int = 0, quality:int = 0):
        super().__init__(name, ELEM, quality, desc, 1)
        self.type:int = 1
        self.DEF:int = DEF
        self.DEF_ELEM:int = DEF_ELEM

class Weapon(Item):
    def __init__(self, name:str = "Hurtable?", ATK:int = 1, ATK_ELEM:int = 0,
                 classType:int = 0, desc:str = "Oops! No description.", ELEM:int = 0, quality:int = 0):
        super().__init__(name, ELEM, quality, desc, 1)
        self.type:int = 2
        self.ATK:int = ATK

class KeyItem(Item):
    def __init__(self, name:str = "Arbitrary.", questID:int = -1,
                 desc:str = "Oops! No description.", ELEM:int = 0, quality:int = 0):
        super().__init__(name, ELEM, quality, desc, 1)
        self.type:int = 3
        self.questID:int = questID


itemDict = {
    0: Consumable("Apple", 5, 0, "It's an apple.", 1),
    1: Consumable("Apple1", 5, 0, "It's also an apple.", 3),
    2: Armor("Shirt", 1, 0, "Shirt-ly"),
    3: Weapon("Sharp Apple", 5, 0, 1, "It's an apple?"),
    4: Consumable("Apple4", 5, 0, "Where'd the other two go?"),
    5: Consumable("Apple5", 5, 0, "Replaced.")
}

