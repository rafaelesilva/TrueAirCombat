import pygame
from settings import *

class UIManager:
    def __init__(self):
        # --- DETECÇÃO INTELIGENTE DE TAMANHO ---
        # Em vez de confiar no settings, perguntamos para a janela o tamanho real dela.
        screen = pygame.display.get_surface()
        if screen:
            self.scr_w, self.scr_h = screen.get_size()
        else:
            self.scr_w, self.scr_h = WIDTH, HEIGHT # Fallback

        # Fontes
        self.font_big = pygame.font.SysFont("arial", int(40 * SCALE), bold=True)
        self.font_small = pygame.font.SysFont("arial", int(20 * SCALE), bold=True)
        self.font_icon = pygame.font.SysFont("arial", int(30 * SCALE), bold=True)
        
        # --- MENU PRINCIPAL (Centralizado) ---
        cx, cy = self.scr_w // 2, self.scr_h // 2
        self.btn_campanha = pygame.Rect(cx - 150, cy - 60, 300, 50)
        self.btn_missao = pygame.Rect(cx - 150, cy + 10, 300, 50)
        
        # --- SELEÇÃO DE AVIÕES ---
        self.plane_buttons = []
        plane_names = list(AIRCRAFT_DATA.keys())
        
        cols = 4
        # Usa a largura real para calcular colunas
        btn_w = (self.scr_w - (cols + 1) * 20) // cols
        btn_h = 50
        start_y = 100
        
        for i, name in enumerate(plane_names):
            c = i % cols
            r = i // cols
            x = 20 + c * (btn_w + 20)
            y = start_y + r * (btn_h + 20)
            rect = pygame.Rect(x, y, btn_w, btn_h)
            self.plane_buttons.append({'name': name, 'rect': rect})

        # --- HUD (CONTROLES) ---
        btn_size = int(60 * SCALE)
        pad = 10
        # Aumentei a margem para 30 para fugir de cantos arredondados/câmeras
        margin = 30 
        
        # D-PAD (Esquerda)
        base_x = margin
        base_y = self.scr_h - (btn_size * 3) - margin
        
        self.btn_up = pygame.Rect(base_x + btn_size + pad, base_y, btn_size, btn_size)
        self.btn_left = pygame.Rect(base_x, base_y + btn_size + pad, btn_size, btn_size)
        self.btn_down = pygame.Rect(base_x + btn_size + pad, base_y + (btn_size * 2) + (pad * 2), btn_size, btn_size)
        self.btn_right = pygame.Rect(base_x + (btn_size * 2) + (pad * 2), base_y + btn_size + pad, btn_size, btn_size)
        
        # BOTÕES DE AÇÃO (Direita) - Usando self.scr_w para colar na direita certa
        fire_size = int(80 * SCALE)
        self.btn_fire = pygame.Rect(self.scr_w - fire_size - margin, self.scr_h - fire_size - margin, fire_size, fire_size)
        
        switch_size = int(50 * SCALE)
        # Posiciona o botão de troca acima do botão de tiro
        self.btn_switch = pygame.Rect(self.scr_w - switch_size - margin - 15, self.scr_h - fire_size - margin - switch_size - 20, switch_size, switch_size)

    def draw_menu(self, screen):
        screen.fill((30, 30, 30))
        title = self.font_big.render(TITLE, True, YELLOW)
        screen.blit(title, (self.scr_w//2 - title.get_width()//2, 30))
        
        self._draw_glossy_button(screen, self.btn_campanha, (0, 100, 200), "JOGAR")
        self._draw_glossy_button(screen, self.btn_missao, (0, 100, 200), "MISSÃO")

    def draw_select(self, screen):
        screen.fill((20, 20, 40))
        title = self.font_big.render("ESCOLHA SUA AERONAVE", True, WHITE)
        screen.blit(title, (self.scr_w//2 - title.get_width()//2, 20))
        
        for btn in self.plane_buttons:
            name = btn['name']
            rect = btn['rect']
            color = (0, 80, 0) if 'Gripen' in name else (60, 60, 60)
            pygame.draw.rect(screen, color, rect, border_radius=5)
            pygame.draw.rect(screen, WHITE, rect, 2, border_radius=5)
            
            txt = pygame.font.SysFont("arial", int(16*SCALE)).render(name, True, WHITE)
            screen.blit(txt, (rect.centerx - txt.get_width()//2, rect.centery - txt.get_height()//2))

    def draw_hud(self, screen, player):
        # Barra de Vida
        pygame.draw.rect(screen, (100,0,0), (20, 20, 200, 20))
        pct = player.hp / player.max_hp
        if pct < 0: pct = 0
        pygame.draw.rect(screen, GREEN, (20, 20, 200 * pct, 20))
        pygame.draw.rect(screen, WHITE, (20, 20, 200, 20), 2)
        
        txt = self.font_small.render(f"ARMA: {player.weapons.get_current()}", True, WHITE)
        screen.blit(txt, (20, 45))

        # Controles
        self._draw_dpad_btn(screen, self.btn_left, "<")
        self._draw_dpad_btn(screen, self.btn_right, ">")
        self._draw_dpad_btn(screen, self.btn_up, "^")
        self._draw_dpad_btn(screen, self.btn_down, "v")
        
        self._draw_circle_button(screen, self.btn_fire, (200, 50, 50), "FIRE")
        self._draw_circle_button(screen, self.btn_switch, (0, 150, 150), "SW")

    def _draw_glossy_button(self, screen, rect, color, text):
        pygame.draw.rect(screen, color, rect, border_radius=10)
        pygame.draw.rect(screen, WHITE, rect, 2, border_radius=10)
        txt = self.font_small.render(text, True, WHITE)
        screen.blit(txt, (rect.centerx - txt.get_width()//2, rect.centery - txt.get_height()//2))

    def _draw_dpad_btn(self, screen, rect, symbol):
        s = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        pygame.draw.circle(s, (255, 255, 255, 40), (rect.width//2, rect.height//2), rect.width//2)
        pygame.draw.circle(s, WHITE, (rect.width//2, rect.height//2), rect.width//2, 2)
        screen.blit(s, rect.topleft)
        txt = self.font_icon.render(symbol, True, WHITE)
        screen.blit(txt, (rect.centerx - txt.get_width()//2, rect.centery - txt.get_height()//2))

    def _draw_circle_button(self, screen, rect, color, text):
        s = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        pygame.draw.circle(s, (*color, 180), (rect.width//2, rect.height//2), rect.width//2)
        pygame.draw.circle(s, WHITE, (rect.width//2, rect.height//2), rect.width//2, 2)
        screen.blit(s, rect.topleft)
        txt = self.font_small.render(text, True, WHITE)
        screen.blit(txt, (rect.centerx - txt.get_width()//2, rect.centery - txt.get_height()//2))
