import pygame
from main_menu import main_menu_screen

# Pygame 초기화
screen_width, screen_height = 1280, 720
screen = pygame.display.set_mode((screen_width, screen_height))

def results_screen(screen, perfect, note, selected_music):
    WHITE = (255, 255, 255)
    GRAY = (190, 190, 190)
    HIGHLIGHT_COLOR = (255, 0, 0)  # 선택된 항목 테두리 색상 (빨간색)

    font = pygame.font.Font(None, 60)
    small_font = pygame.font.Font(None, 40)
    exit_button_rect = pygame.Rect(540, 600, 200, 60)  # 종료 버튼 위치

    selected_index = 0  # 선택된 버튼의 초기값
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Enter 키로 음악 선택
                    if selected_index == 0:  # 메인 메뉴 선택
                        main_menu_screen(screen)
                        running = False

        # 화면 그리기
        screen.fill((0, 0, 0))

        # 제목
        title_text = font.render("Game Results", True, WHITE)
        screen.blit(title_text, (screen.get_width() // 2 - title_text.get_width() // 2, 50))

        # 결과 표시
        music_text = small_font.render(f"Music: {selected_music}", True, WHITE)
        score_text = small_font.render(f"Score: {(perfect/note)*10000000:.0f}", True, WHITE)

        screen.blit(music_text, (100, 200))
        screen.blit(score_text, (100, 300))

        # 종료 버튼
        pygame.draw.rect(screen, GRAY, exit_button_rect)  # 기본 버튼 색상
        if selected_index == 0:  # 선택된 항목에만 빨간색 테두리 추가
            pygame.draw.rect(screen, HIGHLIGHT_COLOR, exit_button_rect, 5)  # 테두리 두께 5

        exit_text = small_font.render("Main Menu", True, WHITE)
        text_rect = exit_text.get_rect(center=exit_button_rect.center)
        screen.blit(exit_text, text_rect)

        pygame.display.flip()
