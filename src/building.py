class Building():
    width = 1
    height = 1
    asset = ""
    def __init__(self, width, height, asset):
        self.width = width
        self.height = height
        self.asset = asset
    def getType(self):
        return self.asset.split('/')[2][:-4]

class Police(Building):
    price = 50
    def __init__(self):
        super().__init__(1, 1, "assets/pictures/policeStation.png")
class Stadium(Building):
    price = 80
    def __init__(self):
        super().__init__(1, 1, "assets/pictures/stadium.png")
class School(Building):
    price = 60
    capacity = 0
    saturation = 0
    asset = "assets/pictures/school.png"
    def __init__(self, width=1, height=1, asset="assets/pictures/school.png", capacity=0, saturation=0):
        self.capacity = capacity
        self.saturation = saturation
        super().__init__(width, height, asset)
class FireDepartment(Building):
    price = 50
    def __init__(self):
        super().__init__(1, 1, "assets/pictures/fireStation.png")
class HighSchool(School):
    price = 80
    def __init__(self, capacity=0, saturation=0):
        super().__init__(1, 1, "assets/pictures/school.png", capacity, saturation)
class University(School):
    price = 100
    def __init__(self, capacity=0, saturation=0):
        super().__init__(2, 2, "assets/pictures/universityZone.png", capacity, saturation)
class Road(Building):
    price = 50
    type = ""

    def __init__(self,orientation="h"):
        if orientation == "v":
            assetname = "assets/pictures/street_v.png"
        elif orientation == "h":
            assetname = "assets/pictures/street_h.png"
        else :
            assetname = "assets/pictures/street_x.png"

        self.type = orientation
        super().__init__(1, 1, assetname)