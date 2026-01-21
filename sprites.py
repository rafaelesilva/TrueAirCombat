import pygame
import os
import random
from settings import *
from weapons import WeaponSystem

# --- CORREÇÃO: Aponta para a pasta 'assets' ---
GAME_FOLDER = os.path.dirname(__file__)
ASSETS_FOLDER = os.path.join(GAME_FOLDER, 'assets') # Agora ele sabe que existe uma pasta

class Player(pygame.sprite.Sprite):
    def __init__(self, model_name):
        super().__init__()
        if model_name in AIRCRAFT_DATA:
            self.data = AIRCRAFT_DATA[model_name]
        else:
            self.data = AIRCRAFT_DATA['Gripen F-39E']
            
        self.model_name = model_name
        self.prefix = self.data['prefix']
        
        # Define o tamanho
        base_w = int(70 * SCALE * self.data.get('scale_factor', 1.0))
        base_h = int(90 * SCALE * self.data.get('scale_factor', 1.0))
        self.base_size = (base_w, base_h)
        
        self.sprites = {}
        self.has_images = False
        
        # --- CARREGAMENTO DE IMAGEM ---
        try:
            # Agora busca dentro de ASSETS_FOLDER
            self.sprites['neutral'] = self.load_and_scale(f"{self.prefix}_neutral.png")
            self.sprites['left'] = self.load_and_scale(f"{self.prefix}_left.png")
            self.sprites['right'] = self.load_and_scale(f"{self.prefix}_right.png")
            self.sprites['shoot'] = self.load_and_scale(f"{self.prefix}_shoot.png")
            self.has_images = True
            self.image = self.sprites['neutral']
        except Exception as e:
            print(f"AVISO: Imagens não encontradas em 'assets' para {self.prefix} ({e}).")
            self.has_images = False
            self.image = pygame.Surface(self.base_size, pygame.SRCALPHA)
            pygame.draw.polygon(self.image, (100, 100, 120), 
                              [(base_w//2, 0), (base_w, base_h), (0, base_h)])
            pygame.draw.polygon(self.image, (255, 255, 255), 
                              [(base_w//2, 0), (base_w, base_h), (0, base_h)], 2)

        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 120
        
        self.hp = self.data['hp']
        self.max_hp = self.data['hp']
        self.speed = self.data['speed'] * SCALE
        
        self.weapons = WeaponSystem()
        self.vel_x = 0
        self.vel_y = 0
        self.is_shooting = False
        self.shoot_timer = 0

    def load_and_scale(self, filename):
        # --- CORREÇÃO: Usa ASSETS_FOLDER ---
        path = os.path.join(ASSETS_FOLDER, filename)
        img = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(img, self.base_size)

    def update_input(self, axis_x, axis_y):
        self.vel_x = axis_x * self.speed
        self.vel_y = axis_y * self.speed

    def trigger_shoot_anim(self):
        self.is_shooting = True
        self.shoot_timer = pygame.time.get_ticks()

    def update(self):
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
        
        if self.rect.left < 0: self.rect.left = 0
        if self.rect.right > WIDTH: self.rect.right = WIDTH
        if self.rect.top < 0: self.rect.top = 0
        if self.rect.bottom > HEIGHT: self.rect.bottom = HEIGHT

        if self.has_images:
            if self.vel_x < -1.0: 
                self.image = self.sprites['left']
            elif self.vel_x > 1.0:
                self.image = self.sprites['right']
            else:
                if self.is_shooting and (pygame.time.get_ticks() - self.shoot_timer < 100):
                    self.image = self.sprites['shoot']
                else:
                    self.image = self.sprites['neutral']
                    self.is_shooting = False

# --- O resto do código (Enemy, Explosion, Background) continua igual ---
# Copie as classes Enemy, Explosion e Background do código anterior para cá
# Se precisar que eu mande completo de novo, é só avisar!
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, e_type="JET"):
        super().__init__()
        self.type = e_type
        
        if self.type == "JET":
            self.image = pygame.Surface((int(40*SCALE), int(40*SCALE)))
            self.image.fill((150, 50, 50))
            pygame.draw.polygon(self.image, (255, 50, 50), [(0,0), (int(40*SCALE),0), (int(20*SCALE),int(40*SCALE))])
            self.speed_y = 5 * SCALE
            self.hp = 30
        elif self.type == "TANK":
            self.image = pygame.Surface((int(50*SCALE), int(50*SCALE)))
            self.image.fill((80, 100, 50))
            pygame.draw.rect(self.image, (30, 60, 30), (10, 10, 30, 30))
            self.speed_y = SCROLL_SPEED
            self.hp = 100
        elif self.type == "HELICOPTER":
            self.image = pygame.Surface((int(45*SCALE), int(45*SCALE)))
            self.image.fill((50, 50, 100))
            self.speed_y = 3 * SCALE
            self.hp = 50
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.y = y

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.top > HEIGHT:
            self.kill()

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
            color = (255, random.randint(100,255), 0)
            pygame.draw.circle(self.image, color, (self.size//2, self.size//2), (self.size//2) * (self.timer/15))
        if self.timer <= 0:
            self.kill()

class Background:
    def __init__(self):
        self.scroll_y = 0
        self.bg_image = pygame.Surface((WIDTH, HEIGHT))
        self.bg_image.fill((50, 150, 50))
        for _ in range(40):
            color = (34, 100, 34)
            rect = (random.randint(0, WIDTH), random.randint(0, HEIGHT), random.randint(40, 90), random.randint(40, 90))
            pygame.draw.rect(self.bg_image, color, rect)
    def update(self):
        self.scroll_y += SCROLL_SPEED
        if self.scroll_y >= HEIGHT:
            self.scroll_y = 0
    def draw(self, screen):
        screen.blit(self.bg_image, (0, self.scroll_y))
        screen.blit(self.bg_image, (0, self.scroll_y - HEIGHT))
