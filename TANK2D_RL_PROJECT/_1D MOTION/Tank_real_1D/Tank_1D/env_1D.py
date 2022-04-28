import pygame
import random
import numpy as np

pygame.font.init()

WIDTH, HEIGHT = 750, 750
COOLDOWN = 30
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tank Faceoff")

# Load images
# Player
TANK = pygame.image.load("_1D MOTION\Assets_1D\TANK.png")
TANK = pygame.transform.scale(TANK, (int(TANK.get_width()/4), int(TANK.get_height()/4)))
# Enemy
TANK_ENEMY = pygame.image.load("_1D MOTION\Assets_1D\TANK_ENEMY.png")
TANK_ENEMY = pygame.transform.scale(TANK_ENEMY, (int(TANK_ENEMY.get_width()/4), int(TANK_ENEMY.get_height()/4)))
# Lasers
RED_LASER = pygame.image.load("_1D MOTION\Assets_1D\pixel_laser_red.png")
GREEN_LASER = pygame.image.load("_1D MOTION\Assets_1D\pixel_laser_green.png")
# Background
BG = pygame.transform.scale(pygame.image.load("_1D MOTION\Assets_1D\BG_Tank.jpg"), (WIDTH, HEIGHT))

class Laser:
    def __init__(self, x, y, img, hori_vel, ver_vel):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)
        #self.hori_vel = hori_vel
        self.ver_vel = ver_vel

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self, vel):
        #self.y += self.ver_vel 
        self.x += vel 

    def off_screen(self, width):
        return not(self.y <= width and self.y >= 0)

    def collision(self, obj):
        return collide(self, obj)


class Ship:
    global COOLDOWN
    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0
     
    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)

    def move_lasers(self, vel, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(WIDTH):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 20
                self.lasers.remove(laser)

    def cooldown(self):
        if self.cool_down_counter >= COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def shoot(self, hori_vel=0, ver_vel=0):
        if self.cool_down_counter == 0:
            laser = Laser(self.x, self.y, self.laser_img, hori_vel, ver_vel)
            self.lasers.append(laser)
            self.cool_down_counter = 1

    def get_width(self):
        return self.ship_img.get_width()
    
    def get_height(self):
        return self.ship_img.get_height()

class Player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_img = TANK
        self.laser_img = GREEN_LASER
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health

    def move_lasers(self, vel, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(WIDTH):
                self.lasers.remove(laser)
            else:
                if laser.collision(obj):
                    obj.health -= 20
                    if laser in self.lasers:
                        self.lasers.remove(laser) 

    def draw(self, window):
        super().draw(window)
        self.healthbar(window)

    def healthbar(self, window):
        pygame.draw.rect(window, (255,0,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width(), 10))
        pygame.draw.rect(window, (0,255,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width() * (self.health/self.max_health), 10))

class Enemy(Ship):

    def __init__(self, x, y, health=100):
            super().__init__(x, y, health)
            self.ship_img = TANK_ENEMY
            self.laser_img = RED_LASER
            self.mask = pygame.mask.from_surface(self.ship_img)
            self.max_health = health
            self.steps_x = 0
            self.steps_y = 0
            self.timer = 0 
            self.sign_x = None
            self.sign_y = None

    def move_lasers(self, vel, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(WIDTH):
                self.lasers.remove(laser)
            else:
                if laser.collision(obj):
                    obj.health -= 20
                    if laser in self.lasers:
                        self.lasers.remove(laser)

    def move(self, obj, vel, game_level):

        if self.y not in range(obj.y-20,obj.y+20):
            #self.y += vel
            if self.steps_y == 0:
                self.steps_y = HEIGHT
                self.sign_y = random.choice((1,-1))

            if self.steps_y != 0:
                if self.timer > random.randrange(0,80,20):
                    self.y += self.sign_y*vel
                    self.steps_y = self.steps_y - 1
                self.timer += 1 
            if self.y > HEIGHT - self.ship_img.get_height() - vel:
                self.y = HEIGHT - self.ship_img.get_height() -vel
                self.sign_y = -self.sign_y
            if self.y < vel:
                self.y = vel
                self.sign_y = -self.sign_y
        if self.y in range(obj.y-15, obj.y+15):
            self.steps_y = 0
                
  
    def draw(self, window):
        super().draw(window)
        self.healthbar(window)

    def healthbar(self, window):
        pygame.draw.rect(window, (255,0,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width(), 10))
        pygame.draw.rect(window, (0,255,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width() * (self.health/self.max_health), 10))

def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (int(offset_x), int(offset_y))) != None

def main():
    global COOLDOWN
    run = True
    FPS = 60
    level = 1

    main_font = pygame.font.SysFont("comicsans", 50)
    lost_font = pygame.font.SysFont("comicsans", 60)
    win_font = pygame.font.SysFont("comicsans", 80)

    player_vel = 5
    enemy_vel = 5                                                    
    laser_vel = 10

    player = Player(630, 300)
    enemy = Enemy(0,300)
    clock = pygame.time.Clock()

    lost = False
    lost_count = 0

    win = False 
    win_count = 0

    player_current_x_pos, player_current_y_pos = player.x, player.y
    enemy_current_x_pos, enemy_current_y_pos = enemy.x, enemy.y

    def redraw_window():
        WIN.blit(BG, (0,0))
        # draw text
        #level_label = main_font.render(f"Level: {level}", 1, (255,255,255))

        #WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))

        enemy.draw(WIN)
        player.draw(WIN)
        pygame.draw.aaline(WIN, (0,0,0), (WIDTH / 2, 0),(WIDTH / 2, HEIGHT))
        if lost:
            lost_label = lost_font.render("You Lost!!", 1, (255,255,255))
            WIN.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2, 350))
        if win:
            win_label = win_font.render("You Won!!", 1, (255,255,255))
            WIN.blit(win_label, (WIDTH/2 - win_label.get_width()/2, 350))

        pygame.display.update()

class Open_Ai:
    
    global COOLDOWN
    def __init__(self):

        self.player = Player(630, random.randrange(0,HEIGHT-50,5))
        self.enemy = Enemy(0,random.randrange(0,HEIGHT-50,5))
        self.clock = pygame.time.Clock()

        self.run = True
        self.FPS = 60
        self.level = 1

        self.main_font = pygame.font.SysFont("comicsans", 50)
        self.lost_font = pygame.font.SysFont("comicsans", 60)
        self.win_font = pygame.font.SysFont("comicsans", 80)

        self.player_vel = 5
        self.enemy_vel = 5                                                     
        self.laser_vel = 50

        self.lost = False
        self.lost_count = 0

        self.win = False 
        self.win_count = 0

        self.player_current_health = self.player.health
        self.enemy_current_health = self.enemy.health

        self.player_current_x_pos, self.player_current_y_pos = self.player.x, self.player.y
        self.enemy_current_x_pos, self.enemy_current_y_pos = self.enemy.x, self.enemy.y

        self.shoot_status = False

    def action(self,action): # [0:NOOP, 1:UP, 2:DOWN, 3:FIRE] 
        global COOLDOWN
        self.player_last_x_pos, self.player_last_y_pos = self.player_current_x_pos, self.player_current_y_pos
        self.player_current_x_pos, self.player_current_y_pos = self.player.x, self.player.y
        self.current_player_x_vel, self.current_player_y_vel = (self.player_current_x_pos - self.player_last_x_pos), (self.player_current_y_pos - self.player_last_y_pos)

        self.enemy_last_x_pos, self.enemy_last_y_pos = self.enemy_current_x_pos, self.enemy_current_y_pos
        self.enemy_current_x_pos, self.enemy_current_y_pos = self.enemy.x, self.enemy.y
        self.current_enemy_x_vel, self.current_enemy_y_vel = (self.enemy_current_x_pos - self.enemy_last_x_pos), (self.enemy_current_y_pos - self.enemy_last_y_pos) 

        if action == 0: 
           pass 
        if action == 1:
            if self.player.y - self.player_vel > 0: # up
                self.player.y -= self.player_vel
        if action == 2:
            if self.player.y + self.player_vel + self.player.get_height() + 15 < HEIGHT: # down
                self.player.y += self.player_vel  
        if action == 3:
            self.player.shoot(self.current_player_x_vel, self.current_player_y_vel)
        
        self.enemy.move_lasers(self.laser_vel, self.player)
        self.player.move_lasers(-self.laser_vel, self.enemy)
        self.enemy.move(self.player, self.enemy_vel, self.level)

        if self.enemy.y in range(self.player.y-50, self.player.y+50):
            self.enemy.shoot(self.current_enemy_x_vel, self.current_enemy_y_vel)   
        
        if self.enemy.health <= 0:
            self.win = True
   
        if self.player.health <= 0:
            self.lost = True
            

    def observe(self):
        #return state
        self.player_loc = self.player.y
        if self.enemy.y in range(self.player.y-500, self.player.y+500):
            self.enemy_loc = self.enemy.y
        else:
            self.enemy_loc = random.choice((0,HEIGHT))

        state = np.array([self.player_loc, self.player.health, self.enemy_loc, self.enemy.health])
        return state    

    def evaluate(self):
        reward = 0

        reward -= self.enemy.health/100
        if self.player.health <= 0:
            reward -= 10000
        if self.enemy.health <= 0:  
            reward += self.player.health 
                
        return reward
    
    def is_done(self):
        if self.lost == True or self.win == True:
            return True
        else:
            return False

    def redraw_window1(self):
        WIN.blit(BG, (0,0))
        # draw text
        level_label = self.main_font.render(f"Level: {self.level}", 1, (255,255,255))

        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))

        self.enemy.draw(WIN)
        self.player.draw(WIN)
        pygame.draw.aaline(WIN, (0,0,0), (WIDTH / 2, 0),(WIDTH / 2, HEIGHT))


        pygame.display.update()

    def view(self):
        self.redraw_window1()
        self.clock.tick(self.FPS)
