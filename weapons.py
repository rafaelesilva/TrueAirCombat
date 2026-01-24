import pygame
import math
import random
from settings import *

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
        if self.lifetime <= 0: self.kill()
        else:
            alpha = int((self.lifetime / self.original_life) * 255)
            self.image.set_alpha(alpha)

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, angle, missile_type, owner_type="PLAYER"):
        super().__init__()
        self.type = missile_type
        self.owner = owner_type 
        # Fallback para VULCAN se der erro no nome
        self.stats = MISSILE_STATS.get(missile_type, MISSILE_STATS['VULCAN'])
        
        self.speed = self.stats['vel']
        self.color = self.stats['color']
        self.damage = self.stats.get('dmg', 10)
        self.category = self.stats.get('type', 'MISSILE') 
        self.angle = angle
        
        # Timer de detonação para bombas
        self.timer = 40 if self.category == 'BOMB' else 200
        self.should_explode = False
        
        length, width = self.stats['size']
        self.original_image = pygame.Surface((length + 6, width + 6), pygame.SRCALPHA)
        cy = (width + 6) // 2
        
        if self.category == 'GUN':
            pygame.draw.circle(self.original_image, self.color, (2, cy), 2)
        else:
            fins = self.stats['fins']
            if fins in ['BOMB', 'MOAB']:
                # Bomba
                rect = pygame.Rect(0, cy - width//2, length, width)
                pygame.draw.ellipse(self.original_image, self.color, rect)
                pygame.draw.line(self.original_image, (255, 255, 0), (length-4, cy-width//2+2), (length-4, cy+width//2-2), 2)
                if fins == 'MOAB': pygame.draw.rect(self.original_image, (100,100,100), (0, cy-width//2, length, 2)) # Detalhe MOAB
                else: pygame.draw.rect(self.original_image, (20,20,20), (0, cy-width//2-2, 3, width+4)) # Aletas
            else:
                # Míssil
                pygame.draw.rect(self.original_image, self.color, (0, cy - width//2, length, width))
                pygame.draw.polygon(self.original_image, (50, 50, 50), [(length, cy - width//2), (length + 4, cy), (length, cy + width//2)])
                
                fin_c = (60, 60, 60)
                if fins == 'INTAKE': pygame.draw.rect(self.original_image, (20,20,20), (length//2, cy-width-1, 4, width+2))
                elif fins == 'GRID': pygame.draw.line(self.original_image, fin_c, (2, cy-width), (2, cy+width), 2)
                elif fins == 'STEALTH': pygame.draw.polygon(self.original_image, self.color, [(0, cy-2), (length, cy-width), (length, cy+width), (0, cy+2)])
                elif fins == 'WINGS': 
                    pygame.draw.polygon(self.original_image, fin_c, [(length//2, cy), (length-2, cy-6), (length, cy-6)])
                    pygame.draw.polygon(self.original_image, fin_c, [(length//2, cy), (length-2, cy+6), (length, cy+6)])
                else: pygame.draw.polygon(self.original_image, fin_c, [(0, cy), (4, cy-width-2), (4, cy+width+2)])

        self.image = pygame.transform.rotate(self.original_image, angle)
        self.rect = self.image.get_rect(center=(x, y))
        
        rad = math.radians(angle)
        self.vx = math.cos(rad) * self.speed
        self.vy = -math.sin(rad) * self.speed 
        self.pos_x, self.pos_y = float(x), float(y)
        self.drag = 0.96 if self.category == 'BOMB' else 1.0

    def update(self):
        self.pos_x += self.vx
        self.pos_y += self.vy
        
        if self.category == 'BOMB':
            self.vx *= self.drag
            self.vy *= self.drag
            self.timer -= 1
            if self.timer <= 0: self.should_explode = True
        
        self.rect.centerx = int(self.pos_x)
        self.rect.centery = int(self.pos_y)
        
        if (self.rect.x < -100 or self.rect.x > MAP_WIDTH + 100 or
            self.rect.y < -100 or self.rect.y > MAP_HEIGHT + 100):
            self.kill()

class WeaponSystem:
    def __init__(self, loadout_list):
        # Recebe a lista de armas (ex: ['VULCAN', 'METEOR', 'MK-82'])
        self.weapons = loadout_list
        self.index = 0
        
    def switch(self):
        # Cicla: 0 -> 1 -> 2 -> 0 ...
        self.index = (self.index + 1) % len(self.weapons)
            
    def get_current(self):
        return self.weapons[self.index]
