class Tile:
    coords = (0, 0)
    width = 0
    height = 0
    content = None
    capacity = 0
    saturation = 0

    def __init__(self, coords, width, height, content):
        self.coords = coords
        self.width = width
        self.height = height
        self.content = content
    
    def setContent(self, content):
        self.content = content

    def identify(self,x,y):
        if self.width == 1 or self.height == 1:
            return self.coords[0] == x and self.coords[1] == y
        if self.width == 2 or self.height == 2:
            return self.coords[0] == x and self.coords[1] == y or self.coords[0] + 40 == x and self.coords[1] == y or self.coords[0] == x and self.coords[1] + 40 == y or self.coords[0] + 40 == x and self.coords[1] + 40 == y