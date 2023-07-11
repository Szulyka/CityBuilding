import pytest
import sys, os
import json

test_dir = os.path.dirname(__file__)
src_dir = '../src'
sys.path.insert(0,os.path.abspath(os.path.join(test_dir, src_dir)))
from city import City

@pytest.fixture
def empty_city():
    city = City(1000,100,1000)
    city.tiles.clear()
    city.save.clear()
    return city

@pytest.fixture
def single_neighbour():
    city = City(0,100,1000)
    city.loadGame("./neighbours.json")
    tmp = []
    for tile in city.tiles:
        if tile.coords[1] == 0:
            tmp.append(tile)
    return tmp

@pytest.fixture
def test_save1():
    with open("test_save.json", "r") as inputfile:
        return json.load(inputfile)

@pytest.mark.parametrize("input, expected",[((0,0,0), (0,0,0)), ((1000,1000,1000), (1000,1000,1000))]) 
def test_city_init(input, expected):
    city = City(input[0], input[1], input[2])
    assert city.population == expected[0] and city.happiness == expected[1] and city.money == expected[2]

@pytest.mark.parametrize("type, x,y,idx",[("police dep.", 0,0,0), ("police dep.", 80,0,2),("police dep.", 1560,0,39),("police dep.", 0,1000,1000),("police dep.", 160,0,4),("police dep.", 1560,1000,1039)]) 
def test_placeTile_1x1(type, x,y,idx):
    city = City(0,100,1000)
    for _ in range(5):
        city.placeTile(type, x,y,idx)
    assert len(city.tiles) == 1 + len(city.main_road)
    
@pytest.mark.parametrize("type, x,y,idx",[("residential", 0,0,0), ("residential", 80,0,2),("residential", 0,1000,1000),("residential", 160,0,4)]) 
def test_placeTile_2x2(type, x,y,idx):
    city = City(0,100,1000)
    for _ in range(5):
        city.placeTile(type, x,y,idx)
    assert len(city.tiles) == 1 + len(city.main_road)

def test_load_ticks(empty_city,test_save1):
    assert empty_city.loadGame("./test_save.json")[0] == test_save1["ticks"]

def test_load_population(empty_city, test_save1):
    city = empty_city
    city.loadGame("./test_save.json")
    print(city.population)
    assert city.population == test_save1["population"]

def test_load_money(empty_city, test_save1):
    city = empty_city
    city.loadGame("./test_save.json")
    assert city.money == test_save1["money"]

def test_load_happiness(empty_city, test_save1):
    city = empty_city
    city.loadGame("./test_save.json")
    assert city.happiness == test_save1["happiness"]

def test_road_accesibility():
    city = City(1000,100,1000)
    city.loadGame("./accesible.json")
    accesible = True
    for tile in city.tiles:
        accesible = accesible and city.roadAcces(tile)
    assert accesible

def test_road_naccesibility():
    city = City(1000,100,1000)
    city.loadGame("./inaccesible.json")
    accesible = False
    for tile in city.tiles:
        if tile.content.getType()[:6] != "street":
            accesible = accesible or city.roadAcces(tile)
    assert not accesible

def test_destroyTile(empty_city, test_save1):
    city = City(1000,100,1000)
    city.loadGame("./test_save.json")
    for item in test_save1["tiles"]:
        empty_city.destroyTile(item["type"], item["x"],item["y"],item["idx"])
    assert len(empty_city.tiles) == 0 and len(empty_city.save) == 0

@pytest.mark.parametrize("type, x,y,idx",[("residential", 0,0,0), ("residential", 80,0,2),("residential", 0,1000,1000),("residential", 160,0,4),("police dep.", 0,0,0), ("police dep.", 80,0,2),("police dep.", 1560,0,39),("police dep.", 0,1000,1000),("police dep.", 160,0,4),("police dep.", 1560,1000,1039)]) 
def test_getSelectedTile(type, x,y,idx):
    city = City(0,100,1000)
    city.placeTile(type, x,y,idx)
    assert city.getSelectedTile(x,y) != None

@pytest.mark.parametrize("type, x,y,idx",[("police dep.", 0,0,0), ("police dep.", 80,0,2),("police dep.", 1520,0,39),("police dep.", 0,1000,1000),("police dep.", 160,0,4),("police dep.", 1560,1000,1039)]) 
def test_getSelectedTile1x1(type, x,y,idx):
    city = City(0,100,1000)
    city.placeTile(type, x,y,idx)
    assert city.getSelectedTile(x+40,y) == None

@pytest.mark.parametrize("type, x,y,idx",[("residential", 0,0,0), ("residential", 80,0,2),("residential", 0,1000,1000),("residential", 160,0,4)]) 
def test_getSelectedTile2x2(type, x,y,idx):
    city = City(0,100,1000)
    city.placeTile(type, x,y,idx)
    assert city.getSelectedTile(x+80,y) == None

# def test_getNeighbours():
#     city = City(1000,100,1000)
#     city.loadGame("./neighbours.json")
#     result = True
#     for item in city.road[0]:
#         assert city.getNeighbour(item["x"], item["y"]) == {"count": 0, "north": False, "south": False, "east": False, "west": False}
#     assert result