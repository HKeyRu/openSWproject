import pygame
from game_play import game_play_screen

def music_select_screen(screen):
    WHITE = (255, 255, 255)
    GRAY = (190, 190, 190)

    font = pygame.font.Font(None, 40)
    music_list = ["Song 1", "Song 2", "Song 3"]
    music_buttons = [pygame.Rect(540, 150 + i * 100, 200, 60) for i in range(len(music_list))]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, button in enumerate(music_buttons):
                    if button.collidepoint(event.pos):
                        selected_music = music_list[i]
                        game_play_screen(screen, selected_music)  # 게임 화면으로 이동

        screen.fill((50, 50, 50))
        title_text = font.render("Select Music", True, WHITE)
        screen.blit(title_text, (540, 50))

        for i, button in enumerate(music_buttons):
            pygame.draw.rect(screen, GRAY, button)
            music_text = font.render(music_list[i], True, WHITE)
            screen.blit(music_text, button.move(50, 15).topleft)

        pygame.display.flip()
