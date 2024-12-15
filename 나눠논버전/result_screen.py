import pygame

def results_screen(screen, score, accuracy, selected_music):
    WHITE = (255, 255, 255)
    GRAY = (190, 190, 190)
    font = pygame.font.Font(None, 60)
    small_font = pygame.font.Font(None, 40)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                running = False  # 결과창을 종료하고 메인 메뉴로 돌아갈 수 있음

        # 화면 그리기
        screen.fill((0, 0, 0))

        # 제목
        title_text = font.render("Game Results", True, WHITE)
        screen.blit(title_text, (screen.get_width() // 2 - title_text.get_width() // 2, 50))

        # 결과 표시
        music_text = small_font.render(f"Music: {selected_music}", True, WHITE)
        score_text = small_font.render(f"Score: {score}", True, WHITE)
        accuracy_text = small_font.render(f"Accuracy: {accuracy:.2f}%", True, WHITE)

        screen.blit(music_text, (100, 200))
        screen.blit(score_text, (100, 300))
        screen.blit(accuracy_text, (100, 400))

        # 종료 버튼
        exit_button_rect = pygame.Rect(540, 600, 200, 60)
        pygame.draw.rect(screen, GRAY, exit_button_rect)
        exit_text = small_font.render("Main Menu", True, WHITE)
        screen.blit(exit_text, exit_button_rect.move(50, 15).topleft)

        # 버튼 클릭 처리
        if event.type == pygame.MOUSEBUTTONDOWN and exit_button_rect.collidepoint(event.pos):
            running = False  # 메인 메뉴로 돌아가게 처리

        pygame.display.flip()
