import pygame
from renderer import Renderer
from ui import UI
from city import City


def main():
    running = True
    inGame = False
    selected_tile = None
    city = City(0, 50, 1000)
    renderer = Renderer('Sim City 2', city)
    ui = UI(renderer, city)
    clock = pygame.time.Clock()
    FPS = 30

    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.KMOD_LCTRL:
                    renderer.ddd =  not renderer.ddd
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for button in ui.buttons:
                    if button[2].collidepoint(event.pos):
                        if (button[0][2:4] == "ex"):
                            pygame.quit()
                            quit()
                        elif (button[0][:4] == "m_ng"):
                            inGame = True
                        elif (button[0][:5] == "m_con"):
                            inGame = True
                            loadedData = city.loadGame()
                            ui.ticks = loadedData[0]
                            ui.eY = loadedData[1]
                            ui.eM = loadedData[2]
                            ui.eD = loadedData[3]
                        elif (button[0][0:3] == "p_B" and renderer.buildMode):
                            ui.selectedBuilding = int(button[0][3:])
                        elif (button[0] == "p_bm" and not ui.isTimeStopped):
                            renderer.buildMode = not renderer.buildMode
                            renderer.destroyMode = False
                        elif (button[0] == "p_dm" and not ui.isTimeStopped):
                            renderer.destroyMode = not renderer.destroyMode
                            renderer.buildMode = False
                        elif (button[0] == "t_S") and not ui.isTimeStopped:
                            ui.tickRate *= 0.5
                        elif (button[0] == "t_F") and not ui.isTimeStopped:
                            ui.tickRate *= 2
                        elif (button[0] == "t_P"):
                            ui.isTimeStopped = not ui.isTimeStopped
                        elif (button[0] == "t_ng"):
                            city.save.clear()
                            ui.ticks = 0
                            inGame = False
                            renderer.buildMode = False
                            renderer.destroyMode = False
                            city.__init__(0, 100, 10000)
                        elif (button[0] == "t_sg"):
                            city.saveGame(ui.ticks, ui.eY, ui.eM, ui.eD)
                        elif (button[0] == "p_U" and selected_tile != None and selected_tile.content.getType() in ["residentialZone", "industrialZone", "serviceZone", "school", "universityZone"] and selected_tile.content.level < 3):
                            selected_tile.content.capacity *= 1.5
                            selected_tile.content.level += 1
                            city.money -= selected_tile.content.price / 2 + 25 * selected_tile.content.level
                            ui.updateZoneStats(selected_tile.content)
                        elif button[0] == "p_+":
                            city.taxRate *= 1.5
                        elif button[0] == "p_-" and city.taxRate > 0:
                            city.taxRate *= 0.5
                
                for idx, square in enumerate(city.grid):
                    if (square[1].collidepoint(event.pos)):
                        selected_tile = city.getSelectedTile(square[0][0],square[0][1])
                        if renderer.buildMode:
                            city.placeTile(ui.buildingNames[ui.selectedBuilding], square[0][0], square[0][1],idx)

                        if renderer.destroyMode:
                            if selected_tile != None:
                                city.destroyTile(selected_tile.content.getType(), square[0][0], square[0][1],idx)
                                
        renderer.clearScreen()
        if inGame:
            if (not ui.isTimeStopped ):
                ui.updateTime()
                ui.ticks += (clock.get_time() * ui.tickRate)

                if selected_tile != None and selected_tile.content.getType() in ["residentialZone", "industrialZone", "serviceZone", "school", "universityZone"]:
                    ui.updateZoneStats(selected_tile.content)
                else:
                    ui.clearZoneStats()
            ui.removeMenuButtons()
            renderer.clearScreen()
            renderer.gameScene()
            ui.draw()
        else:
            ui.menu()
        renderer.update()


if __name__ == '__main__':
    main()
