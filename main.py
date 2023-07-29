import pygame as pyg
import sys
import math
import random

pyg.init()

display = pyg.display.set_mode((800, 800)) #makes the window that the game is on
clock = pyg.time.Clock()

player_walk_cycle = [pyg.image.load("player_walk_0.png"), pyg.image.load("player_walk_1.png"), pyg.image.load("player_walk_2.png"), pyg.image.load("player_walk_3.png")]

player_weapon = pyg.image.load("shotgun.png").convert()
player_weapon.set_colorkey("white")

#bar at top of window stuff
#title of window
pyg.display.set_caption("mygame")

#image of window
favicon = pyg.image.load("favicon.png")
pyg.display.set_icon(favicon)

class Player:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.animation_count = 0
        self.moving_right = False
        self.moving_left = False

    def handle_weapons(self, display):
        mouse_x, mouse_y = pyg.mouse.get_pos()

        #calculates angle to point gun at
        rel_x, rel_y = mouse_x - player.x, mouse_y - player.y
        angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)

        player_weapon_copy = pyg.transform.rotate(player_weapon, angle)

        display.blit(player_weapon_copy, (self.x + 15 - int(player_weapon_copy.get_width() / 2), self.y + 25 - int(player_weapon_copy.get_height() / 2)))

        
    def main(self, display): #ladies and gentlemen, the player.
        if self.animation_count + 1 >= 16:
            self.animation_count = 0

        self.animation_count += 1
        
        if self.moving_right:
            display.blit(pyg.transform.scale(player_walk_cycle[self.animation_count // 4], (32, 42)), (self.x, self.y))

        elif self.moving_left:
            display.blit(pyg.transform.scale(pyg.transform.flip(player_walk_cycle[self.animation_count // 4], True, False), (32, 42)), (self.x, self.y))

        else:
             display.blit(pyg.transform.scale(player_walk_cycle[0], (32, 42)), (self.x, self.y))

        self.handle_weapons(display)
        
        self.moving_right = False
        self.moving_left = False

class Slime:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.animation_cycle = [pyg.image.load("slime_animation_0.png"), pyg.image.load("slime_animation_1.png"), pyg.image.load("slime_animation_2.png"), pyg.image.load("slime_animation_3.png")]
        self.animation_count = 0
        self.reset_offset = 0
        self.offset_x = random.randrange(-150, 150)
        self.offset_y = random.randrange(-150, 150)

    def main(self, display):
        if self.animation_count + 1 >= 16:
            self.animation_count = 0
        self.animation_count += 1

        if self.reset_offset == 0:
            self.offset_x = random.randrange(-150, 150)
            self.offset_y = random.randrange(-150, 150)
            self.reset_offset = random.randrange(120, 150)
        else:
            self.reset_offset -= 1
        
        if player.x + self.offset_x > self.x - display_scroll[0]: #player on right side of enemy
            self.x += 1
        elif player.x + self.offset_x < self.x - display_scroll[0]: #player on left side of enemy
            self.x -= 1

        if player.y + self.offset_y > self.y - display_scroll[1]: #player above enemy
            self.y += 1
        elif player.y + self.offset_y < self.y - display_scroll[1]: #player below enemy
            self.y -= 1

        display.blit(pyg.transform.scale(self.animation_cycle[self.animation_count // 4], (32, 30)), (self.x - display_scroll[0], self.y - display_scroll[1]))



class PlayerBullet:
    def __init__(self, x, y, mouse_x, mouse_y):
        self.x = x
        self.y = y
        self.mouse_x = mouse_x
        self.mouse_y = mouse_y
        self.speed = 15 #hardcoded temporarily
        self.angle = math.atan2(y - mouse_y, x - mouse_x)
        self.x_vel = math.cos(self.angle) * self.speed #i would like to thank ScriptLine Studios on youtube for this part of this code, cause what person without 200iq would think
        self.y_vel = math.sin(self.angle) * self.speed #of using geometry lol
    
    def main(self, display):
        self.x -= int(self.x_vel)
        self.y -= int(self.y_vel)

        pyg.draw.circle(display, "white", (self.x, self.y), 5)
        

player = Player(400, 400, 64, 64)
    
display_scroll = [0, 0] #1st represents the x, and the 2nd represents y

player_bullets = []
enemies = [Slime(400, 300)]

while True:
    display.fill((25, 165, 85))

    mouse_x, mouse_y = pyg.mouse.get_pos()

    for event in pyg.event.get():
        if event.type == pyg.QUIT:
            sys.exit()
            pyg.quit()
        
        if event.type == pyg.MOUSEBUTTONDOWN: #if mouse is clicked
            if event.button == 1: #if mouse1 (left click) is pressed
                player_bullets.append(PlayerBullet(player.x + 20, player.y + 20, mouse_x, mouse_y))


    
    #movement (moving map around player)
    keys = pyg.key.get_pressed()

    pyg.draw.rect(display, "white", (100 - display_scroll[0], 100 - display_scroll[1], 16, 16))

    if keys[pyg.K_a]: #if "A" is pressed
        display_scroll[0] -= 5
        player.moving_left = True

        for bullet in player_bullets: #move bullet for illusion of movement
            bullet.x +=5

    if keys[pyg.K_d]: #if "D" is pressed
        display_scroll[0] += 5
        player.moving_right = True

        for bullet in player_bullets: #move bullet for illusion of movement
            bullet.x -=5

    if keys[pyg.K_w]: #if "W" is pressed
        display_scroll[1] -= 5
        player.moving_right = True

        for bullet in player_bullets: #move bullet for illusion of movement
            bullet.y +=5

    if keys[pyg.K_s]: #if "S" is pressed
        display_scroll[1] += 5
        player.moving_right = True

        for bullet in player_bullets: #move bullet for illusion of movement
            bullet.y -=5


    player.main(display)

    for bullet in player_bullets:
        bullet.main(display)
    
    for enemy in enemies:
        enemy.main(display)

    clock.tick(60) #game runs 60fps
    pyg.display.update() #update display so shit actually happens