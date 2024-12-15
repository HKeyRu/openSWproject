import pygame
from result_screen import results_screen

pygame.init()
screen_width, screen_height = 1280, 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pose Detection Game")

perfect = 88 # 임의로 설정한 수들
notes = 90

# 메인 메뉴 실행
results_screen(screen, perfect, notes, "YMCA")