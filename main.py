import pygame
import sys
import os
from settings import *
from sprites import Player, Background, Explosion, Enemy
from weapons import Projectile
from level_manager import LevelManager
from interface import UIManager

# --- DIAGNÓSTICO DE ARQUIVOS (Olhe o Console!) ---
print("\n--- INICIANDO VERIFICAÇÃO DE ARQUIVOS ---")
folder = os.path.dirname(__file__)
files = os.listdir(folder)
print(f"Pasta do jogo: {folder}")
print("Arquivos encontrados:")
tem_gripen = False
for f in files:
    print(f" - {f}")
    if "gripen_neutral" in f:
        tem_gripen = True

if not tem_gripen:
    print("!!! ALERTA: 'gripen_neutral.png' NÃO ENCONTRADO !!!")
    print("O avião ficará como um triângulo cinza.")
else:
    print(">>> SUCESSO: Imagem do Gripen encontrada!")
print("------------------------------------------\n")

class Game:
    def __init__(self):
        pygame.init()
        pygame.joystick.init()
        
        try:
            self.joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
        except Exception:
            self.joysticks = []
        
        # Cria a tela
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        
        self.ui = UIManager()
        self.state = 'MENU'
        self.selected_plane = "F-16 Viper" # Começa com um avião padrão
        
        self.fingers = {} 
        self.running = True
        self.bg = Background()

    def new_game(self):
        self.all_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.enemy_bullets = pygame.sprite.Group()
        
        # Cria o jogador
        self.player = Player(self.selected_plane)
        self.all_sprites.add(self.player)
        
        self.level_manager = LevelManager(self)
        self.state = 'GAME'

    # --- FUNÇÃO MÁGICA PARA CONSERTAR O TOUCH ---
    def get_touch_pos(self, event):
        # Pega o tamanho real da janela naquele momento
        w, h = self.screen.get_size()
        # Converte a posição relativa (0.0 a 1.0) para pixels exatos
        return int(event.x * w), int(event.y * h)

    def run(self):
        while self.running:
            self.clock.tick(FPS)
            
            if self.state == 'MENU':
                self.events_menu()
                self.ui.draw_menu(self.screen)
            elif self.state == 'SELECT':
                self.events_select()
                self.ui.draw_select(self.screen)
            elif self.state == 'GAME':
                self.events_game()
                self.update_game()
                self.draw_game()
                
            pygame.display.flip()

    def events_menu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: self.running = False
            
            # Joystick
            if event.type == pygame.JOYBUTTONDOWN:
                if event.joy < len(self.joysticks):
                     if event.button == 0: self.state = 'SELECT'
            
            # Touch (Usando a correção)
            if event.type == pygame.FINGERDOWN:
                x, y = self.get_touch_pos(event)
                if self.ui.btn_campanha.collidepoint(x,y): self.state = 'SELECT'
                elif self.ui.btn_missao.collidepoint(x,y): self.state = 'SELECT'
            
            # Mouse (Para teste no PC)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.ui.btn_campanha.collidepoint(event.pos): self.state = 'SELECT'

    def events_select(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: self.running = False
            
            if event.type == pygame.FINGERDOWN:
                x, y = self.get_touch_pos(event)
                for btn in self.ui.plane_buttons:
                    if btn['rect'].collidepoint(x,y):
                        self.selected_plane = btn['name']
                        print(f"Selecionado: {self.selected_plane}")
                        self.new_game()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                for btn in self.ui.plane_buttons:
                    if btn['rect'].collidepoint(event.pos):
                        self.selected_plane = btn['name']
                        self.new_game()

    def events_game(self):
        move_x, move_y = 0, 0
        shoot = False
        
        # --- INPUT JOYSTICK ---
        if self.joysticks:
            joy = self.joysticks[0]
            if joy.get_numaxes() >= 2:
                raw_x = joy.get_axis(0)
                raw_y = joy.get_axis(1)
                if abs(raw_x) > 0.4: move_x = raw_x
                if abs(raw_y) > 0.4: move_y = raw_y
            if joy.get_numbuttons() > 0:
                if joy.get_button(0): shoot = True

        # --- INPUT TOUCHSCREEN (CORRIGIDO) ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT: self.running = False
            
            # Troca de arma (Z no teclado ou botão joy)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_z:
                self.player.weapons.switch()
            if event.type == pygame.JOYBUTTONDOWN:
                 if event.button == 1: self.player.weapons.switch()

            # Rastreamento de dedos
            if event.type == pygame.FINGERDOWN or event.type == pygame.FINGERMOTION:
                # AQUI ESTÁ O SEGREDO DO TOUCH PRECISO
                x, y = self.get_touch_pos(event)
                self.fingers[event.finger_id] = (x, y)
                
                # Clique único no botão SW (Switch)
                if event.type == pygame.FINGERDOWN:
                    if self.ui.btn_switch.collidepoint(x, y):
                        self.player.weapons.switch()

            if event.type == pygame.FINGERUP:
                if event.finger_id in self.fingers:
                    del self.fingers[event.finger_id]

        # Verifica D-PAD e Botão de Tiro
        for finger_pos in self.fingers.values():
            fx, fy = finger_pos
            if self.ui.btn_left.collidepoint(fx, fy): move_x = -1
            if self.ui.btn_right.collidepoint(fx, fy): move_x = 1
            if self.ui.btn_up.collidepoint(fx, fy): move_y = -1
            if self.ui.btn_down.collidepoint(fx, fy): move_y = 1
            
            if self.ui.btn_fire.collidepoint(fx, fy):
                shoot = True

        # Aplica movimento
        self.player.update_input(move_x, move_y)
        
        # Lógica de tiro
        if shoot:
            now = pygame.time.get_ticks()
            if now % 10 == 0: 
                self.player.trigger_shoot_anim() 
                w_type = self.player.weapons.get_current()
                if w_type == "VULCAN":
                    b1 = Projectile(self.player.rect.left + 10, self.player.rect.top, w_type)
                    b2 = Projectile(self.player.rect.right - 10, self.player.rect.top, w_type)
                    self.all_sprites.add(b1, b2); self.bullets.add(b1, b2)
                else:
                    b = Projectile(self.player.rect.centerx, self.player.rect.top, w_type)
                    self.all_sprites.add(b); self.bullets.add(b)

    def update_game(self):
        self.bg.update()
        self.all_sprites.update()
        self.level_manager.update()
        
        # Colisão Tiro -> Inimigo
        hits = pygame.sprite.groupcollide(self.enemies, self.bullets, False, True)
        for enemy, bullets in hits.items():
            for b in bullets:
                enemy.hp -= b.damage
                if enemy.hp <= 0:
                    expl = Explosion(enemy.rect.center)
                    self.all_sprites.add(expl)
                    enemy.kill()
        
        # Colisão Inimigo -> Jogador
        if pygame.sprite.spritecollide(self.player, self.enemies, True):
            self.player.hp -= 20
            self.all_sprites.add(Explosion(self.player.rect.center))
            if self.player.hp <= 0:
                self.state = 'MENU' 

    def draw_game(self):
        self.bg.draw(self.screen)
        self.all_sprites.draw(self.screen)
        self.ui.draw_hud(self.screen, self.player)

if __name__ == "__main__":
    g = Game()
    g.run()

