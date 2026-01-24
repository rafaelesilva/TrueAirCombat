import pygame
import sys
import os
import random
import math
from settings import *
from camera import Camera
from sprites import Player, BigMap, Explosion, Enemy, Cloud, PowerUp
# CORREÇÃO: Adicionei 'Particle' aqui
from weapons import Projectile, Particle 
from level_manager import LevelManager
from interface import UIManager

print("\n--- INICIANDO MODO DESERT STRIKE (FINAL + PARTICLES) ---")
folder = os.path.dirname(__file__)
assets_folder = os.path.join(folder, 'assets')

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        
        self.sounds = {}
        try:
            self.sounds['shoot'] = pygame.mixer.Sound(os.path.join(assets_folder, 'pew.wav'))
            self.sounds['expl'] = pygame.mixer.Sound(os.path.join(assets_folder, 'boom.wav'))
            self.sounds['powerup'] = pygame.mixer.Sound(os.path.join(assets_folder, 'powerup.wav'))
        except: pass
        
        self.screen = pygame.display.set_mode((REAL_WIDTH, REAL_HEIGHT), pygame.FULLSCREEN)
        self.virtual_screen = pygame.Surface((WIDTH, HEIGHT))
        
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.ui = UIManager()
        self.state = 'MENU'
        self.selected_plane = "F-16 Viper"
        self.fingers = {} 
        self.running = True
        
        self.score = 0
        self.high_score = 0
        
        try:
            with open("highscore.txt", "r") as f:
                self.high_score = int(f.read())
        except:
            pass

    def save_highscore(self):
        if self.score > self.high_score:
            self.high_score = self.score
            try:
                with open("highscore.txt", "w") as f:
                    f.write(str(self.high_score))
            except:
                pass

    def play_sound(self, name):
        if name in self.sounds: self.sounds[name].play()

    def new_game(self):
        self.score = 0
        self.all_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.enemy_bullets = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        self.clouds = pygame.sprite.Group() 
        self.particles = pygame.sprite.Group()

        self.map = BigMap("big_map.png")
        self.camera = Camera(MAP_WIDTH, MAP_HEIGHT)

        self.player = Player(self.selected_plane)
        self.all_sprites.add(self.player)
        
        for i in range(20):
            c = Cloud()
            self.clouds.add(c)

        self.level_manager = LevelManager(self)
        self.state = 'GAME'

    def get_virtual_pos(self, event):
        virt_x = int(event.x * WIDTH)
        virt_y = int(event.y * HEIGHT)
        return virt_x, virt_y

    def run(self):
        while self.running:
            self.clock.tick(FPS)
            
            if self.state == 'MENU':
                self.events_menu()
                self.ui.draw_menu(self.virtual_screen)
            elif self.state == 'SELECT':
                self.events_select()
                self.ui.draw_select(self.virtual_screen)
            elif self.state == 'GAME':
                self.events_game()
                self.update_game()
                self.draw_game()
            
            scaled_surf = pygame.transform.scale(self.virtual_screen, (REAL_WIDTH, REAL_HEIGHT))
            self.screen.blit(scaled_surf, (0, 0))
            
            # Debug Visual (Bolinha Amarela)
            for f_id, pos in self.fingers.items():
                rx = int((pos[0] / WIDTH) * REAL_WIDTH)
                ry = int((pos[1] / HEIGHT) * REAL_HEIGHT)
                pygame.draw.circle(self.screen, (255, 255, 0), (rx, ry), 40, 2)
                
            pygame.display.flip()

    def events_menu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: self.running = False
            if event.type == pygame.FINGERDOWN:
                x, y = self.get_virtual_pos(event)
                if self.ui.btn_campanha.collidepoint(x,y): self.state = 'SELECT'
                elif self.ui.btn_missao.collidepoint(x,y): self.state = 'SELECT'

    def events_select(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: self.running = False
            if event.type == pygame.FINGERDOWN:
                x, y = self.get_virtual_pos(event)
                for btn in self.ui.plane_buttons:
                    if btn['rect'].collidepoint(x,y):
                        self.selected_plane = btn['name']
                        self.new_game()

    def events_game(self):
        move_x, move_y = 0, 0
        shoot = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_z: self.player.weapons.switch()
            
            if event.type == pygame.FINGERDOWN or event.type == pygame.FINGERMOTION:
                x, y = self.get_virtual_pos(event)
                self.fingers[event.finger_id] = (x, y)
                if event.type == pygame.FINGERDOWN:
                    if self.ui.btn_switch_hitbox.collidepoint(x, y): 
                        self.player.weapons.switch()

            if event.type == pygame.FINGERUP:
                if event.finger_id in self.fingers: del self.fingers[event.finger_id]

        for finger_pos in self.fingers.values():
            fx, fy = finger_pos
            
            # Lógica do D-Pad Circular
            dx = fx - self.ui.dpad_center[0]
            dy = fy - self.ui.dpad_center[1]
            dist = math.hypot(dx, dy)
            
            if 10 < dist < self.ui.dpad_radius:
                angle = math.atan2(dy, dx)
                deg = math.degrees(angle)
                
                if -22.5 <= deg <= 22.5: move_x = 1
                elif 22.5 < deg < 67.5: move_x, move_y = 1, 1
                elif 67.5 <= deg <= 112.5: move_y = 1
                elif 112.5 < deg < 157.5: move_x, move_y = -1, 1
                elif deg >= 157.5 or deg <= -157.5: move_x = -1
                elif -157.5 < deg < -112.5: move_x, move_y = -1, -1
                elif -112.5 <= deg <= -67.5: move_y = -1
                elif -67.5 < deg < -22.5: move_x, move_y = 1, -1

            if self.ui.btn_fire_hitbox.collidepoint(fx, fy): shoot = True

        self.player.update_input(move_x, move_y)
        
        if shoot:
            now = pygame.time.get_ticks()
            if now % 15 == 0: 
                self.player.trigger_shoot_anim()
                self.play_sound('shoot')
                w_type = self.player.weapons.get_current()
                
                angle_rad = math.radians(self.player.angle + 90)
                # Velocidade do tiro (vetor)
                # Pegamos a velocidade do míssil definida no settings (via WeaponSystem -> Projectile)
                # Mas aqui criamos o projetil primeiro para pegar a velocidade dele depois?
                # Melhor: instanciamos e ele já calcula.
                
                b = Projectile(self.player.rect.centerx, self.player.rect.centery, self.player.angle + 90, w_type, "PLAYER")
                
                # Hack para mover o projetil no update (sobrescrevendo o método update do objeto)
                # Como a classe Projectile no weapons.py já tem movimento vetorial,
                # NÃO precisamos do lambda hack aqui se o weapons.py estiver correto!
                # Vou manter o padrão simples: adicionar ao grupo e deixar a classe Projectile cuidar do movimento.
                
                self.all_sprites.add(b); self.bullets.add(b)

    def update_game(self):
        self.all_sprites.update()
        self.clouds.update()
        self.level_manager.update()
        self.particles.update()
        self.camera.update(self.player)
        
        # Inimigos atiram
        current_time = pygame.time.get_ticks()
        for enemy in self.enemies:
            should_fire, angle = enemy.check_fire(self.player.rect, current_time)
            if should_fire:
                b = Projectile(enemy.rect.centerx, enemy.rect.centery, angle, enemy.missile_type, "ENEMY")
                self.all_sprites.add(b)
                self.enemy_bullets.add(b)

        # Rastro de Fumaça (Particles)
        all_missiles = list(self.bullets) + list(self.enemy_bullets)
        for b in all_missiles:
            if b.type != 'VULCAN':
                if random.random() < 0.5:
                    p = Particle(b.rect.center, (200, 200, 200), random.randint(4, 8), 20)
                    self.particles.add(p)

        # Colisões
        hits = pygame.sprite.groupcollide(self.enemies, self.bullets, False, True)
        for enemy, bullets in hits.items():
            for b in bullets:
                enemy.hp -= 20
                if enemy.hp <= 0:
                    self.score += 100
                    self.play_sound('expl')
                    if random.random() < 0.15:
                        p = PowerUp(enemy.rect.center)
                        self.all_sprites.add(p); self.powerups.add(p)
                    expl = Explosion(enemy.rect.center)
                    self.all_sprites.add(expl)
                    enemy.kill()
        
        hits_player = pygame.sprite.spritecollide(self.player, self.enemy_bullets, True)
        for b in hits_player:
            self.player.hp -= 15
            self.play_sound('expl')
            self.all_sprites.add(Explosion(self.player.rect.center))
            if self.player.hp <= 0:
                self.save_highscore()
                self.state = 'MENU'

        if pygame.sprite.spritecollide(self.player, self.enemies, True):
            self.player.hp -= 30
            self.all_sprites.add(Explosion(self.player.rect.center))
            self.play_sound('expl')
            if self.player.hp <= 0:
                self.save_highscore()
                self.state = 'MENU' 
                
        hit_powerup = pygame.sprite.spritecollide(self.player, self.powerups, True)
        for p in hit_powerup:
            self.play_sound('powerup')
            self.player.enable_powerup()

    def draw_game(self):
        self.virtual_screen.fill(BLACK)
        self.virtual_screen.blit(self.map.image, self.camera.apply(self.map))
        
        for p in self.particles:
            self.virtual_screen.blit(p.image, self.camera.apply(p))
            
        for cloud in self.clouds: self.virtual_screen.blit(cloud.image, self.camera.apply(cloud))
        for sprite in self.all_sprites: self.virtual_screen.blit(sprite.image, self.camera.apply(sprite))
        
        self.ui.draw_hud(self.virtual_screen, self.player, self.enemies)
        
        font = pygame.font.SysFont("arial", 20, bold=True)
        score_txt = font.render(f"SCORE: {self.score}", True, WHITE)
        center_x = WIDTH // 2
        self.virtual_screen.blit(score_txt, (center_x - score_txt.get_width() // 2, 10))

if __name__ == "__main__":
    g = Game()
    g.run()
