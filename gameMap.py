solids:list[str] = [' ', 'T', 'R', '#']

class Map():
    def __init__(self):
        self.data:list[list[str]]
        self.width:int
        self.height:int
        self.padding:int
