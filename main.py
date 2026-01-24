import pygame
import sys
import os
import random
from settings import *
from sprites import Player, Background, Explosion, Enemy, Cloud, PowerUp
from weapons import Projectile
from level_manager import LevelManager
from interface import UIManager

print("\n--- INICIANDO COM SAFE MARGINS ---")
folder = os.path.dirname(__file__)
assets_folder = os.path.join(folder, 'assets')

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.joystick.init()
        
        self.sounds = {}
        try:
            self.sounds['shoot'] = pygame.mixer.Sound(os.path.join(assets_folder, 'pew.wav'))
            self.sounds['expl'] = pygame.mixer.Sound(os.path.join(assets_folder, 'boom.wav'))
            self.sounds['powerup'] = pygame.mixer.Sound(os.path.join(assets_folder, 'powerup.wav'))
        except: pass
        
        try:
            self.joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
        except Exception: self.joysticks = []
        
        self.screen = pygame.display.set_mode((REAL_WIDTH, REAL_HEIGHT), pygame.FULLSCREEN)
        self.virtual_screen = pygame.Surface((WIDTH, HEIGHT))
        self.scale_w = REAL_WIDTH / WIDTH
        self.scale_h = REAL_HEIGHT / HEIGHT
        
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.ui = UIManager()
        self.state = 'MENU'
        self.selected_plane = "F-16 Viper"
        self.fingers = {} 
        self.running = True
        
        layers_config = [("layer_sea.png", 0.5), ("layer_surface.png", 0.8)]
        self.bg = Background(layers_config)
        
        self.score = 0
        self.high_score = 0
        try:
            with open("highscore.txt", "r") as f: self.high_score = int(f.read())
        except: pass

    def save_highscore(self):
        if self.score > self.high_score:
            self.high_score = self.score
            with open("highscore.txt", "w") as f: f.write(str(self.high_score))

    def play_sound(self, name):
        if name in self.sounds: self.sounds[name].play()

    def new_game(self):
        self.score = 0
        self.all_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        
        for i in range(3): 
            c = Cloud()
            c.rect.y = random.randint(0, HEIGHT) 
            self.all_sprites.add(c)

        self.player = Player(self.selected_plane)
        self.all_sprites.add(self.player)
        self.level_manager = LevelManager(self)
        self.state = 'GAME'

    def get_virtual_pos(self, event):
        real_x = event.x * REAL_WIDTH
        real_y = event.y * REAL_HEIGHT
        virt_x = int(real_x / self.scale_w)
        virt_y = int(real_y / self.scale_h)
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
        if self.joysticks:
            joy = self.joysticks[0]
            if joy.get_numaxes() >= 2:
                if abs(joy.get_axis(0)) > 0.4: move_x = joy.get_axis(0)
                if abs(joy.get_axis(1)) > 0.4: move_y = joy.get_axis(1)
            if joy.get_numbuttons() > 0 and joy.get_button(0): shoot = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT: self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_z: self.player.weapons.switch()
            if event.type == pygame.FINGERDOWN or event.type == pygame.FINGERMOTION:
                x, y = self.get_virtual_pos(event)
                self.fingers[event.finger_id] = (x, y)
                if event.type == pygame.FINGERDOWN:
                    if self.ui.btn_switch.collidepoint(x, y): self.player.weapons.switch()
            if event.type == pygame.FINGERUP:
                if event.finger_id in self.fingers: del self.fingers[event.finger_id]

        for finger_pos in self.fingers.values():
            fx, fy = finger_pos
            if self.ui.btn_left.collidepoint(fx, fy): move_x = -1
            if self.ui.btn_right.collidepoint(fx, fy): move_x = 1
            if self.ui.btn_up.collidepoint(fx, fy): move_y = -1
            if self.ui.btn_down.collidepoint(fx, fy): move_y = 1
            if self.ui.btn_fire.collidepoint(fx, fy): shoot = True

        self.player.update_input(move_x, move_y)
        
        if shoot:
            now = pygame.time.get_ticks()
            if now % 10 == 0: 
                self.player.trigger_shoot_anim()
                self.play_sound('shoot')
                w_type = self.player.weapons.get_current()
                if w_type == "VULCAN" and self.player.powered_up:
                    b1 = Projectile(self.player.rect.left, self.player.rect.top, w_type)
                    b2 = Projectile(self.player.rect.right, self.player.rect.top, w_type)
                    b3 = Projectile(self.player.rect.centerx, self.player.rect.top - 10, w_type)
                    self.all_sprites.add(b1, b2, b3); self.bullets.add(b1, b2, b3)
                else:
                    if w_type == "VULCAN":
                        b1 = Projectile(self.player.rect.left + 5, self.player.rect.top, w_type)
                        b2 = Projectile(self.player.rect.right - 5, self.player.rect.top, w_type)
                        self.all_sprites.add(b1, b2); self.bullets.add(b1, b2)
                    else:
                        b = Projectile(self.player.rect.centerx, self.player.rect.top, w_type)
                        self.all_sprites.add(b); self.bullets.add(b)

    def update_game(self):
        self.bg.update()
        self.all_sprites.update()
        self.level_manager.update()
        hits = pygame.sprite.groupcollide(self.enemies, self.bullets, False, True)
        for enemy, bullets in hits.items():
            for b in bullets:
                enemy.hp -= b.damage
                if enemy.hp <= 0:
                    self.score += 100
                    self.play_sound('expl')
                    if random.random() < 0.1:
                        p = PowerUp(enemy.rect.center)
                        self.all_sprites.add(p); self.powerups.add(p)
                    expl = Explosion(enemy.rect.center)
                    self.all_sprites.add(expl)
                    enemy.kill()
        hit_powerup = pygame.sprite.spritecollide(self.player, self.powerups, True)
        for p in hit_powerup:
            self.play_sound('powerup')
            self.player.enable_powerup()
        if pygame.sprite.spritecollide(self.player, self.enemies, True):
            self.player.hp -= 20
            self.all_sprites.add(Explosion(self.player.rect.center))
            self.play_sound('expl')
            if self.player.hp <= 0:
                self.save_highscore()
                self.state = 'MENU' 

    def draw_game(self):
        self.bg.draw(self.virtual_screen)
        self.all_sprites.draw(self.virtual_screen)
        self.ui.draw_hud(self.virtual_screen, self.player)
        
        # --- SCORE NO CENTRO (CORRIGIDO) ---
        font = pygame.font.SysFont("arial", 20, bold=True)
        score_txt = font.render(f"SCORE: {self.score}", True, WHITE)
        hi_txt = font.render(f"HI: {self.high_score}", True, YELLOW)
        
        # Centralizado horizontalmente no topo
        center_x = WIDTH // 2
        self.virtual_screen.blit(score_txt, (center_x - score_txt.get_width() // 2, 10))
        self.virtual_screen.blit(hi_txt, (center_x - hi_txt.get_width() // 2, 30))
        
        if self.player.powered_up:
            pwr_txt = font.render("POWER UP!", True, CYAN)
            self.virtual_screen.blit(pwr_txt, (WIDTH//2 - pwr_txt.get_width()//2, HEIGHT - 80))

if __name__ == "__main__":
    g = Game()
    g.run()
