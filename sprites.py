import pygame
import os
import random
from settings import *
from weapons import WeaponSystem

# Define a pasta do jogo para carregar imagens
GAME_FOLDER = os.path.dirname(__file__)
ASSETS_FOLDER = os.path.join(GAME_FOLDER, 'assets')

# --- CLASSE JOGADOR ---
class Player(pygame.sprite.Sprite):
    def __init__(self, model_name):
        super().__init__()
        # Carrega dados do settings.py
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
            self.sprites['neutral'] = self.load_and_scale(f"{self.prefix}_neutral.png")
            self.sprites['left'] = self.load_and_scale(f"{self.prefix}_left.png")
            self.sprites['right'] = self.load_and_scale(f"{self.prefix}_right.png")
            self.sprites['shoot'] = self.load_and_scale(f"{self.prefix}_shoot.png")
            self.has_images = True
            self.image = self.sprites['neutral']
        except Exception as e:
            print(f"AVISO: Imagens não encontradas para {self.prefix}. Usando modo geométrico.")
            self.has_images = False
            self.image = pygame.Surface(self.base_size, pygame.SRCALPHA)
            pygame.draw.polygon(self.image, (100, 100, 120), [(base_w//2, 0), (base_w, base_h), (0, base_h)])
            pygame.draw.polygon(self.image, (255, 255, 255), [(base_w//2, 0), (base_w, base_h), (0, base_h)], 2)

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

# --- CLASSE INIMIGO (ATUALIZADA) ---
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, model_name="Gripen F-39E"):
        super().__init__()
        
        # 1. Carrega dados do avião escolhido
        if model_name in AIRCRAFT_DATA:
            self.data = AIRCRAFT_DATA[model_name]
        else:
            self.data = AIRCRAFT_DATA['Gripen F-39E']
            
        self.prefix = self.data['prefix']
        
        # 2. Define tamanho (igual ao player)
        base_w = int(70 * SCALE * self.data.get('scale_factor', 1.0))
        base_h = int(90 * SCALE * self.data.get('scale_factor', 1.0))
        self.base_size = (base_w, base_h)
        
        # 3. Tenta carregar a imagem e GIRAR 180 GRAUS (Inimigo vem de cima)
        try:
            path = os.path.join(ASSETS_FOLDER, f"{self.prefix}_neutral.png")
            img = pygame.image.load(path).convert_alpha()
            img_scaled = pygame.transform.scale(img, self.base_size)
            self.image = pygame.transform.rotate(img_scaled, 180)
        except Exception:
            # Fallback se não achar imagem
            self.image = pygame.Surface(self.base_size)
            self.image.fill((200, 50, 50))
            pygame.draw.line(self.image, WHITE, (0,0), (base_w, base_h), 3)
            pygame.draw.line(self.image, WHITE, (base_w, 0), (0, base_h), 3)

        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.y = y
        
        # 4. Atributos
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

# --- NOVA CLASSE NUVEM (Efeito Parallax) ---
class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Tamanho aleatório
        w = random.randint(int(100*SCALE), int(250*SCALE))
        h = int(w * 0.6)
        self.image = pygame.Surface((w, h), pygame.SRCALPHA)
        
        # Desenha "bolinhas" de nuvem
        num_blobs = random.randint(5, 8)
        for _ in range(num_blobs):
            bx = random.randint(0, w//2)
            by = random.randint(0, h//2)
            radius = random.randint(int(20*SCALE), int(50*SCALE))
            # Branco semi-transparente
            pygame.draw.circle(self.image, (255, 255, 255, 60), (bx+radius, by+radius), radius)
            
        self.rect = self.image.get_rect()
        # Nasce em posição aleatória
        self.rect.x = random.randint(0, WIDTH - w)
        self.rect.y = random.randint(-500, -50)
        # Velocidade diferente do fundo
        self.speed_y = random.randint(2, 4) * SCALE

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.top > HEIGHT:
            # Recicla a nuvem lá em cima
            self.rect.x = random.randint(0, WIDTH - self.rect.width)
            self.rect.y = random.randint(-500, -50)

# --- CLASSE BACKGROUND (Flexível para Fases) ---
class Background:
    def __init__(self, image_file):
        self.scroll_y = 0
        self.speed = SCROLL_SPEED
        
        # Carrega a imagem específica da fase
        bg_path = os.path.join(ASSETS_FOLDER, image_file)
        
        try:
            img = pygame.image.load(bg_path).convert()
            
            # Ajusta tamanho mantendo proporção ou esticando
            # Aqui vamos esticar para garantir que cubra a tela (estilo Shoot em Up)
            self.bg_image = pygame.transform.scale(img, (WIDTH, HEIGHT))
            self.bg_h = HEIGHT
            self.has_image = True
            print(f"Cenário carregado: {image_file}")
            
        except Exception as e:
            print(f"Erro no cenário {image_file}: {e}")
            self.has_image = False
            self.bg_image = pygame.Surface((WIDTH, HEIGHT))
            self.bg_image.fill((0, 100, 200)) # Azul padrão

    def update(self):
        self.scroll_y += self.speed
        if self.scroll_y >= self.bg_h:
            self.scroll_y = 0

    def draw(self, screen):
        if self.has_image:
            # Desenha duas vezes para loop infinito
            screen.blit(self.bg_image, (0, self.scroll_y))
            screen.blit(self.bg_image, (0, self.scroll_y - self.bg_h))
        else:
            screen.blit(self.bg_image, (0,0))
