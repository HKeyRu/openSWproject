import pygame
import cv2
import mediapipe as mp
from music_select import music_select_screen

def main_menu_screen(screen):
    WHITE = (255, 255, 255)
    GRAY = (190, 190, 190)
    HIGHLIGHT_COLOR = (255, 0, 0)  # 선택된 항목 테두리 색상 (빨간색)

    # OpenCV 웹캠 초기화
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    if not cap.isOpened():
        print("웹캠을 열 수 없습니다!")
        return

    # Mediapipe 초기화
    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

    font = pygame.font.Font(None, 50)
    start_button_rect = pygame.Rect(540, 550, 200, 60)
    quit_button_rect = pygame.Rect(540, 630, 200, 60)

    # 게임 제목 텍스트 설정
    title_font = pygame.font.Font(None, 70)  # 큰 폰트 크기 설정
    title_text = title_font.render("Game Name", True, WHITE)  # 게임 이름 텍스트 렌더링
    title_text_rect = title_text.get_rect(center=(640, 120))  # 중앙에 위치

    # 선택된 버튼 인덱스 초기화 (0: Start, 1: Quit)
    selected_button = 0

    running = True
    while running:
        # Pygame 이벤트 처리
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_button = 0  # 위 방향키 -> Start 선택
                elif event.key == pygame.K_DOWN:
                    selected_button = 1  # 아래 방향키 -> Quit 선택
                elif event.key == pygame.K_RETURN:  # Enter 키로 선택
                    if selected_button == 0:
                        music_select_screen(screen)  # Start 클릭
                    elif selected_button == 1:
                        running = False  # Quit 클릭

        # OpenCV로 프레임 읽기
        ret, frame = cap.read()
        if not ret:
            print("웹캠 프레임을 읽을 수 없습니다!")
            break

        # Mediapipe로 포즈 감지
        frame_rgb = cv2.cvtColor(cv2.flip(frame, 1), cv2.COLOR_BGR2RGB)  # BGR -> RGB로 변환
        results = pose.process(frame_rgb)

        # 포즈 랜드마크를 웹캠 이미지 위에 그리기
        if results.pose_landmarks:
            mp_drawing.draw_landmarks(
                image=frame_rgb,
                landmark_list=results.pose_landmarks,
                connections=mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
                connection_drawing_spec=mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2)
            )

        # OpenCV 이미지를 Pygame에서 사용할 수 있게 변환
        frame_resized = cv2.resize(frame_rgb, (1280, 720))  # 1280x720 해상도에 맞게 조정
        frame_surface = pygame.surfarray.make_surface(frame_resized)  # NumPy 배열을 Pygame 서페이스로 변환

        # OpenCV 이미지는 RGB, Pygame은 RGB 순서로 사용하므로 색상이 정상적으로 표시됨
        frame_surface = pygame.transform.rotate(frame_surface, -90)  # 필요한 경우 회전

        # 배경에 웹캠 화면 그리기
        screen.blit(frame_surface, (0, 0))

        # 게임 제목 텍스트 그리기
        screen.blit(title_text, title_text_rect)

        # 버튼 배경 그리기
        pygame.draw.rect(screen, GRAY, start_button_rect)
        pygame.draw.rect(screen, GRAY, quit_button_rect)

        # 선택된 버튼에 빨간색 테두리 그리기
        if selected_button == 0:
            pygame.draw.rect(screen, HIGHLIGHT_COLOR, start_button_rect, 5)  # 빨간 테두리
        if selected_button == 1:
            pygame.draw.rect(screen, HIGHLIGHT_COLOR, quit_button_rect, 5)  # 빨간 테두리

        # 버튼 텍스트를 중앙 정렬
        start_text = font.render("Start", True, WHITE)
        quit_text = font.render("Quit", True, WHITE)
        start_text_rect = start_text.get_rect(center=start_button_rect.center)
        quit_text_rect = quit_text.get_rect(center=quit_button_rect.center)
        screen.blit(start_text, start_text_rect)
        screen.blit(quit_text, quit_text_rect)

        pygame.display.flip()

    cap.release()
    pose.close()
    pygame.quit()
