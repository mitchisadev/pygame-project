import pygame as pyg
import sys
pyg.init()

display = pyg.display.set_mode((800, 600)) #makes the window that the game is on
clock = pyg.time.Clock()
favicon = pyg.image.load("favicon.png")
pyg.display.set_icon(favicon)

class Player:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def main(self, display):
        pyg.draw.rect(display, "white", (self.x, self.y, self.width, self.height))

player = Player(400, 300, 32, 32)
    
running = True
while running:
    display.fill("black")

    for event in pyg.event.get():
        if event.type == pyg.QUIT:
            sys.exit()
            pyg.QUIT
        player.main(display)

    clock.tick(60)
    pyg.display.update()