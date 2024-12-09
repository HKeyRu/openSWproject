import pygame
import cv2
import sys

# Pygame 초기화
pygame.init()

# 화면 크기 설정 (1280x720 해상도)
screen_width, screen_height = 1280, 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("대충 게임이름")

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (190, 190, 190)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# OpenCV 웹캠 초기화
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("웹캠을 열 수 없습니다!")
    sys.exit()

# 웹캠의 비율 유지하기 위한 원본 크기 구하기
cap_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
cap_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# 버튼 위치와 크기 (1280x720 해상도에 맞게 적당히 배치)
start_button_rect = pygame.Rect(540, 550, 200, 60)  # Start 버튼
quit_button_rect = pygame.Rect(540, 630, 200, 60)   # Quit 버튼

# 게임 루프
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # 버튼 클릭 이벤트 처리
        if event.type == pygame.MOUSEBUTTONDOWN:
            if start_button_rect.collidepoint(event.pos):
                print("게임 시작!")  # Start 버튼 클릭 시
            elif quit_button_rect.collidepoint(event.pos):
                print("게임 종료!")  # Quit 버튼 클릭 시
                running = False

    # OpenCV로 프레임 읽기
    ret, frame = cap.read()
    if not ret:
        print("웹캠 프레임을 읽을 수 없습니다!")
        break

    # 웹캠 영상 비율 유지하면서 화면에 맞게 크기 조정
    aspect_ratio = cap_width / cap_height  # 원본 영상 비율 계산
    new_width = screen_width
    new_height = int(screen_width / aspect_ratio)

    if new_height > screen_height:  # 화면 크기를 넘지 않도록 조정
        new_height = screen_height
        new_width = int(screen_height * aspect_ratio)

    frame_resized = cv2.resize(frame, (new_width, new_height))

    # OpenCV 이미지를 Pygame에서 사용할 수 있게 변환 (BGR -> RGB)
    frame_resized = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)
    
    # 90도 회전 (웹캠이 90도 회전되어 있는 버그 수정)
    frame_resized = pygame.transform.rotate(pygame.surfarray.make_surface(frame_resized), 270)

    # Pygame 화면에 웹캠 배경 그리기 (중앙에 배치)
    frame_x = (screen_width - new_width) // 2
    frame_y = (screen_height - new_height) // 2
    screen.blit(frame_resized, (frame_x, frame_y))

    # 게임 제목 그리기
    font = pygame.font.Font(None, 60)
    title_text = font.render("Game Name", True, WHITE)
    title_rect = title_text.get_rect(center=(screen_width // 2, 100))
    screen.blit(title_text, title_rect)

    # Start 버튼 그리기
    pygame.draw.rect(screen, GRAY, start_button_rect)  # Start 버튼 배경
    start_text = font.render("Start", True, WHITE)
    start_text_rect = start_text.get_rect(center=start_button_rect.center)
    screen.blit(start_text, start_text_rect)

    # Quit 버튼 그리기
    pygame.draw.rect(screen, GRAY, quit_button_rect)  # Quit 버튼 배경
    quit_text = font.render("Quit", True, WHITE)
    quit_text_rect = quit_text.get_rect(center=quit_button_rect.center)
    screen.blit(quit_text, quit_text_rect)

    # 화면 업데이트
    pygame.display.flip()

# 종료 처리
cap.release()
pygame.quit()
