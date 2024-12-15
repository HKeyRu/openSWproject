import pygame
import cv2
from music_select import music_select_screen

def main_menu_screen(screen):
    WHITE = (255, 255, 255)
    GRAY = (190, 190, 190)

    # OpenCV 웹캠 초기화
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("웹캠을 열 수 없습니다!")
        return

    font = pygame.font.Font(None, 50)
    start_button_rect = pygame.Rect(540, 550, 200, 60)
    quit_button_rect = pygame.Rect(540, 630, 200, 60)

    running = True
    while running:
        # Pygame 이벤트 처리
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button_rect.collidepoint(event.pos):
                    music_select_screen(screen)  # 곡 선택 화면으로 이동
                elif quit_button_rect.collidepoint(event.pos):
                    running = False

        # OpenCV로 프레임 읽기
        ret, frame = cap.read()
        if not ret:
            print("웹캠 프레임을 읽을 수 없습니다!")
            break

        # OpenCV 프레임 처리
        frame = cv2.cvtColor(cv2.flip(frame, 1), cv2.COLOR_BGR2RGB)
        frame_resized = cv2.resize(frame, (screen.get_width(), screen.get_height()))
        frame_surface = pygame.surfarray.make_surface(frame_resized)
        frame_surface = pygame.transform.rotate(frame_surface, -90)  # 필요한 경우 회전

        # 배경에 웹캠 화면 그리기
        screen.blit(frame_surface, (0, 0))

        # 버튼 그리기
        pygame.draw.rect(screen, GRAY, start_button_rect)
        pygame.draw.rect(screen, GRAY, quit_button_rect)

        # 버튼 텍스트를 중앙 정렬
        start_text = font.render("Start", True, WHITE)
        quit_text = font.render("Quit", True, WHITE)
        start_text_rect = start_text.get_rect(center=start_button_rect.center)
        quit_text_rect = quit_text.get_rect(center=quit_button_rect.center)
        screen.blit(start_text, start_text_rect)
        screen.blit(quit_text, quit_text_rect)

        pygame.display.flip()

    cap.release()
    pygame.quit()
