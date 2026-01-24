import pygame
from settings import *

class Camera:
    def __init__(self, map_width, map_height):
        # A câmera é um retângulo que define o que está visível
        self.camera_rect = pygame.Rect(0, 0, WIDTH, HEIGHT)
        self.map_width = map_width
        self.map_height = map_height

    def apply(self, entity):
        # Pega um objeto do mundo e retorna sua posição na tela (com o deslocamento da câmera)
        # O "move" aplica o offset (topleft da câmera, que será negativo)
        return entity.rect.move(self.camera_rect.topleft)

    def update(self, target):
        # Calcula a posição ideal da câmera: centralizada no alvo (jogador)
        # Se o jogador está em (1000, 1000) e a tela tem 640 de largura,
        # queremos que o centro da tela (320) coincida com o 1000 do jogador.
        # Offset X = 320 - 1000 = -680.
        x = -target.rect.centerx + int(WIDTH / 2)
        y = -target.rect.centery + int(HEIGHT / 2)

        # LIMITES (Clamping): Impede que a câmera mostre área fora do mapa
        # A câmera nunca pode ir além de 0 na esquerda/topo
        # E nunca pode ir além do (tamanho do mapa - tamanho da tela) na direita/baixo
        x = min(0, max(-(self.map_width - WIDTH), x))
        y = min(0, max(-(self.map_height - HEIGHT), y))

        self.camera_rect = pygame.Rect(x, y, WIDTH, HEIGHT)
