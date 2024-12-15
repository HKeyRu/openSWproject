import pygame
from game_play import game_play_screen

def music_select_screen(screen):
    WHITE = (255, 255, 255)
    GRAY = (190, 190, 190)
    HIGHLIGHT_COLOR = (255, 0, 0)  # 선택된 항목 테두리 색상 (빨간색)

    font = pygame.font.Font(None, 40)
    music_list = ["YMCA", "Alone", "Shape of You"]
    music_buttons = [pygame.Rect(540, 150 + i * 100, 200, 60) for i in range(len(music_list))]

    selected_index = 0  # 기본 선택은 첫 번째 곡
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_index = (selected_index - 1) % len(music_list)  # 위 방향키
                elif event.key == pygame.K_DOWN:
                    selected_index = (selected_index + 1) % len(music_list)  # 아래 방향키
                elif event.key == pygame.K_RETURN:  # Enter 키로 음악 선택
                    selected_music = music_list[selected_index]
                    game_play_screen(screen, selected_music)  # 게임 화면으로 이동

        screen.fill((50, 50, 50))  # 배경 색상
        title_text = font.render("Select Music", True, WHITE)
        screen.blit(title_text, (540, 50))

        # 각 음악 항목 그리기
        for i, button in enumerate(music_buttons):
            pygame.draw.rect(screen, GRAY, button)  # 기본 버튼 색상
            if i == selected_index:  # 선택된 항목에만 빨간색 테두리 추가
                pygame.draw.rect(screen, HIGHLIGHT_COLOR, button, 5)  # 테두리 두께 5

            music_text = font.render(music_list[i], True, WHITE)
            # 텍스트를 버튼의 중앙에 정렬
            text_rect = music_text.get_rect(center=button.center)
            screen.blit(music_text, text_rect)

        pygame.display.flip()
