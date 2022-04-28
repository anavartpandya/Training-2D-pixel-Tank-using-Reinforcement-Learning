import pygame
import random
import math
import numpy as np
import cv2
from pygame.locals import *
pygame.font.init()

pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
for joystick in joysticks:
    print(joystick.get_name())

WIDTH, HEIGHT = 750, 750
COOLDOWN = 30
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tank Faceoff")
FPS = 60
mu = 0.005

# Load images
# Player
TANK = pygame.image.load("_2D MOTION (DISCRETE ACTION SPACE)\Assets_2D_dis\TANK.png")
#TANK = pygame.image.load("PyGame_tank_game\Assets\Background-black.png")
TANK = pygame.transform.scale(TANK, (int(TANK.get_width()/4), int(TANK.get_height()/4)))
#TANK = pygame.transform.scale(TANK, (100, 100))
# Enemy
TANK_ENEMY = pygame.image.load("_2D MOTION (DISCRETE ACTION SPACE)\Assets_2D_dis\TANK_ENEMY.png")
TANK_ENEMY = pygame.transform.scale(TANK_ENEMY, (int(TANK_ENEMY.get_width()/4), int(TANK_ENEMY.get_height()/4)))
# Lasers
RED_LASER = pygame.image.load("_2D MOTION (DISCRETE ACTION SPACE)\Assets_2D_dis\pixel_laser_red.png")
GREEN_LASER = pygame.image.load("_2D MOTION (DISCRETE ACTION SPACE)\Assets_2D_dis\pixel_laser_green.png")
# Background
BG = pygame.transform.scale(pygame.image.load("_2D MOTION (DISCRETE ACTION SPACE)\Assets_2D_dis\BG_Tank.jpg"), (WIDTH, HEIGHT))

class Laser:
    def __init__(self, x, y, img, hori_vel, ver_vel, angle):
        self.init_x = x
        self.init_y = y
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)
        self.hori_vel = hori_vel
        self.ver_vel = ver_vel
        self.angle = angle

    def draw(self, window):
        rect_ = self.img.get_rect(center=(self.x,self.y))
        rotated_laser_img_ = pygame.transform.rotate(self.img, self.angle)
        rect_ = rotated_laser_img_.get_rect(center = rect_.center)
        window.blit(rotated_laser_img_, rect_)

    def move(self, vel):
        self.y -= vel*(math.sin(math.radians(self.angle)))

        self.x += vel*(math.cos(math.radians(self.angle)))

    def off_screen(self, width):
        return not(self.y <= width and self.y >= 0)

    def collision(self, obj):
        return collide(self, obj)

    def range(self, range):
        if ((self.x - self.init_x)**2 + (self.y - self.init_y)**2) >= range**2:
            return True 
        else:
            return False 



class Ship:
    global COOLDOWN
    def __init__(self, x, y, angle = 0, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0
        self.angle = angle 
        self.current_xvel = 0
        self.current_yvel = 0

    def draw(self, window):
        rect = self.ship_img.get_rect(center=(self.x,self.y))
        rotated_ship_img = pygame.transform.rotate(self.ship_img, self.angle)
        rect = rotated_ship_img.get_rect(center = rect.center)
        window.blit(rotated_ship_img, rect)
        for laser in self.lasers:
            laser.draw(window)

    def move_lasers(self, vel, obj, range):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.range(range) == True:
                self.lasers.remove(laser)
            if laser.off_screen(WIDTH):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 25
                self.lasers.remove(laser)

    def cooldown(self):
        if self.cool_down_counter >= COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def shoot(self, hori_vel=0, ver_vel=0):
        if self.cool_down_counter == 0:
            laser = Laser(self.x, self.y, self.laser_img, hori_vel, ver_vel, self.angle)
            self.lasers.append(laser)
            self.cool_down_counter = 1

    def get_width(self):
        return self.ship_img.get_width()
    
    def get_height(self):
        return self.ship_img.get_height()

    def check_bound(self,x,y,radius,border_rect = WIN.get_rect()):        
        object_rect = pygame.Rect(x-radius, y-radius, radius*2, radius*2)
        object_rect.clamp_ip(border_rect)
        return object_rect.center

class Player(Ship):
    def __init__(self, x, y, angle = 0, health=100):
        super().__init__(x, y, angle, health)
        self.ship_img = TANK
        self.laser_img = GREEN_LASER
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health
        self.hit = False

    def move_lasers(self, vel, obj, range):
        self.cooldown()
        self.hit = False
        for laser in self.lasers:
            laser.move(vel)
            if laser.range(range) == True:
                self.lasers.remove(laser)
            elif laser.off_screen(WIDTH):
                self.lasers.remove(laser)
            else:
                if laser.collision(obj):
                    self.hit = True
                    obj.health -= 25
                    if laser in self.lasers:
                        self.lasers.remove(laser) 

    def draw(self, window):
        super().draw(window)
        self.healthbar(window)

    def healthbar(self, window):
        pygame.draw.rect(window, (255,0,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width(), 10))
        pygame.draw.rect(window, (0,255,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width() * (self.health/self.max_health), 10))

class Enemy(Ship):

    def __init__(self, x, y, angle, health=100):
            super().__init__(x, y, angle, health)
            self.ship_img = TANK_ENEMY
            self.laser_img = RED_LASER
            self.mask = pygame.mask.from_surface(self.ship_img)
            self.max_health = health
            self.steps_x = 0
            self.steps_y = 0
            self.x_count = 0 
            self.vel = 0.5
            self.sign_x = None
            self.sign_y = None
            self.past_x = x
            self.past_y = y
            self.mu_e = 0.005
            self.value = 0
            self.err_angle = random.randrange(-7,7)
            self.flag = 0
            self.motiv = random.randrange(500,2000)
            self.motiv_ = 0
            self.diffe_x = 0
            self.diffe_y = 0
            self.update_x = 0
            self.update_y = 0
            self.hit = False

    def move_lasers(self, vel, obj, range):
        self.hit = False
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.range(range) == True:
                self.lasers.remove(laser)
            elif laser.off_screen(WIDTH):
                self.lasers.remove(laser)
            else:
                if laser.collision(obj):
                    self.hit = True
                    obj.health -= 25
                    if laser in self.lasers:
                        self.lasers.remove(laser)


    def move(self, player):
        target_angle = math.degrees(math.atan(abs((self.y - player.y)/(abs(self.x-player.x) + 0.00001))))
        if self.x < player.x:
            if self.y >= player.y:
                target_angle = target_angle
            if self.y < player.y:
                target_angle = -target_angle
        if self.x > player.x:
            if self.y >= player.y:
                target_angle = 180 - target_angle
            if self.y < player.y:
                target_angle = 180 + target_angle
        
        
        self.angle = target_angle + self.err_angle

        self.motiv_ += 1

        if self.motiv_ == self.motiv:
            self.motiv_ -= 1
            value_target = 0.05
            if self.value == value_target:
                value_update = 0
            else: 
                value_update = 0.002
            self.value += value_update
            if self.flag == 1:
                self.err_angle = random.randrange(-7,7)
                self.motiv = random.randrange(10,1000)
        
        if ((player.x - self.x)**2 + (player.y - self.y)**2)**0.5 < 350:
            self.value = 0
            self.mu_e = 0.05
            self.flag += 1
            self.motiv_ = 0

        else:
            self.flag = 0

        self.update_x = self.value*(math.cos(math.radians(self.angle)))
        self.update_y = self.value*(math.sin(math.radians(self.angle)))

        if  (WIDTH-15 < self.x < WIDTH) or (0 < self.x < 15) or (HEIGHT-15 < self.y < HEIGHT) or (0 < self.y < 15):
            self.x = self.past_x
            self.y = self.past_y

        self.y -= self.update_y

        self.x += self.update_x


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

class Open_Ai:
    global COOLDOWN
    def __init__(self):
    
        self.run = True
        self.FPS = 60
        self.level = 1

        self.update_y = 0
        self.update_x = 0
        self.update_angle = 0

        self.eupdate_y = 0
        self.eupdate_x = 0
        self.eupdate_angle = 0

        global mu

        self.main_font = pygame.font.SysFont("comicsans", 50)
        self.lost_font = pygame.font.SysFont("comicsans", 60)
        self.win_font = pygame.font.SysFont("comicsans", 80)

        self.player_vel = 5
        self.enemy_vel = 1                                                     
        self.laser_vel = 50

        self.event_val = 0
        while True:
            self.player_initx = random.randrange(80,WIDTH - 80)
            self.player_inity = random.randrange(80,WIDTH - 80)
            self.enemy_initx = random.randrange(80,HEIGHT - 80)
            self.enemy_inity = random.randrange(80,HEIGHT - 80)
            if ((self.player_initx - self.enemy_initx)**2 + (self.player_inity - self.enemy_inity)**2)**0.5 > (WIDTH + HEIGHT)/4:
                break
        self.player = Player(self.player_initx, self.player_inity, angle = random.randrange(0,360))
        self.enemy = Enemy(self.enemy_initx, self.enemy_inity, angle = random.randrange(0,360))
        self.clock = pygame.time.Clock()

        self.past_player_x = self.player.x
        self.past_player_y = self.player.y
    
        self.past_enemy_x = self.enemy.x
        self.past_enemy_y = self.enemy.y

        self.lost = False
        self.lost_count = 0

        self.win = False 
        self.win_count = 0

        self.diff_y = 0
        self.diff_x = 0
    
        self.diffe_y = 0
        self.diffe_x = 0

        self.player_current_x_pos, self.player_current_y_pos = self.player.x, self.player.y
        self.enemy_current_x_pos, self.enemy_current_y_pos = self.enemy.x, self.enemy.y   


    def action(self,action): # action: [acceleration,steer,shoot,break] 
        global COOLDOWN

        player_last_x_pos, player_last_y_pos = self.player_current_x_pos, self.player_current_y_pos
        self.player_current_x_pos, self.player_current_y_pos = self.player.x, self.player.y
        current_player_x_vel, current_player_y_vel = (self.player_current_x_pos - player_last_x_pos), (self.player_current_y_pos - player_last_y_pos)

        enemy_last_x_pos, enemy_last_y_pos = self.enemy_current_x_pos, self.enemy_current_y_pos
        self.enemy_current_x_pos, self.enemy_current_y_pos = self.enemy.x, self.enemy.y
        current_enemy_x_vel, current_enemy_y_vel = (self.enemy_current_x_pos - enemy_last_x_pos), (self.enemy_current_y_pos - enemy_last_y_pos) 
        #self.clock.tick(FPS)
        #self.redraw_window1()


        if self.player.health <= 0:
            self.lost = True
        
        if collide(self.enemy, self.player):
            self.player.health = 0
            self.lost = True
        
        if self.enemy.health <= 0:
            self.win = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        if action == 4:
            self.player.shoot(current_player_x_vel, current_player_y_vel) 
        if action == 2:
            self.update_angle = 0.5
        if action == 3:
            self.update_angle = -0.5            

        self.player.angle -= self.update_angle
        if action == 0:
            self.update_y = (2)*(math.sin(math.radians(self.player.angle)))
            self.update_x = (2)*(math.cos(math.radians(self.player.angle)))
        
        if action == 1:
            self.update_y = -(2)*(math.sin(math.radians(self.player.angle)))
            self.update_x = -(2)*(math.cos(math.radians(self.player.angle)))
               
        if  (WIDTH-15 < self.player.x < WIDTH) or (0 < self.player.x < 15) or (HEIGHT-15 < self.player.y < HEIGHT) or (0 < self.player.y < 15):
            self.player.x = self.past_player_x
            self.player.y = self.past_player_y

        self.past_player_y = self.player.y
        self.player.y = self.past_player_y - self.update_y

        self.past_player_x = self.player.x
        self.player.x = self.past_player_x + self.update_x

        if ((self.player.x - self.enemy.x)**2 + (self.player.y - self.enemy.y)**2)**0.5 < 400:
            if random.randrange(0, int(120/(self.level))) == 1:
                self.enemy.shoot(current_enemy_x_vel, current_enemy_y_vel)

        self.player.move_lasers(self.laser_vel, self.enemy, 400)
        self.enemy.move_lasers(self.laser_vel, self.player, 400)
        self.enemy.move(self.player)   

    def observe(self):
        #return state

        target_angle_ = math.degrees(math.atan(abs((self.player.y - self.enemy.y)/(abs(self.player.x-self.enemy.x) + 0.00001))))
        if self.player.x < self.enemy.x:
            if self.player.y >= self.enemy.y:
                target_angle_ = target_angle_
            if self.player.y < self.enemy.y:
                target_angle_ = -target_angle_
        if self.player.x > self.enemy.x:
            if self.player.y >= self.enemy.y:
                target_angle_ = 180 - target_angle_
            if self.player.y < self.enemy.y:
                target_angle_ = 180 + target_angle_
        
        self.player_coord = (int(self.player.x), int(self.player.y))
        self.enemy_coord = (int(self.enemy.x), int(self.enemy.y))

        state = np.array([self.player_coord[0], self.player_coord[1], self.player.angle, self.player.health, self.player.hit, target_angle_, self.enemy_coord[0], self.enemy_coord[1], self.enemy.angle, self.enemy.health, self.enemy.hit])

        return state    

    def evaluate(self):         
        reward = 0 
        obs = self.observe()

        if self.lost == True:
            reward -= 100000
        if (obs[2] >= obs[5]-15) and (obs[2] <= obs[5]+15):
            reward += 10*(15-abs(obs[2]-obs[5]))
        if self.player.hit == True:
            reward += 1000
        if self.enemy.hit == True:
            reward -= 1000
        if self.win == True:
            print(True)
            reward += (self.player.health)*100
        return reward
        

    
    def is_done(self):
        if (self.lost == True) or (self.win == True):       
            return True 
        else:
            return False       


    def redraw_window1(self):
        WIN.blit(BG, (0,0))
        self.enemy.draw(WIN)
        self.player.draw(WIN)
        if self.lost:
            lost_label = self.lost_font.render("You Lost!!", 1, (255,255,255))
            WIN.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2, 350))
        if self.win:
            win_label = self.win_font.render("You Won!!", 1, (255,255,255))
            WIN.blit(win_label, (WIDTH/2 - win_label.get_width()/2, 350))

        pygame.display.update()

    def view(self):
        self.redraw_window1()
        self.clock.tick(self.FPS)