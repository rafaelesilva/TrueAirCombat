import pygame
from settings import *

class UIManager:
    def __init__(self):
        self.scr_w, self.scr_h = WIDTH, HEIGHT

        self.font_big = pygame.font.SysFont("arial", 40, bold=True)
        self.font_small = pygame.font.SysFont("arial", 15, bold=True)
        self.font_icon = pygame.font.SysFont("arial", 25, bold=True)
        
        # Margens
        SAFE_MARGIN_X = 60 
        SAFE_MARGIN_Y = 30
        
        # --- RADAR ---
        self.radar_size = 100
        self.radar_rect = pygame.Rect(SAFE_MARGIN_X, 60, self.radar_size, self.radar_size)
        
        # --- MENU ---
        cx, cy = self.scr_w // 2, self.scr_h // 2
        self.btn_campanha = pygame.Rect(cx - 100, cy - 30, 200, 40)
        self.btn_missao = pygame.Rect(cx - 100, cy + 20, 200, 40)
        
        # --- SELEÇÃO ---
        self.plane_buttons = []
        plane_names = list(AIRCRAFT_DATA.keys())
        cols = 4
        btn_w = (self.scr_w - (cols + 1) * 10) // cols
        btn_h = 30
        start_y = 80
        for i, name in enumerate(plane_names):
            c = i % cols
            r = i // cols
            x = 10 + c * (btn_w + 10)
            y = start_y + r * (btn_h + 10)
            rect = pygame.Rect(x, y, btn_w, btn_h)
            display_name = name.split(' ')[0]
            self.plane_buttons.append({'name': name, 'display': display_name, 'rect': rect})

        # --- D-PAD ESTILO MEGA DRIVE (TRANSPARENTE) ---
        btn_size = 50 
        base_x = SAFE_MARGIN_X
        base_y = self.scr_h - (btn_size * 3) - SAFE_MARGIN_Y
        
        # O Centro do direcional
        self.dpad_center = (base_x + btn_size + 5 + btn_size//2, base_y + btn_size + 5 + btn_size//2)
        self.dpad_radius = int(btn_size * 1.8)
        
        # Posições apenas para desenhar as setinhas (decorativo)
        pad = 5
        self.vis_up = (self.dpad_center[0], self.dpad_center[1] - btn_size)
        self.vis_down = (self.dpad_center[0], self.dpad_center[1] + btn_size)
        self.vis_left = (self.dpad_center[0] - btn_size, self.dpad_center[1])
        self.vis_right = (self.dpad_center[0] + btn_size, self.dpad_center[1])
        
        # --- BOTÕES DE AÇÃO (DIREITA) ---
        # CORREÇÃO CRÍTICA: Definir pelo CENTRO para alinhar Hitbox e Visual
        fire_radius = 40 # Raio do botão visual
        fire_center_x = self.scr_w - fire_radius - SAFE_MARGIN_X
        fire_center_y = self.scr_h - fire_radius - SAFE_MARGIN_Y
        self.fire_center = (fire_center_x, fire_center_y)
        self.fire_radius = fire_radius
        
        # A hitbox é um retângulo centrado no mesmo ponto, mas maior
        hitbox_size = 120 
        self.btn_fire_hitbox = pygame.Rect(0, 0, hitbox_size, hitbox_size)
        self.btn_fire_hitbox.center = self.fire_center
        
        # Botão Switch (Menor, acima e a esquerda do Fire)
        sw_radius = 25
        sw_center_x = fire_center_x - 70
        sw_center_y = fire_center_y + 20
        self.sw_center = (sw_center_x, sw_center_y)
        self.sw_radius = sw_radius
        
        self.btn_switch_hitbox = pygame.Rect(0, 0, 80, 80)
        self.btn_switch_hitbox.center = self.sw_center

    def draw_menu(self, screen):
        screen.fill((30, 30, 30))
        title = self.font_big.render(TITLE, True, YELLOW)
        screen.blit(title, (self.scr_w//2 - title.get_width()//2, 20))
        self._draw_glossy_button(screen, self.btn_campanha, (0, 100, 200), "JOGAR")
        self._draw_glossy_button(screen, self.btn_missao, (0, 100, 200), "MISSÃO")

    def draw_select(self, screen):
        screen.fill((20, 20, 40))
        title = self.font_big.render("ESCOLHA:", True, WHITE)
        screen.blit(title, (self.scr_w//2 - title.get_width()//2, 20))
        for btn in self.plane_buttons:
            rect = btn['rect']
            color = (0, 80, 0) if 'Gripen' in btn['name'] else (60, 60, 60)
            pygame.draw.rect(screen, color, rect, border_radius=5)
            pygame.draw.rect(screen, WHITE, rect, 1, border_radius=5)
            txt = pygame.font.SysFont("arial", 10, bold=True).render(btn['display'], True, WHITE)
            screen.blit(txt, (rect.centerx - txt.get_width()//2, rect.centery - txt.get_height()//2))

    def draw_radar(self, screen, player, enemies):
        # Radar Transparente
        radar_surf = pygame.Surface((self.radar_size, self.radar_size), pygame.SRCALPHA)
        radar_surf.fill((0, 20, 0, 100)) # Verde escuro muito transparente
        pygame.draw.rect(radar_surf, (0, 255, 0, 150), (0,0,self.radar_size, self.radar_size), 2)
        
        scale_x = self.radar_size / MAP_WIDTH
        scale_y = self.radar_size / MAP_HEIGHT
        
        for enemy in enemies:
            ex = int(enemy.rect.centerx * scale_x)
            ey = int(enemy.rect.centery * scale_y)
            if 0 <= ex <= self.radar_size and 0 <= ey <= self.radar_size:
                pygame.draw.circle(radar_surf, (255, 0, 0, 200), (ex, ey), 2)
        
        px = int(player.rect.centerx * scale_x)
        py = int(player.rect.centery * scale_y)
        pygame.draw.circle(radar_surf, (0, 255, 0, 200), (px, py), 3)
        
        screen.blit(radar_surf, self.radar_rect.topleft)
        txt = pygame.font.SysFont("arial", 10, bold=True).render("RADAR", True, (0, 255, 0))
        screen.blit(txt, (self.radar_rect.x, self.radar_rect.y - 12))

    def draw_hud(self, screen, player, enemies):
        # Barra de Vida
        margin_hud = 60
        pygame.draw.rect(screen, (100,0,0), (margin_hud, 20, 150, 15))
        pct = player.hp / player.max_hp
        if pct < 0: pct = 0
        pygame.draw.rect(screen, GREEN, (margin_hud, 20, 150 * pct, 15))
        pygame.draw.rect(screen, WHITE, (margin_hud, 20, 150, 15), 1)
        txt = self.font_small.render(f"ARMA: {player.weapons.get_current()}", True, WHITE)
        screen.blit(txt, (margin_hud, 40))

        # --- DESENHO TRANSPARENTE DO D-PAD ---
        # Cria uma superfície separada para poder usar Alpha (transparência)
        dpad_surf = pygame.Surface((self.dpad_radius*2, self.dpad_radius*2), pygame.SRCALPHA)
        
        # Fundo do D-Pad (Preto semi-transparente)
        pygame.draw.circle(dpad_surf, (0, 0, 0, 80), (self.dpad_radius, self.dpad_radius), self.dpad_radius)
        # Borda
        pygame.draw.circle(dpad_surf, (200, 200, 200, 100), (self.dpad_radius, self.dpad_radius), self.dpad_radius, 2)
        
        # Cola o D-Pad na tela
        screen.blit(dpad_surf, (self.dpad_center[0] - self.dpad_radius, self.dpad_center[1] - self.dpad_radius))
        
        # Desenha as setas (Letras)
        self._draw_text_at(screen, "^", self.vis_up)
        self._draw_text_at(screen, "v", self.vis_down)
        self._draw_text_at(screen, "<", self.vis_left)
        self._draw_text_at(screen, ">", self.vis_right)
        
        # --- BOTÕES AÇÃO TRANSPARENTES ---
        self._draw_transparent_circle(screen, self.fire_center, self.fire_radius, (200, 50, 50, 100), "FIRE")
        self._draw_transparent_circle(screen, self.sw_center, self.sw_radius, (0, 150, 150, 100), "SW")
        
        # (Debug Visual: Se quiser ver as hitboxes quadradas, descomente abaixo)
        # pygame.draw.rect(screen, (255, 255, 0), self.btn_fire_hitbox, 1)
        
        self.draw_radar(screen, player, enemies)

    def _draw_glossy_button(self, screen, rect, color, text):
        pygame.draw.rect(screen, color, rect, border_radius=8)
        pygame.draw.rect(screen, WHITE, rect, 1, border_radius=8)
        txt = self.font_small.render(text, True, WHITE)
        screen.blit(txt, (rect.centerx - txt.get_width()//2, rect.centery - txt.get_height()//2))

    def _draw_text_at(self, screen, text, center_pos):
        txt = self.font_icon.render(text, True, (255, 255, 255, 150))
        screen.blit(txt, (center_pos[0] - txt.get_width()//2, center_pos[1] - txt.get_height()//2))

    def _draw_transparent_circle(self, screen, center, radius, color_rgba, text):
        # Superfície temporária para transparência
        s = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
        # Círculo preenchido
        pygame.draw.circle(s, color_rgba, (radius, radius), radius)
        # Borda Branca
        pygame.draw.circle(s, (255, 255, 255, 150), (radius, radius), radius, 2)
        
        # Cola na tela principal
        screen.blit(s, (center[0] - radius, center[1] - radius))
        
        # Texto
        txt = self.font_small.render(text, True, (255, 255, 255, 200))
        screen.blit(txt, (center[0] - txt.get_width()//2, center[1] - txt.get_height()//2))
