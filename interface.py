import pygame
from settings import *

class UIManager:
    def __init__(self):
        self.scr_w, self.scr_h = WIDTH, HEIGHT

        # Fontes
        self.font_big = pygame.font.SysFont("arial", 40, bold=True)
        self.font_small = pygame.font.SysFont("arial", 15, bold=True)
        self.font_icon = pygame.font.SysFont("arial", 25, bold=True)
        
        # --- MARGEM DE SEGURANÇA REFORÇADA ---
        # Aumentei para 60px. Isso empurra os controles para longe da borda curva.
        SAFE_MARGIN_X = 60 
        SAFE_MARGIN_Y = 30
        
        # --- MENU PRINCIPAL ---
        cx, cy = self.scr_w // 2, self.scr_h // 2
        self.btn_campanha = pygame.Rect(cx - 100, cy - 30, 200, 40)
        self.btn_missao = pygame.Rect(cx - 100, cy + 20, 200, 40)
        
        # --- SELEÇÃO DE AVIÕES ---
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

        # --- HUD (CONTROLES) ---
        btn_size = 50 
        pad = 5
        
        # D-PAD (Esquerda) - Empurrado para a direita (SAFE_MARGIN_X)
        base_x = SAFE_MARGIN_X
        base_y = self.scr_h - (btn_size * 3) - SAFE_MARGIN_Y
        
        self.btn_up = pygame.Rect(base_x + btn_size + pad, base_y, btn_size, btn_size)
        self.btn_left = pygame.Rect(base_x, base_y + btn_size + pad, btn_size, btn_size)
        self.btn_down = pygame.Rect(base_x + btn_size + pad, base_y + (btn_size * 2) + (pad * 2), btn_size, btn_size)
        self.btn_right = pygame.Rect(base_x + (btn_size * 2) + (pad * 2), base_y + btn_size + pad, btn_size, btn_size)
        
        # BOTÕES DE AÇÃO (Direita) - Empurrados para a esquerda
        fire_size = 70
        self.btn_fire = pygame.Rect(
            self.scr_w - fire_size - SAFE_MARGIN_X, # Mais longe da borda direita
            self.scr_h - fire_size - SAFE_MARGIN_Y, # Mais longe da borda inferior
            fire_size, fire_size
        )
        
        switch_size = 45
        self.btn_switch = pygame.Rect(
            self.scr_w - switch_size - SAFE_MARGIN_X - 10, 
            self.btn_fire.top - switch_size - 15, 
            switch_size, switch_size
        )

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

    def draw_hud(self, screen, player):
        # Barra de Vida - Empurrada para a direita
        margin_hud = 60
        pygame.draw.rect(screen, (100,0,0), (margin_hud, 20, 150, 15))
        pct = player.hp / player.max_hp
        if pct < 0: pct = 0
        pygame.draw.rect(screen, GREEN, (margin_hud, 20, 150 * pct, 15))
        pygame.draw.rect(screen, WHITE, (margin_hud, 20, 150, 15), 1)
        
        txt = self.font_small.render(f"ARMA: {player.weapons.get_current()}", True, WHITE)
        screen.blit(txt, (margin_hud, 40))

        # Controles
        self._draw_dpad_btn(screen, self.btn_left, "<")
        self._draw_dpad_btn(screen, self.btn_right, ">")
        self._draw_dpad_btn(screen, self.btn_up, "^")
        self._draw_dpad_btn(screen, self.btn_down, "v")
        
        self._draw_circle_button(screen, self.btn_fire, (200, 50, 50), "FIRE")
        self._draw_circle_button(screen, self.btn_switch, (0, 150, 150), "SW")

    def _draw_glossy_button(self, screen, rect, color, text):
        pygame.draw.rect(screen, color, rect, border_radius=8)
        pygame.draw.rect(screen, WHITE, rect, 1, border_radius=8)
        txt = self.font_small.render(text, True, WHITE)
        screen.blit(txt, (rect.centerx - txt.get_width()//2, rect.centery - txt.get_height()//2))

    def _draw_dpad_btn(self, screen, rect, symbol):
        s = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        pygame.draw.circle(s, (255, 255, 255, 40), (rect.width//2, rect.height//2), rect.width//2)
        pygame.draw.circle(s, WHITE, (rect.width//2, rect.height//2), rect.width//2, 1)
        screen.blit(s, rect.topleft)
        txt = self.font_icon.render(symbol, True, WHITE)
        screen.blit(txt, (rect.centerx - txt.get_width()//2, rect.centery - txt.get_height()//2))

    def _draw_circle_button(self, screen, rect, color, text):
        s = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        pygame.draw.circle(s, (*color, 180), (rect.width//2, rect.height//2), rect.width//2)
        pygame.draw.circle(s, WHITE, (rect.width//2, rect.height//2), rect.width//2, 1)
        screen.blit(s, rect.topleft)
        txt = self.font_small.render(text, True, WHITE)
        screen.blit(txt, (rect.centerx - txt.get_width()//2, rect.centery - txt.get_height()//2))
