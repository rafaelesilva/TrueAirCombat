import pygame
import os
import random
from settings import *
from weapons import WeaponSystem

# Garante que acha a pasta assets onde quer que esteja
GAME_FOLDER = os.path.dirname(__file__)
ASSETS_FOLDER = os.path.join(GAME_FOLDER, 'assets')

# --- CLASSE JOGADOR ---
class Player(pygame.sprite.Sprite):
    def __init__(self, model_name):
        super().__init__()
        # Carrega dados da aeronave
        if model_name in AIRCRAFT_DATA:
            self.data = AIRCRAFT_DATA[model_name]
        else:
            self.data = AIRCRAFT_DATA['Gripen F-39E']
            
        self.model_name = model_name
        self.prefix = self.data['prefix']
        
        # Tamanho Base
        base_w = int(70 * SCALE * self.data.get('scale_factor', 1.0))
        base_h = int(90 * SCALE * self.data.get('scale_factor', 1.0))
        self.base_size = (base_w, base_h)
        
        self.sprites = {}
        self.has_images = False
        
        # Tenta carregar as imagens
        try:
            self.sprites['neutral'] = self.load_and_scale(f"{self.prefix}_neutral.png")
            self.sprites['left'] = self.load_and_scale(f"{self.prefix}_left.png")
            self.sprites['right'] = self.load_and_scale(f"{self.prefix}_right.png")
            self.sprites['shoot'] = self.load_and_scale(f"{self.prefix}_shoot.png")
            self.has_images = True
            self.image = self.sprites['neutral']
        except Exception:
            # Fallback se não tiver imagem: Triângulo
            self.has_images = False
            self.image = pygame.Surface(self.base_size, pygame.SRCALPHA)
            pygame.draw.polygon(self.image, (100, 100, 120), [(base_w//2, 0), (base_w, base_h), (0, base_h)])
            pygame.draw.polygon(self.image, (255, 255, 255), [(base_w//2, 0), (base_w, base_h), (0, base_h)], 2)

        self.rect = self.image.get_rect()
        # Posiciona no centro da tela VIRTUAL
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 50 # Margem inferior
        
        self.hp = self.data['hp']
        self.max_hp = self.data['hp']
        self.speed = self.data['speed'] * SCALE
        
        self.weapons = WeaponSystem()
        self.vel_x = 0
        self.vel_y = 0
        self.is_shooting = False
        self.shoot_timer = 0
        
        # PowerUp
        self.powerup_timer = 0
        self.powered_up = False

    def load_and_scale(self, filename):
        path = os.path.join(ASSETS_FOLDER, filename)
        img = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(img, self.base_size)

    def update_input(self, axis_x, axis_y):
        self.vel_x = axis_x * self.speed
        self.vel_y = axis_y * self.speed

    def trigger_shoot_anim(self):
        self.is_shooting = True
        self.shoot_timer = pygame.time.get_ticks()

    def enable_powerup(self):
        self.powered_up = True
        self.powerup_timer = pygame.time.get_ticks()
        self.hp = min(self.hp + 20, self.max_hp)

    def update(self):
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
        
        # Mantém dentro da tela VIRTUAL
        if self.rect.left < 0: self.rect.left = 0
        if self.rect.right > WIDTH: self.rect.right = WIDTH
        if self.rect.top < 0: self.rect.top = 0
        if self.rect.bottom > HEIGHT: self.rect.bottom = HEIGHT
        
        if self.powered_up and pygame.time.get_ticks() - self.powerup_timer > 5000:
            self.powered_up = False

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

# --- CLASSE INIMIGO ---
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, model_name="Gripen F-39E"):
        super().__init__()
        
        if model_name in AIRCRAFT_DATA:
            self.data = AIRCRAFT_DATA[model_name]
        else:
            self.data = AIRCRAFT_DATA['Gripen F-39E']
            
        self.prefix = self.data['prefix']
        
        base_w = int(70 * SCALE * self.data.get('scale_factor', 1.0))
        base_h = int(90 * SCALE * self.data.get('scale_factor', 1.0))
        self.base_size = (base_w, base_h)
        
        try:
            path = os.path.join(ASSETS_FOLDER, f"{self.prefix}_neutral.png")
            img = pygame.image.load(path).convert_alpha()
            img_scaled = pygame.transform.scale(img, self.base_size)
            self.image = pygame.transform.rotate(img_scaled, 180)
        except Exception:
            self.image = pygame.Surface(self.base_size)
            self.image.fill((200, 50, 50))
            pygame.draw.line(self.image, WHITE, (0,0), (base_w, base_h), 3)

        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.y = y
        self.speed_y = (self.data['speed'] * 0.7) * SCALE 
        self.hp = self.data['hp'] * 0.4 

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.top > HEIGHT:
            self.kill()

# --- CLASSE EXPLOSÃO ---
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

# --- CLASSE POWERUP ---
class PowerUp(pygame.sprite.Sprite):
    def __init__(self, center):
        super().__init__()
        self.size = int(25 * SCALE)
        self.image = pygame.Surface((self.size, self.size))
        self.image.fill(CYAN)
        pygame.draw.rect(self.image, WHITE, (0,0,self.size,self.size), 2)
        
        font = pygame.font.SysFont('arial', int(15*SCALE), bold=True)
        txt = font.render("P", True, BLACK)
        self.image.blit(txt, (self.size//2 - txt.get_width()//2, self.size//2 - txt.get_height()//2))
        
        self.rect = self.image.get_rect(center=center)
        self.speed_y = 2 * SCALE

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.top > HEIGHT:
            self.kill()

# --- CLASSE NUVEM ---
class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        w = random.randint(int(50*SCALE), int(150*SCALE))
        h = int(w * 0.6)
        self.image = pygame.Surface((w, h), pygame.SRCALPHA)
        num_blobs = random.randint(3, 6)
        for _ in range(num_blobs):
            bx = random.randint(0, w//2)
            by = random.randint(0, h//2)
            radius = random.randint(int(10*SCALE), int(30*SCALE))
            pygame.draw.circle(self.image, (255, 255, 255, 60), (bx+radius, by+radius), radius)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - w)
        self.rect.y = random.randint(-200, -50)
        self.speed_y = random.randint(1, 3) * SCALE

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.top > HEIGHT:
            self.rect.x = random.randint(0, WIDTH - self.rect.width)
            self.rect.y = random.randint(-200, -50)

# --- BACKGROUND OTIMIZADO ---
class BackgroundLayer:
    def __init__(self, image_file, scroll_speed_factor):
        self.scroll_y = 0
        self.speed = SCROLL_SPEED * scroll_speed_factor
        
        bg_path = os.path.join(ASSETS_FOLDER, image_file)
        try:
            img_raw = pygame.image.load(bg_path)
            
            # PERFORMANCE TOTAL:
            # 1. Converte formato
            if "sea" in image_file:
                img = img_raw.convert()
            else:
                img = img_raw.convert_alpha()
            
            # 2. Redimensiona UMA VEZ para a resolução virtual (pequena)
            self.bg_image = pygame.transform.scale(img, (WIDTH, HEIGHT))
            self.bg_h = HEIGHT
            self.has_image = True
        except Exception as e:
            print(f"Erro fundo {image_file}: {e}")
            self.has_image = False
            self.bg_image = pygame.Surface((WIDTH, HEIGHT))
            self.bg_h = HEIGHT
            if scroll_speed_factor > 0.5: self.bg_image.fill((0,0,0,0)) 
            else: self.bg_image.fill((0, 50, 100))

    def update(self):
        self.scroll_y += self.speed
        if self.scroll_y >= self.bg_h:
            self.scroll_y = 0

    def draw(self, screen):
        if self.has_image:
            screen.blit(self.bg_image, (0, self.scroll_y))
            if self.scroll_y > 0:
                screen.blit(self.bg_image, (0, self.scroll_y - self.bg_h))
        else:
             screen.blit(self.bg_image, (0,0))

class Background:
    def __init__(self, layers_config):
        self.layers = []
        for img_file, speed_factor in layers_config:
            self.layers.append(BackgroundLayer(img_file, speed_factor))

    def update(self):
        for layer in self.layers:
            layer.update()

    def draw(self, screen):
        for layer in self.layers:
            layer.draw(screen)
