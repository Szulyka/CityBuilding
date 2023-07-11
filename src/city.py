import pygame
import math
import random
from tile import Tile
from building import *
from zone import *
import json

class City(object):
    tiles = []
    grid = []
    road = []
    save = []
    
    population = 0
    happiness = 0
    money = 0
    taxes = 1000
    taxRate = 100

    CITY_WIDTH = 40
    CITY_HEIGHT = 26

    main_road = [{'type': 'hor. street', 'x': 0, 'y': 520, 'idx': 520}, {'type': 'hor. street', 'x': 40, 'y': 520, 'idx': 521}, {'type': 'hor. street', 'x': 80, 'y': 520, 'idx': 522}, {'type': 'hor. street', 'x': 120, 'y': 520, 'idx': 523}, {'type': 'hor. street', 'x': 160, 'y': 520, 'idx': 524}, {'type': 'hor. street', 'x': 200, 'y': 520, 'idx': 525}, {'type': 'hor. street', 'x': 240, 'y': 520, 'idx': 526}, {'type': 'hor. street', 'x': 280, 'y': 520, 'idx': 527}, {'type': 'hor. street', 'x': 320, 'y': 520, 'idx': 528}, {'type': 'hor. street', 'x': 360, 'y': 520, 'idx': 529}, {'type': 'hor. street', 'x': 400, 'y': 520, 'idx': 530}, {'type': 'hor. street', 'x': 440, 'y': 520, 'idx': 531}]

    def __init__(self, population, happiness, money):
        self.population = population
        self.happiness = happiness
        self.money = money

        self.tiles = []
        self.grid = []
        self.road = []

        for y in range(0, self.CITY_HEIGHT):
            col = []
            for x in range(0, self.CITY_WIDTH):
                col.append({"x": None, "y": None, "type": None})
                self.grid.append(((x * 40, y * 40), pygame.Rect(320 + x * 40, 40 + y * 40, 40, 40)))
            self.road.append(col)
        for item in self.main_road:
            self.placeTile(item["type"], item["x"], item["y"], item["idx"], True)

    def saveGame(self,ticks, eY, eM, eD):
        """
            Saves the game in a json file
        """
        with open("save.json", "w") as outfile:
            for item in self.save:
                tile = self.getSelectedTile(item["x"], item["y"])
                if item["type"] in ["industrial", "service"]:
                    item["capacity"] = tile.content.capacity
                    item["saturation"] = tile.content.saturation
                if item["type"] == "residential":
                    item["capacity"] = tile.content.capacity
                    item["saturation"] = tile.content.saturation
                    item["satisfaction"] = tile.content.satisfaction
                    
            json_data = {
                "population": self.population,
                "happiness": self.happiness,
                "money": self.money,
                "taxes": self.taxes,
                "taxRate": self.taxRate,
                "ticks": ticks,
                "eY": eY,
                "eM": eM,
                "eD": eD,
                "tiles": self.save,
            }
            json.dump(json_data, outfile, indent=4)
    
    def roadAcces(self, tile):
        """
            Returns True if the tile is next to a road, False otherwise
        """
        if tile.height == 1 and tile.width == 1:
            return self._roadNeighbour(tile.coords[0], tile.coords[1])
        elif tile.height == 2 and tile.width == 2:
            return self._roadNeighbour(tile.coords[0], tile.coords[1]) or self._roadNeighbour(tile.coords[0]+40, tile.coords[1]) or self._roadNeighbour(tile.coords[0], tile.coords[1]+40) or self._roadNeighbour(tile.coords[0]+40, tile.coords[1]+40)
        return False
    
    def _roadNeighbour(self,x, y):
        """
            Returns True if the tile is next to a road, False otherwise
        """
        for tile in self.tiles:
            if tile.identify(x+40, y) and tile.content.getType()[:6] == "street":
                return True
        for tile in self.tiles:
            if tile.identify(x-40,y) and tile.content.getType()[:6] == "street":
                return True
        for tile in self.tiles:
            if tile.identify(x,y+40) and tile.content.getType()[:6] == "street":
                return True
        for tile in self.tiles:
            if tile.identify(x,y-40) and tile.content.getType()[:6] == "street":
                return True
        return False

    def loadGame(self,filename = "save.json"):
        """
            Loads a saved game
        """
        json_data = json.load(open(filename, "r"))
        self.population = json_data["population"]
        self.happiness = json_data["happiness"]
        self.money = json_data["money"]
        self.taxes = json_data["taxes"]
        self.taxRate = json_data["taxRate"]

        for item in json_data["tiles"]:
            tile = self.placeTile(item["type"], item["x"], item["y"], item["idx"], True)

            if item["type"] in ["industrial", "service"]:
                tile.capacity = item["capacity"]
                tile.saturation = item["saturation"]
            if item["type"] == "residential":
                tile.capacity = item["capacity"]
                tile.saturation = item["saturation"]
                tile.satisfaction = item["satisfaction"]
        return [json_data["ticks"], json_data["eY"], json_data["eM"], json_data["eD"]]

    def destroyTile(self, type, x, y, idx):
        """
            Destroys the tile at the given coordinates
        """
        indexes = [idx]
        for tile in self.tiles:
            coords = []
            coords.append(tile.coords)

            if tile.width != 1:
                coords.append((tile.coords[0]+40, tile.coords[1]))
            if tile.height != 1:
                coords.append((tile.coords[0], tile.coords[1]+40))
            if tile.width != 1 and tile.height != 1:
                coords.append((tile.coords[0]+40, tile.coords[1]+40))

            if (x,y) in coords:
                if type[:6] == "street":
                    x = int(idx/40)
                    y = idx % 40
                    if self.getNeighbour(x,y)["count"] > 1:
                        return
                    self.road[x][y] = {"x": None, "y": None, "type": None}

                for coord in coords:
                    indexes.append(coord[1] + coord[0]/40)
                if type == "residential":
                    self.population -= int(tile.content.capacity * tile.content.saturation / 100)
                    self.calcPopulation()
                    self.updateWorkers()
                self.tiles.remove(tile)
                self.money += int(self.payBack(type))
        for item in self.save:
            for id in indexes:
                if id == item["idx"]:
                    self.save.remove(item)
                    break
    
    def getSelectedTile(self, x,y):
        """
        Returns the tile at the given coordinates
        """
        for tile in self.tiles:
            if tile.identify(x,y):
                return tile
        return None



    def placeTile(self, type, x, y, idx, loading_save = False):
        """
        Places a tile at the given coordinates
        """
        content = None
        if type == "police dep.":
            content = Police()
        elif type == "fire dep.":
            content = FireDepartment()
        elif type == "ver. street":
            content = self.placeRoad(idx,x,y, "v") #coords in pixel
        elif type == "hor. street":
            content = self.placeRoad(idx,x,y, "h")
        elif type == "school":
            content = HighSchool(200, 0)
        elif type == "university":
            content = University(200, 0)
        elif type == "stadium":
            content = Stadium()
        elif type == "residential":
            content = Residential(400, 25)
        elif type == "industrial":
            content = Industrial(400, 0)
        elif type == "service":
            content = Service(400, 0)
            
        if not self.isSpotAvailable(x, y, content.width, content.height):
            content = None
            return
        
        self.save.append({"type": type, "x": x, "y": y, "idx": idx})

        if self.pay(content.price, loading_save):
            self.tiles.append(Tile((x, y), content.width, content.height, content))
            self.placeX()
            if type == "residential":
                self.calcPopulation()
            self.updateWorkers()
        return content

    def pay(self, amount, loading_save):
        """
            Returns True if the player can pay the amount of money, False otherwise
        """
        if loading_save:
            return True
        if self.money > amount:
            self.money -= amount
            return True
        self.happiness *= 0.95
        self.money -= amount
        return True
    
    def payBack(self, type):
        """
            Returns the amount of money to pay back to the player when he destroys a building
        """
        if type == "policeStation":
            return Police().price / 2
        elif type == "fireStation":
            return FireDepartment().price / 2
        elif type == "street_v":
            return Road().price / 2
        elif type == "street_h":
            return Road().price / 2
        elif type == "school":
            return School().price / 2
        elif type == "residentialZone":
            return Residential(0,0).price / 2
        elif type == "industrialZone":
            return Industrial(0,0).price / 2
        elif type == "serviceZone":
            return Service(0,0).price / 2
        elif type == "stadium":
            return Stadium().price / 2
        elif type == "universityZone":
            return University().price / 2

    def placeRoad(self, idx, pos_x, pos_y, orinentation):
        """
            Places a road on the map
        """
        x = int(idx/40)
        y = idx % 40
        self.road[x][y]["x"] = pos_x
        self.road[x][y]["y"] = pos_y
        self.road[x][y]["type"] = orinentation
        return Road(orinentation)

    def placeX(self):
        """
            Creates crossroads when needed
        """
        for i in range(26):
            for j in range(40):
                neighbours = self.getNeighbour(i,j)
                if neighbours["count"] == 2:
                    if neighbours["north"] and neighbours["east"]:
                        self.replaceRoad(self.road[i][j]["x"], self.road[i][j]["y"], "ne")
                    if neighbours["north"] and neighbours["west"]:
                        self.replaceRoad(self.road[i][j]["x"], self.road[i][j]["y"], "nw")
                    if neighbours["south"] and neighbours["east"]:
                        self.replaceRoad(self.road[i][j]["x"], self.road[i][j]["y"], "se")
                    if neighbours["south"] and neighbours["west"]:
                        self.replaceRoad(self.road[i][j]["x"], self.road[i][j]["y"], "sw")
                    if neighbours["north"] and neighbours["south"]:
                        self.replaceRoad(self.road[i][j]["x"], self.road[i][j]["y"], "v")
                    if neighbours["west"] and neighbours["east"]:
                        self.replaceRoad(self.road[i][j]["x"], self.road[i][j]["y"], "h")
                if neighbours["count"] == 3:
                    if neighbours["north"] and neighbours["east"] and neighbours["west"]:
                        self.replaceRoad(self.road[i][j]["x"], self.road[i][j]["y"], "wne")
                    if neighbours["south"] and neighbours["east"] and neighbours["west"]:
                        self.replaceRoad(self.road[i][j]["x"], self.road[i][j]["y"], "wse")
                    if neighbours["north"] and neighbours["east"] and neighbours["south"]:
                        self.replaceRoad(self.road[i][j]["x"], self.road[i][j]["y"], "nes")
                    if neighbours["north"] and neighbours["west"] and neighbours["south"]:
                        self.replaceRoad(self.road[i][j]["x"], self.road[i][j]["y"], "nws")
                if neighbours["count"] == 4:
                    self.replaceRoad(self.road[i][j]["x"], self.road[i][j]["y"], "x")
                if neighbours["count"] == 1:
                    if neighbours["north"]:
                        self.replaceRoad(self.road[i][j]["x"], self.road[i][j]["y"], "v")
                    if neighbours["south"]:
                        self.replaceRoad(self.road[i][j]["x"], self.road[i][j]["y"], "v")
                    if neighbours["west"]:
                        self.replaceRoad(self.road[i][j]["x"], self.road[i][j]["y"], "h")
                    if neighbours["east"]:
                        self.replaceRoad(self.road[i][j]["x"], self.road[i][j]["y"], "h")
                
                

    def getNeighbour(self, x,y):
        """Return a dictionnary with the number of neighbours and the direction of each one"""
        r = self.road
        res = {"count": 0, "north": False, "south": False, "east": False, "west": False}
        if self.road[x][y]["type"] != None:
            if x+1 < 26 and self.road[x+1][y]["type"] != None:
                res["south"] = True
                res["count"] += 1
            if x-1 >= 0 and self.road[x-1][y]["type"] != None:
                res["north"] = True
                res["count"] += 1
            if y-1 >= 0 and self.road[x][y-1]["type"] != None:
                res["west"] = True
                res["count"] += 1
            if (y+1 < 40 ) and (self.road[x][y+1]["type"] != None):
                res["east"] = True
                res["count"] += 1
        return res
    
    def replaceRoad(self, x, y, orientation = "h"):
        """
            Replace a road by a new one with the right orientation
            x, y: top left corner of the road
            orientation: orientation of the road
        """
        for tile in self.tiles:
            if tile.identify(x,y):
                tile.setContent(Road(orientation))

    def isSpotAvailable(self, x, y, width, height):
        """
            Check if the spot is available for a building
            x, y: top left corner of the building   
            width, height: width and height of the building
        """
        newCoords = []
        for i in range(width):
            for j in range(height):
                newCoords.append((x + i*40, y + j*40))

        for tile in self.tiles:
            coords = []
            coords.append(tile.coords)
            if tile.width != 1:
                coords.append((tile.coords[0]+40, tile.coords[1]))
            if tile.height != 1:
                coords.append((tile.coords[0], tile.coords[1]+40))
            if tile.width != 1 and tile.height != 1:
                coords.append((tile.coords[0]+40, tile.coords[1]+40))
            for coord in newCoords:
                if coord in coords or (tile.width != 1 and coord[0] > 39 * 40) or (tile.height != 1 and coord[1] > 25 * 40):
                    return False
        return True

    def countZones(self, type):
        """
            Counts the number of zones of a given type.
        """
        count = 0
        for tile in self.tiles:
            if tile.content != None:
                if tile.content.getType() == type:
                    count += 1
        return count
    
    def sumZoneCapacity(self, type):
        """
            Sums the capacity of the zones of a given type.
        """
        count = 0
        for tile in self.tiles:
            if tile.content != None:
                if tile.content.getType() == type:
                    count += tile.content.capacity
        return count

    def moveIn(self):
        """
            Moves in the people in the residential zones.
        """
        for tile in self.tiles:
            if not self.roadAcces(tile):
                continue
            if tile.content != None:
                if tile.content.getType() == "residentialZone" and tile.content.saturation < 100:
                    toAdd = random.randint(20,50)
                    if self.happiness > 25:
                        toAdd += 1
                    if self.happiness > 50:
                        toAdd += 1
                    if self.happiness > 75:
                        toAdd += 1
                
                    if tile.content.saturation + toAdd > 100:
                        tile.content.saturation = 100
                    else:
                        tile.content.saturation += toAdd / tile.content.capacity * 100

    def calcPopulation(self):
        """
            Calculates the population of the city.
        """
        population = 0
        for tile in self.tiles:
            if tile.content != None:
                if tile.content.getType() == "residentialZone":
                    population += int(tile.content.capacity * tile.content.saturation / 100)
        self.population = population

    def isTileInRadius(self, tile, radius, type):
        """
            Returns a list of tiles of a certain type in a certain radius. The distance is calculated using the center of the tiles.
        """
        tilesInRadius = []
        tileCenterX = tile.coords[0] + tile.width * 20
        tileCenterY = tile.coords[1] + tile.height * 20
        for t in self.tiles:
            if t.content.getType() == type and self.roadAcces(t):
                tileX = t.coords[0] + t.width * 20
                tileY = t.coords[1] + t.height * 20
                if math.sqrt((tileCenterX - tileX)**2 + (tileCenterY - tileY)**2) <= radius * 40:
                    tilesInRadius.append(t)
        return tilesInRadius

    def adjustHappiness(self):
        """
            Adjusts the happiness of the city based on the satisfaction of the residential zones and the amount of industrial and service zones in a certain radius.
        """
        self.happiness = 0
        for tile in self.tiles:
            if not self.roadAcces(tile):
                continue
            if tile.content.getType() == "residentialZone":
                tile.content.resetSatisfaction()
                industrialZones = self.isTileInRadius(tile, 7, "industrialZone")
                serviceZones = self.isTileInRadius(tile, 7, "serviceZone")
                stadiums = self.isTileInRadius(tile, 7, "stadium")
                schools = self.isTileInRadius(tile, 7, "school") + self.isTileInRadius(tile, 7, "university")
                policeStations = self.isTileInRadius(tile, 7, "policeStation")
                if len(industrialZones) != 0:
                    tile.content.adjustSatisfaction(-5 * len(industrialZones))
                if len(serviceZones) != 0:
                    tile.content.adjustSatisfaction(10 * len(serviceZones))
                if len(stadiums) != 0:
                    tile.content.adjustSatisfaction(20 * len(stadiums))
                if len(schools) != 0:
                    tile.content.adjustSatisfaction(15 * len(schools))
                if len(policeStations) != 0:
                    tile.content.adjustSatisfaction(5 * len(policeStations))
                
        collectiveHappiness = []
        for tile in self.tiles:
            if tile.content.getType() == "residentialZone":
                collectiveHappiness.append(tile.content.satisfaction)
        if len(collectiveHappiness) == 0:
            self.happiness = 50
        else:
            self.happiness = int(sum(collectiveHappiness) / len(collectiveHappiness))
        self.happiness -= int((self.taxRate - 100) / 10)
        if self.money < 0:
            self.happiness -= 25

        if self.population > self.sumZoneCapacity("industrialZone") + self.sumZoneCapacity("serviceZone"):
            self.happiness -= 10

        if self.happiness < 0:
            self.happiness = 0
        if self.happiness > 100:
            self.happiness = 100

    def updateTax(self):
        self.taxes = int(((self.population * 0.01) + 10) * self.taxRate)
    
    def collectTaxes(self):
        """
            Collects taxes from the residential zones.
        """
        for tile in self.tiles:
            if not self.roadAcces(tile):
                continue
            if tile.content.getType() == "residentialZone":
                self.money += int(self.taxes * tile.content.saturation / 100)
            elif tile.content.getType() == "school":
                self.money += int((tile.content.capacity * (tile.content.saturation / 100)) * 10)
            elif tile.content.getType() == "universityZone":
                self.money += int((tile.content.capacity * (tile.content.saturation / 100)) * 20)

    def updateWorkers(self):
        """
            Updates the workers of the industrial and service zones.
        """
        iCount = self.countZones("industrialZone")
        sCount = self.countZones("serviceZone")
        iWorkers = 0
        sWorkers = 0
        if (iCount != 0):
            iWorkers = int(self.population * 0.8 / 2 / iCount)
        if (sCount != 0):
            sWorkers = int(self.population * 0.8 / 2 / sCount)
        for tile in self.tiles:
            if not self.roadAcces(tile):
                continue
            if tile.content.getType() == "industrialZone":
                tile.content.saturation = iWorkers / tile.content.capacity * 100
            if tile.content.getType() == "serviceZone":
                tile.content.saturation = sWorkers / tile.content.capacity * 100

    def updateStudents(self):
        """
            Updates the students of the schools.
        """
        hsCount = self.countZones("school")
        uCount = self.countZones("universityZone")
        hsStudents = 0
        uStudents = 0
        if (hsCount != 0):
            hsStudents = int(self.population * random.uniform(0.4, 0.5) / 2 / hsCount)
        if (uCount != 0):
            uStudents = int(self.population * random.uniform(0.2, 0.3) / 2 / uCount)
        for tile in self.tiles:
            if not self.roadAcces(tile):
                continue
            if tile.content.getType() == "school":
                tile.content.saturation = hsStudents / tile.content.capacity * 100
            elif tile.content.getType() == "universityZone":
                tile.content.saturation = uStudents / tile.content.capacity * 100

    def updateYear(self):
        """
            Updates the year of the city. This function is called every 12 months.
        """
        self.collectTaxes()
        self.updateStudents()

    def updateMonth(self):
        """
            Updates the month of the city. This function is called every month.
        """
        self.moveIn()
        self.calcPopulation()
        self.updateWorkers()

    def updateDay(self):
        """
            Updates the day of the city. This function is called every day.
        """
        self.updateTax()
        self.adjustHappiness()