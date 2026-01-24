import pygame
import os
import random
import math
from settings import *
from weapons import WeaponSystem

GAME_FOLDER = os.path.dirname(__file__)
ASSETS_FOLDER = os.path.join(GAME_FOLDER, 'assets')

class Player(pygame.sprite.Sprite):
    def __init__(self, model_name):
        super().__init__()
        if model_name in AIRCRAFT_DATA: self.data = AIRCRAFT_DATA[model_name]
        else: self.data = AIRCRAFT_DATA['Gripen F-39E']
        self.prefix = self.data['prefix']
        
        base_w = int(70 * SCALE * self.data.get('scale', 1.0))
        base_h = int(90 * SCALE * self.data.get('scale', 1.0))
        self.base_size = (base_w, base_h)
        
        self.sprites = {}
        self.has_images = False
        try:
            self.sprites['neutral'] = self.load_and_scale(f"{self.prefix}_neutral.png")
            self.sprites['left'] = self.load_and_scale(f"{self.prefix}_left.png")
            self.sprites['right'] = self.load_and_scale(f"{self.prefix}_right.png")
            self.sprites['shoot'] = self.load_and_scale(f"{self.prefix}_shoot.png")
            self.has_images = True
        except: self.has_images = False

        if self.has_images: 
            self.original_image = self.sprites['neutral']
        else:
            self.original_image = pygame.Surface(self.base_size, pygame.SRCALPHA)
            color = (100, 100, 120)
            if self.prefix == 'b2':
                pygame.draw.polygon(self.original_image, (30, 30, 30), [(base_w//2, 0), (base_w, base_h//2), (base_w//2, base_h-10), (0, base_h//2)])
            elif self.prefix == 'b52':
                pygame.draw.rect(self.original_image, color, (base_w//2 - 5, 0, 10, base_h))
                pygame.draw.rect(self.original_image, color, (0, base_h//3, base_w, 10))
            else: 
                pygame.draw.polygon(self.original_image, color, [(base_w//2, 0), (base_w, base_h), (0, base_h)])

        self.image = self.original_image
        self.rect = self.image.get_rect(center=(MAP_WIDTH // 2, MAP_HEIGHT // 2))
        
        self.hp = self.data['hp']
        self.max_hp = self.data['hp']
        self.speed = self.data['speed'] * SCALE
        
        # --- CARREGA O ARSENAL (LISTA DE ARMAS) ---
        my_loadout = self.data.get('loadout', ['VULCAN'])
        self.weapons = WeaponSystem(my_loadout)
        
        self.vel_x, self.vel_y = 0, 0
        self.angle = 0 
        self.is_shooting, self.shoot_timer = False, 0
        self.powerup_timer, self.powered_up = 0, False

    def load_and_scale(self, filename):
        path = os.path.join(ASSETS_FOLDER, filename)
        img = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(img, self.base_size)
    def update_input(self, axis_x, axis_y):
        self.vel_x = axis_x * self.speed; self.vel_y = axis_y * self.speed
    def trigger_shoot_anim(self):
        self.is_shooting = True; self.shoot_timer = pygame.time.get_ticks()
    def enable_powerup(self):
        self.powered_up = True; self.powerup_timer = pygame.time.get_ticks(); self.hp = min(self.hp + 20, self.max_hp)
    def rotate(self):
        if abs(self.vel_x) < 0.1 and abs(self.vel_y) < 0.1: return
        base_img = self.sprites['neutral'] if self.has_images else self.original_image
        if self.has_images and (abs(self.vel_x) > 0.5 and abs(self.vel_y) > 0.5):
            base_img = self.sprites['left'] if self.vel_x < 0 else self.sprites['right']
        self.angle = math.degrees(math.atan2(-self.vel_y, self.vel_x)) - 90
        self.image = pygame.transform.rotate(base_img, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
    def update(self):
        self.rect.x += self.vel_x; self.rect.y += self.vel_y
        if self.rect.left < 0: self.rect.left = 0
        if self.rect.right > MAP_WIDTH: self.rect.right = MAP_WIDTH
        if self.rect.top < 0: self.rect.top = 0
        if self.rect.bottom > MAP_HEIGHT: self.rect.bottom = MAP_HEIGHT
        self.rotate()
        if self.powered_up and pygame.time.get_ticks() - self.powerup_timer > 5000: self.powered_up = False

class BigMap(pygame.sprite.Sprite):
    def __init__(self, map_file):
        super().__init__()
        bg_path = os.path.join(ASSETS_FOLDER, map_file)
        try:
            self.image = pygame.image.load(bg_path).convert()
            if self.image.get_size() != (MAP_WIDTH, MAP_HEIGHT): self.image = pygame.transform.scale(self.image, (MAP_WIDTH, MAP_HEIGHT))
        except: self.image = pygame.Surface((MAP_WIDTH, MAP_HEIGHT)); self.image.fill((194, 178, 128)) 
        self.rect = self.image.get_rect(topleft=(0, 0))

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, model_name="Gripen F-39E"):
        super().__init__()
        if model_name in AIRCRAFT_DATA: self.data = AIRCRAFT_DATA[model_name]
        else: self.data = AIRCRAFT_DATA['Gripen F-39E']
        self.prefix = self.data['prefix']
        base_w = int(70 * SCALE * self.data.get('scale', 1.0)); base_h = int(90 * SCALE * self.data.get('scale', 1.0))
        self.base_size = (base_w, base_h)
        try:
            path = os.path.join(ASSETS_FOLDER, f"{self.prefix}_neutral.png")
            img = pygame.image.load(path).convert_alpha()
            self.original_image = pygame.transform.scale(img, self.base_size)
        except: self.original_image = pygame.Surface(self.base_size, pygame.SRCALPHA); pygame.draw.polygon(self.original_image, (200, 50, 50), [(base_w//2, base_h), (base_w, 0), (0, 0)])
        self.image = self.original_image; self.rect = self.image.get_rect(center=(x, y))
        self.hp = self.data['hp'] * 0.4; self.speed = (self.data['speed'] * 0.5) * SCALE 
        
        # Inimigo pega a segunda arma (geralmente míssil) para atirar em você
        loadout = self.data.get('loadout', ['VULCAN'])
        self.missile_type = loadout[1] if len(loadout) > 1 else loadout[0]
        
        self.last_shot_time = pygame.time.get_ticks(); self.shot_delay = random.randint(2000, 4000)
        self.vel_x, self.vel_y = 0, 0; self.change_dir_timer = 0; self.angle = 0; self.pick_new_direction()
    def pick_new_direction(self):
        while True:
            dir_x = random.choice([-1, 0, 1]); dir_y = random.choice([-1, 0, 1])
            if dir_x != 0 or dir_y != 0: break
        self.vel_x = dir_x * self.speed; self.vel_y = dir_y * self.speed
        self.angle = math.degrees(math.atan2(-self.vel_y, self.vel_x)) - 90
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
    def check_fire(self, player_rect, current_time):
        dx = player_rect.centerx - self.rect.centerx; dy = player_rect.centery - self.rect.centery
        dist = math.hypot(dx, dy)
        if dist < 600 and current_time - self.last_shot_time > self.shot_delay:
            self.last_shot_time = current_time; self.shot_delay = random.randint(2000, 4000)
            return True, math.degrees(math.atan2(-dy, dx))
        return False, 0
    def update(self):
        self.rect.x += self.vel_x; self.rect.y += self.vel_y
        if self.rect.left < 0 or self.rect.right > MAP_WIDTH: self.vel_x *= -1; self.pick_new_direction()
        if self.rect.top < 0 or self.rect.bottom > MAP_HEIGHT: self.vel_y *= -1; self.pick_new_direction()
        self.change_dir_timer += 1
        if self.change_dir_timer > 100: self.change_dir_timer = 0; self.pick_new_direction()

# Classes Explosion, MassiveExplosion, PowerUp, Cloud (MANTIDAS IGUAIS AO MAIN)
class Explosion(pygame.sprite.Sprite):
    def __init__(self, center):
        super().__init__()
        self.size = int(60 * SCALE)
        self.image = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=center)
        self.timer = 15 
    def update(self):
        self.timer -= 1
        if self.timer % 3 == 0:
            self.image.fill((0,0,0,0))
            pygame.draw.circle(self.image, (255, random.randint(100,255), 0), (self.size//2, self.size//2), (self.size//2) * (self.timer/15))
        if self.timer <= 0: self.kill()

class MassiveExplosion(pygame.sprite.Sprite):
    def __init__(self, center):
        super().__init__()
        self.max_size = int(250 * SCALE)
        self.image = pygame.Surface((self.max_size, self.max_size), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=center)
        self.timer = 0
        self.duration = 20
    def update(self):
        self.timer += 1
        self.image.fill((0,0,0,0))
        progress = self.timer / self.duration
        current_radius = int((self.max_size // 2) * progress)
        pygame.draw.circle(self.image, (255, 255, 255, 100), (self.max_size//2, self.max_size//2), current_radius, 5)
        inner_radius = int(current_radius * 0.8)
        color = (255, random.randint(50, 150), 0)
        pygame.draw.circle(self.image, color, (self.max_size//2, self.max_size//2), inner_radius)
        if self.timer >= self.duration: self.kill()

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, center):
        super().__init__()
        self.size = int(25 * SCALE)
        self.image = pygame.Surface((self.size, self.size))
        self.image.fill(CYAN); pygame.draw.rect(self.image, WHITE, (0,0,self.size,self.size), 2)
        font = pygame.font.SysFont('arial', int(15*SCALE), bold=True)
        txt = font.render("P", True, BLACK)
        self.image.blit(txt, (self.size//2 - txt.get_width()//2, self.size//2 - txt.get_height()//2))
        self.rect = self.image.get_rect(center=center)

class Cloud(pygame.sprite.Sprite):
    def __init__(self, x=None, y=None):
        super().__init__()
        w = random.randint(int(100*SCALE), int(300*SCALE)); h = int(w * 0.6)
        self.image = pygame.Surface((w, h), pygame.SRCALPHA)
        for _ in range(5): pygame.draw.circle(self.image, (255, 255, 255, 50), (random.randint(0, w), random.randint(0, h)), random.randint(20, 60))
        self.rect = self.image.get_rect()
        if x: self.rect.x = x
        else: self.rect.x = random.randint(0, MAP_WIDTH)
        if y: self.rect.y = y
        else: self.rect.y = random.randint(0, MAP_HEIGHT)
