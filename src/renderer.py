import pygame
import os.path

class Renderer(object):
    city = None

    screen_size = (1920, 1080)
    screen = None
    buffer_surface = None
    working_dir = os.path.join(os.path.dirname(__file__), "assets")

    toolbar_font = None
    stat_font = None
    menu_font = None
    title_font = None

    BUILDING_FONT_SIZE = 12
    TOOLBAR_FONT_SIZE = 18
    STAT_FONT_SIZE = 28
    MENU_FONT_SIZE = 36
    TITLE_FONT_SIZE = 112

    OFFSET_X = 320
    OFFSET_Y = 40

    TILE_SIZE = 40

    buildMode = False
    destroyMode = False 
    
    red = pygame.Color(245, 0, 54, 0)
    black = pygame.Color(11, 11, 11)
    soft_black = pygame.Color(40, 40, 40)
    yellow = pygame.Color(228, 226, 41)
    off_white = pygame.Color(235, 235, 235)
    panel_bg = pygame.Color(215, 215, 215)
    panel_stats_bg = pygame.Color(235, 235, 235)
    grid_line = pygame.Color(20, 95, 0, 0)
    grass = pygame.Color(32, 151, 0)

    def __init__(self, title, city):
        pygame.init()
        self.screen_size = pygame.display.Info().current_w, pygame.display.Info().current_h
        self.screen = pygame.display.set_mode(self.screen_size, pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.FULLSCREEN | pygame.SRCALPHA)
        self.buffer_surface = pygame.Surface(self.screen_size)
        try:
            self.building_font = pygame.font.Font(os.path.abspath(os.path.join("assets", "fonts", "Rubik-Medium.ttf")), self.BUILDING_FONT_SIZE)
            self.toolbar_font = pygame.font.Font(os.path.abspath(os.path.join("assets", "fonts", "Rubik-Medium.ttf")), self.TOOLBAR_FONT_SIZE)
            self.stat_font = pygame.font.Font(os.path.abspath(os.path.join("assets","fonts", "Rubik-Medium.ttf")), self.STAT_FONT_SIZE)
            self.menu_font = pygame.font.Font(os.path.abspath(os.path.join("assets","fonts", "Rubik-SemiBold.ttf")), self.MENU_FONT_SIZE)
            self.title_font = pygame.font.Font(os.path.abspath(os.path.join("assets","fonts", "Rubik-SemiBold.ttf")), self.TITLE_FONT_SIZE)
        except FileNotFoundError:
                    print("Could not load fonts, game launched from wrong directory, please move to x-team folder and try 'python3 ./src/main.py'.")
                    pygame.quit()
                    quit()
        pygame.display.set_caption(title)
        self.city = city

    def update(self):
        self.screen.blit(self.buffer_surface, (0, 0))
        pygame.display.flip()

    def draw_rect(self, x, y, width, height, color):
        pygame.draw.rect(self.buffer_surface, color, (x, y, width, height))

    def draw_line(self, x1, y1, x2, y2, color):
        pygame.draw.line(self.buffer_surface, color, (x1, y1), (x2, y2))

    def draw_tile(self, asset, x, y, width, height):
        image = pygame.image.load(asset)
        image = pygame.transform.scale(image, (width * self.TILE_SIZE, height * self.TILE_SIZE))
        self.buffer_surface.blit(image, (x + self.OFFSET_X, y + self.OFFSET_Y, width * self.TILE_SIZE, height * self.TILE_SIZE))

    def draw_text(self, font, text, x, y, color):
        _text = font.render(text, True, color)
        self.buffer_surface.blit(_text, (x, y))
        return _text

    def clearScreen(self):
        self.buffer_surface.fill((0,0,0,0))

    def drawGrid(self):
        """Draw the grid"""
        for x in range(self.OFFSET_X + self.TILE_SIZE, self.screen_size[0], self.TILE_SIZE):
            self.draw_line(x, self.OFFSET_Y, x, self.screen_size[1], self.grid_line)
        for y in range(self.OFFSET_Y + self.TILE_SIZE, self.screen_size[1], self.TILE_SIZE):
            self.draw_line(self.OFFSET_X, y, self.screen_size[0], y, self.grid_line)

    def drawTiles(self):
        """Draw the tiles"""
        for tile in self.city.tiles:
            self.draw_tile(tile.content.asset, tile.coords[0], tile.coords[1], tile.width, tile.height)

    def gameScene(self):
        """Render"""
        self.draw_rect(self.OFFSET_X, self.OFFSET_Y, self.screen_size[0] - self.OFFSET_X, self.screen_size[1] - self.OFFSET_Y, self.grass)
        self.drawTiles()

        if self.buildMode or self.destroyMode:
            self.drawGrid()
