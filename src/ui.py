import pygame
import pygame_gui
import datetime


class UI(object):
    renderer = None
    city = None

    TOOLBAR_HEIGHT = 40
    PANEL_WIDTH = 320
    PANEL_PADDING_X = 25
    PANEL_PADDING_Y = 25
    STAT_PADDING = 42
    
    buildingIcons = ["assets/pictures/residentialZone.png", "assets/pictures/industrialZone.png", "assets/pictures/serviceZone.png", "assets/pictures/policeStation.png", "assets/pictures/fireStation.png", "assets/pictures/school.png", "assets/pictures/universityZone.png", "assets/pictures/stadium.png", "assets/pictures/street_h.png", "assets/pictures/street_v.png" ]
    
    buildingNames = ["residential", "industrial", "service", "police dep.", "fire dep.", "school", "university", "stadium", "hor. street", "ver. street"]
    menuButtonId = ["m_ng2", "m_ex2", "m_con", "m_ex1"]
    buttons = []
    stats = []
    zoneStat = { "capacity" : 0, "satisfaction" : 0, "saturation" : 0}
    selectedBuilding = 0

    date = datetime.date(2023, 1, 1)
    # every second a virtual day passes
    tickRate = 1
    ticks = 0
    isTimeStopped = False
    eY = 0
    eM = 0
    eD = 0


    stats = [
        {"name": "", "value": date.strftime('%Y.%m.%d')},
        {"name": "Population", "value": ""},
        {"name": "Happiness", "value": ""},
        {"name": "Money", "value": ""},
    ]

    def __init__(self, renderer, city):
        self.renderer = renderer
        self.city = city

    def removeButton(self, id):
        """Removes buttons with the given ID from the button list"""
        for i in self.buttons:
            if i[0] == id:
                self.buttons.remove(i)

    def removeMenuButtons(self):
        """Removes menu buttons from the button list"""
        for id in self.menuButtonId:
            self.removeButton(id)

    def updateTime(self):
        daysElapsed = int((self.ticks / 1000))
        self.stats[0]["value"] = (self.date + datetime.timedelta(days=daysElapsed)).strftime('%Y.%m.%d')
        currentYear = int(self.stats[0]["value"][0:4])
        elapsedYears = currentYear - self.date.year
        currentMonth = int(self.stats[0]["value"][5:7])
        elapsedMonths = currentMonth - self.date.month
        currentDay = int(self.stats[0]["value"][8:10])
        elapsedDays = currentDay - self.date.day
        if elapsedYears != self.eY:
            self.city.updateYear()
        if elapsedMonths != self.eM:
            self.city.updateMonth()
        if elapsedDays != self.eD:
            self.city.updateDay()
        self.eY = elapsedYears
        self.eM = elapsedMonths
        self.eD = elapsedDays

    def addButton(self, button):
        """Adds a button to the button list"""
        for i in self.buttons:
            if i[0] == button[0]:
                return
        self.buttons.append(button)

    def toolbarButton(self, id, label, x, y, width, height, color):
        self.renderer.draw_rect(x, y, width, height, color)
        text = self.renderer.toolbar_font.render(
            label, True, self.renderer.black)
        rect = text.get_rect(center=(x + width / 2, y + height / 2))
        self.renderer.buffer_surface.blit(text, rect)
        return (id, label, pygame.Rect(x, y, width, height))  # unique ID added

    def timeButton(self, id, label, x, y, width, height, color):
        '''makes time controlling buttons'''
        self.renderer.draw_rect(x, y, width, height, color)
        text = self.renderer.toolbar_font.render(
            label, True, self.renderer.black)
        rect = text.get_rect(center=(x + width / 2, y + height / 2))
        self.renderer.buffer_surface.blit(text, rect)
        return (id, label, pygame.Rect(x, y, width, height))

    def menuButton(self, id, label, x, y, width, height, color):
        self.renderer.draw_rect(
            x - width / 2, y - height / 2, width, height, color)
        text = self.renderer.menu_font.render(label, True, self.renderer.black)
        rect = text.get_rect(center=(x, y))
        self.renderer.buffer_surface.blit(text, rect)
        # unique ID added
        return (id, label, pygame.Rect(x - width / 2, y - height / 2, width, height))

    def buildButton(self, id, x, y, width, height, label):
        # draw border
        # self.renderer.draw_rect(x, y, width, height, self.renderer.black)
        self.renderer.draw_rect(x + 3, y + 3, width - 6,
                                height - 6, self.renderer.panel_bg)
        text = self.renderer.stat_font.render(label, True, self.renderer.black)
        rect = text.get_rect(center=(x + width / 2, y + height / 2))
        self.renderer.buffer_surface.blit(text, rect)
        return (id, label, pygame.Rect(x, y, width, height))

    def buildingButton(self, id, image, x, y, width, height):
        if (int(id[3:]) == self.selectedBuilding):
            self.renderer.draw_rect(x, y, width, height, self.renderer.yellow)
        else:
            self.renderer.draw_rect(
                x, y, width, height, self.renderer.soft_black)
        self.renderer.draw_rect(x + 3, y + 3, width - 6,
                                height - 6, (255, 255, 255))
        image = pygame.image.load(image)
        image = pygame.transform.scale(image, (width - 6, height - 6))
        self.renderer.buffer_surface.blit(image, (x + 3, y + 3))
        return (id, image, pygame.Rect(x, y, width, height))

    def toolbar(self):
        self.renderer.draw_rect(
            0, 0, self.renderer.screen_size[0], self.TOOLBAR_HEIGHT, (255, 255, 255))
        self.addButton(self.toolbarButton("t_ng", "Menu", 0,
                       0, 120, self.TOOLBAR_HEIGHT, (255, 255, 255)))
        self.addButton(self.toolbarButton("t_sg", "Save game",
                       120, 0, 120, self.TOOLBAR_HEIGHT, (255, 255, 255)))
        self.renderer.draw_line(
            0, self.TOOLBAR_HEIGHT-1, self.renderer.screen_size[0], self.TOOLBAR_HEIGHT-1, (185, 185, 185))
        self.addButton(self.toolbarButton(
            "t_ex", "Exit", self.renderer.screen_size[0] - 80, 0, 80, self.TOOLBAR_HEIGHT, self.renderer.red))

    def stat(self, name, value, x, y, space=250):  # added space to parameters so time looks fine
        self.renderer.draw_text(self.renderer.stat_font,
                                name, x, y, self.renderer.black)
        self.renderer.draw_text(self.renderer.stat_font, str(
            value), x + space, y, self.renderer.black)
        
    def statRed(self, name, value, x, y, space=250):  # added space to parameters so time looks fine
        self.renderer.draw_text(self.renderer.stat_font,
                                name, x, y, self.renderer.red)
        self.renderer.draw_text(self.renderer.stat_font, str(
            value), x + space, y, self.renderer.red)

    def statBigger(self, name, value, x, y, space=250):
        self.renderer.draw_text(self.renderer.toolbar_font,
                                name, x, y, self.renderer.black)
        self.renderer.draw_text(self.renderer.toolbar_font, str(
            value), x + space, y, self.renderer.black)


    def buildingNamesForButtons(self, text, x, y):
        self.renderer.draw_text(self.renderer.building_font,
                                text, x, y, self.renderer.black)

    def panel(self, space=250):
        self.renderer.draw_rect(0, self.TOOLBAR_HEIGHT, self.PANEL_WIDTH,
                                self.renderer.screen_size[1] - self.TOOLBAR_HEIGHT, self.renderer.panel_bg)
        self.stat("Time:", self.stats[0]["value"], self.PANEL_PADDING_X,
                  self.TOOLBAR_HEIGHT + self.PANEL_PADDING_Y, space - 130)
        self.addButton(self.timeButton("t_S", "0.5x", self.PANEL_PADDING_X,
                       self.TOOLBAR_HEIGHT + 70, 70, 30, (153, 153, 153)))
        self.addButton(self.timeButton("t_P", "|| / >", self.PANEL_PADDING_X +
                       100, self.TOOLBAR_HEIGHT + 70, 70, 30, (153, 153, 153)))
        self.addButton(self.timeButton("t_F", "2x", self.PANEL_PADDING_X +
                       200, self.TOOLBAR_HEIGHT + 70, 70, 30, (153, 153, 153)))

        self.stat("Population:", self.city.population, self.PANEL_PADDING_X,
                  self.TOOLBAR_HEIGHT + self.PANEL_PADDING_Y + self.STAT_PADDING * 2, space - 30)
        self.stat("Happiness:", round(self.city.happiness, 1), self.PANEL_PADDING_X,
                  self.TOOLBAR_HEIGHT + self.PANEL_PADDING_Y + self.STAT_PADDING * 3, space - 30)
        if self.city.money >= 0:
            self.stat("Money:", self.city.money, self.PANEL_PADDING_X,
                    self.TOOLBAR_HEIGHT + self.PANEL_PADDING_Y + self.STAT_PADDING * 4, space - 60)
        else:
            self.statRed("Money:", self.city.money, self.PANEL_PADDING_X,
                    self.TOOLBAR_HEIGHT + self.PANEL_PADDING_Y + self.STAT_PADDING * 4, space - 60)
        self.stat("Time:", self.stats[0]["value"], self.PANEL_PADDING_X,
                  self.TOOLBAR_HEIGHT + self.PANEL_PADDING_Y, space - 130)
        self.addButton(self.timeButton("t_S", "0.5x", self.PANEL_PADDING_X,
                       self.TOOLBAR_HEIGHT + 70, 70, 30, (153, 153, 153)))
        self.addButton(self.timeButton("t_P", "|| / >", self.PANEL_PADDING_X +
                       100, self.TOOLBAR_HEIGHT + 70, 70, 30, (153, 153, 153)))
        self.addButton(self.timeButton("t_F", "2x", self.PANEL_PADDING_X +
                       200, self.TOOLBAR_HEIGHT + 70, 70, 30, (153, 153, 153)))

        self.renderer.draw_line(self.PANEL_PADDING_X, 280, self.PANEL_WIDTH -
                                self.PANEL_PADDING_X, 280, self.renderer.black)
        # build button

        if self.renderer.buildMode:
            self.renderer.draw_rect(
                self.PANEL_PADDING_X, 300, 123, 80, self.renderer.red)
        else:
            self.renderer.draw_rect(
                self.PANEL_PADDING_X, 300, 123, 80, self.renderer.black)
        self.addButton(self.buildButton(
            "p_bm", self.PANEL_PADDING_X, 300, 123, 80, "Build"))

        if self.renderer.destroyMode:
            self.renderer.draw_rect(
                (self.PANEL_PADDING_X*2) + 123, 300, 123, 80, self.renderer.red)
        else:
            self.renderer.draw_rect(
                (self.PANEL_PADDING_X*2) + 123, 300, 123, 80, self.renderer.black)
        self.addButton(self.buildButton(
            "p_dm", (self.PANEL_PADDING_X*2) + 123, 300, 123, 80, "Destroy"))

        BUILDING_BUTTONS_PADDING = 20
        # building buttons
        self.addButton(self.buildingButton(
            "p_B0", self.buildingIcons[0], BUILDING_BUTTONS_PADDING, 400, 80, 80))
        self.buildingNamesForButtons(self.buildingNames[0], self.PANEL_PADDING_X + 5, 400 + 80 + 10)
        
        self.addButton(self.buildingButton(
            "p_B1", self.buildingIcons[1], BUILDING_BUTTONS_PADDING * 2 + 80, 400, 80, 80))
        self.buildingNamesForButtons(self.buildingNames[1], self.PANEL_PADDING_X + 5 * 2 + 80 + 15, 400 + 80 + 10)
        
        self.addButton(self.buildingButton(
            "p_B2", self.buildingIcons[2], BUILDING_BUTTONS_PADDING * 3 + 80 * 2, 400, 80, 80))
        self.buildingNamesForButtons(self.buildingNames[2], self.PANEL_PADDING_X + 5 * 3 + 80 * 2 + 35, 400 + 80 + 10)
        
        
        self.addButton(self.buildingButton(
            "p_B3", self.buildingIcons[3], BUILDING_BUTTONS_PADDING, 400 + 120, 80, 80))
        self.buildingNamesForButtons(self.buildingNames[3], self.PANEL_PADDING_X + 5, 400 + 60 + 10 + 140)
        
        self.addButton(self.buildingButton(
            "p_B4", self.buildingIcons[4],BUILDING_BUTTONS_PADDING *2 + 80, 400 + 120, 80, 80))
        self.buildingNamesForButtons(self.buildingNames[4], self.PANEL_PADDING_X + 5 * 2 + 80 + 20, 400 + 60 + 10 + 140)
        
        self.addButton(self.buildingButton(
            "p_B5", self.buildingIcons[5], self.PANEL_PADDING_X + 5 * 3 + 80 * 2 + 20, 400 + 120, 80, 80))
        self.buildingNamesForButtons(self.buildingNames[5], self.PANEL_PADDING_X + 5 * 3 + 80 * 2 + 40, 400 + 60 + 10 + 140)
        
        
        self.addButton(self.buildingButton(
            "p_B6", self.buildingIcons[6], BUILDING_BUTTONS_PADDING, 400 + 120 * 2, 80, 80))
        self.buildingNamesForButtons(self.buildingNames[6], self.PANEL_PADDING_X + 5, 400 + 80 + 10 + 120 * 2)
        
        self.addButton(self.buildingButton(
            "p_B7", self.buildingIcons[7], BUILDING_BUTTONS_PADDING * 2 + 80, 400  + 120 * 2, 80, 80))
        self.buildingNamesForButtons(self.buildingNames[7], self.PANEL_PADDING_X + 5 * 2 + 80 + 20, 400 + 80 + 10 + 120 * 2)
        
        self.addButton(self.buildingButton(
            "p_B8", self.buildingIcons[8], BUILDING_BUTTONS_PADDING * 3 + 80 * 2, 400 + 120 * 2, 80, 80))
        self.buildingNamesForButtons("street", self.PANEL_PADDING_X + 5 * 3 + 80 * 2 + 40, 400 + 80 + 10 + 120 * 2)
        
        #infomration panel for built zones:
        self.renderer.draw_line(self.PANEL_PADDING_X, 760, self.PANEL_WIDTH -
                                self.PANEL_PADDING_X, 760, self.renderer.black)
        
        self.stat("Selected zone info", "", self.PANEL_PADDING_X + 10, 780, space - 30)
        
        self.statBigger("Capacity:", int(self.zoneStat["capacity"]), self.PANEL_PADDING_X + 10, 780 + 40, space - 30)
        self.statBigger("Saturation:", str(round(self.zoneStat["saturation"], 1))+'%', self.PANEL_PADDING_X + 10, 810 + 40, space - 30)
        
        if self.zoneStat["satisfaction"] != -1:
            self.statBigger("Satisfaction:", str(round(self.zoneStat["satisfaction"], 1))+'%', self.PANEL_PADDING_X + 10, 840 + 40, space - 30)
        
        self.renderer.draw_rect(self.PANEL_PADDING_X, 910, 270, 50, self.renderer.black)
        self.addButton(self.buildButton("p_U", self.PANEL_PADDING_X, 910, 270, 50, "Upgrade"))
        
        self.renderer.draw_line(self.PANEL_PADDING_X, 970, self.PANEL_WIDTH - self.PANEL_PADDING_X, 970, self.renderer.black)
        
        #tax panel
        self.stat("Current tax:", int(self.city.taxes) , self.PANEL_PADDING_X + 10, 980, space - 70)
        #egy ev elteltevel adodjon hozza a penzhez
        self.renderer.draw_rect(self.PANEL_PADDING_X, 1020, 130, 40, self.renderer.black)
        self.addButton(self.buildButton("p_+", self.PANEL_PADDING_X, 1020, 130, 40, "+"))
        
        self.renderer.draw_rect(self.PANEL_PADDING_X + 140, 1020, 130, 40, self.renderer.black)
        self.addButton(self.buildButton("p_-", self.PANEL_PADDING_X + 140, 1020, 130, 40, "-"))

    def menuButtons(self, isContinue=True):
        if isContinue:
            self.addButton(self.menuButton(
                "m_con", "Load save", self.renderer.screen_size[0] / 2, self.renderer.screen_size[1] / 2, 300, 80, self.renderer.off_white))
            self.addButton(self.menuButton(
                "m_ng1", "New Game", self.renderer.screen_size[0] / 2, self.renderer.screen_size[1] / 2 + 100, 300, 80, self.renderer.off_white))
            self.addButton(self.menuButton(
                "m_ex1", "Exit", self.renderer.screen_size[0] / 2, self.renderer.screen_size[1] / 2 + 200, 300, 80, self.renderer.off_white))
        else:
            self.addButton(self.menuButton(
                "m_ng2", "New Game", self.renderer.screen_size[0] / 2, self.renderer.screen_size[1] / 2, 300, 80, self.renderer.off_white))
            self.addButton(self.menuButton(
                "m_ex2", "Exit", self.renderer.screen_size[0] / 2, self.renderer.screen_size[1] / 2 + 100, 300, 80, self.renderer.off_white))

    def menu(self):
        self.renderer.draw_rect(
            0, 0, self.renderer.screen_size[0], self.renderer.screen_size[1], (255, 255, 255))
        title_surface = self.renderer.title_font.render(
            "Sim City 2", True, self.renderer.black)
        title_rect = title_surface.get_rect(center=(
            self.renderer.screen_size[0] / 2, self.renderer.screen_size[1] / 2 - 200))
        self.renderer.buffer_surface.blit(title_surface, title_rect)
        self.menuButtons()

    def update(self):
        self.updateStats()

    def updateStats(self):
        self.stats[1]["value"] = self.city.population
        self.stats[2]["value"] = self.city.happiness
        self.stats[3]["value"] = self.city.money

    def updateZoneStats(self, tile):
        if tile.getType() == "residentialZone":
            self.zoneStat["capacity"] = tile.capacity
            self.zoneStat["saturation"] = tile.saturation
            self.zoneStat["satisfaction"] = tile.satisfaction
        else:
            self.zoneStat["capacity"] = tile.capacity
            self.zoneStat["saturation"] = tile.saturation
            self.zoneStat["satisfaction"] = -1


    def clearZoneStats(self):
        self.zoneStat["capacity"] = 0
        self.zoneStat["saturation"] = 0
        self.zoneStat["satisfaction"] = 0

    def draw(self):
        self.panel()
        self.toolbar()
