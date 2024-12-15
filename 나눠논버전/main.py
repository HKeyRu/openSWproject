import pygame
from main_menu import main_menu_screen

# Pygame 초기화
pygame.init()
screen_width, screen_height = 1280, 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("포징 투 댄스")

# 메인 메뉴 실행
main_menu_screen(screen)
