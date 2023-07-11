class Zone():
    price = 0
    level = 0
    width = 2
    height = 2
    asset = ""
    capacity = 0
    # 0-100%
    saturation = 0

    def __init__(self, price, asset, capacity, saturation=0):
        self.price = price
        self.asset = asset
        self.capacity = capacity
        self.saturation = saturation
    def getType(self):
        return self.asset.split('/')[2][:-4]

    def upgrade(self):
        pass
class Residential(Zone):
    employment = 0 #%-ban
    satisfaction = 50
    def __init__(self, capacity, saturation, satisfaction = 50):
        super().__init__(200, "assets/pictures/residentialZone.png", capacity, saturation)
        self.satisfaction = satisfaction

    def resetSatisfaction(self):
        self.satisfaction = 50

    def adjustSatisfaction(self, amount):
        """
            Adjusts the satisfaction of the zone by the given amount whithin the boundaries.
        """
        self.satisfaction += amount
        if self.satisfaction > 100:
            self.satisfaction = 100
        elif self.satisfaction < 0:
            self.satisfaction = 0
class Industrial(Zone):
    def __init__(self, capacity, saturation):
        super().__init__(75, "assets/pictures/industrialZone.png", capacity, saturation)
class Service(Zone):
    def __init__(self, capacity, saturation):
        super().__init__(100, "assets/pictures/serviceZone.png", capacity, saturation)
class Stadium(Zone):
    price = 80
    def __init__(self):
        super().__init__(200, "assets/pictures/stadium.png", 0, 0)
