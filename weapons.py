import pygame
import math
import random
from settings import *

# --- SISTEMA DE PARTÍCULAS (RASTRO DE FUMAÇA) ---
class Particle(pygame.sprite.Sprite):
    def __init__(self, pos, color, size, lifetime):
        super().__init__()
        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (size//2, size//2), size//2)
        self.rect = self.image.get_rect(center=pos)
        self.lifetime = lifetime
        self.original_life = lifetime
        
    def update(self):
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.kill()
        else:
            # Efeito de "dissolver": fica mais transparente e menor
            alpha = int((self.lifetime / self.original_life) * 255)
            self.image.set_alpha(alpha)

# --- CLASSE PROJÉTIL (MÍSSIL BONITO) ---
class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, angle, missile_type, owner_type="PLAYER"):
        super().__init__()
        self.type = missile_type
        self.owner = owner_type # "PLAYER" ou "ENEMY"
        self.stats = MISSILE_STATS.get(missile_type, MISSILE_STATS['VULCAN'])
        
        self.speed = self.stats['vel']
        self.color = self.stats['color']
        self.angle = angle
        
        # Cria a "imagem" base do míssil desenhando formas
        length, width = self.stats['size']
        self.original_image = pygame.Surface((length + 4, width + 6), pygame.SRCALPHA)
        
        # Desenha o corpo do míssil
        cy = (width + 6) // 2
        
        if self.type == 'VULCAN':
            # Tiro simples (bolinha brilhante)
            pygame.draw.circle(self.original_image, self.color, (2, cy), 2)
        else:
            # --- DESENHO DETALHADO DO MÍSSIL ---
            # Corpo
            pygame.draw.rect(self.original_image, self.color, (0, cy - width//2, length, width))
            # Bico (Nariz)
            pygame.draw.polygon(self.original_image, (50, 50, 50), [(length, cy - width//2), (length + 4, cy), (length, cy + width//2)])
            
            # Aletas (Fins) baseadas no tipo
            fin_color = (80, 80, 80)
            if self.stats['fins'] == 'INTAKE': # Meteor (tem entradas de ar)
                pygame.draw.rect(self.original_image, (30,30,30), (length//2 - 2, cy - width - 1, 4, width + 2))
            elif self.stats['fins'] == 'GRID': # R-77 (aletas traseiras de grade)
                pygame.draw.line(self.original_image, fin_color, (2, cy - width), (2, cy + width), 2)
                pygame.draw.line(self.original_image, fin_color, (0, cy - width), (4, cy - width), 1)
                pygame.draw.line(self.original_image, fin_color, (0, cy + width), (4, cy + width), 1)
            else: # Normal (AMRAAM, Sidewinder)
                # Aletas traseiras
                pygame.draw.polygon(self.original_image, fin_color, [(0, cy), (4, cy - width - 2), (4, cy + width + 2)])

        # Rotaciona para a direção correta
        # -angle porque o pygame rotaciona anti-horário e nossos graus são matemáticos
        self.image = pygame.transform.rotate(self.original_image, angle)
        self.rect = self.image.get_rect(center=(x, y))
        
        # Calcula vetor de velocidade (vx, vy)
        rad = math.radians(angle)
        self.vx = math.cos(rad) * self.speed
        self.vy = -math.sin(rad) * self.speed # Y invertido
        
        # Posição float para precisão
        self.pos_x = float(x)
        self.pos_y = float(y)

    def update(self):
        self.pos_x += self.vx
        self.pos_y += self.vy
        self.rect.centerx = int(self.pos_x)
        self.rect.centery = int(self.pos_y)
        
        # Limites do mapa (deleta se sair muito longe)
        if (self.rect.x < -100 or self.rect.x > MAP_WIDTH + 100 or
            self.rect.y < -100 or self.rect.y > MAP_HEIGHT + 100):
            self.kill()

# --- GERENCIADOR DE ARMAS ---
class WeaponSystem:
    def __init__(self, missile_type='AIM-120'):
        self.primary = 'VULCAN'
        self.secondary = missile_type
        self.current = self.primary
        self.ammo = 50 # Mísseis limitados? (Por enquanto infinito na lógica)

    def switch(self):
        if self.current == self.primary:
            self.current = self.secondary
        else:
            self.current = self.primary
            
    def get_current(self):
        return self.current
