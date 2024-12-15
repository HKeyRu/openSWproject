import pygame
import cv2
import mediapipe as mp

pygame.mixer.init()
pygame.mixer.music.load("ymca.mp3")

def game_play_screen(screen, selected_music):
    WHITE = (255, 255, 255)
    font = pygame.font.Font(None, 40)
    
    # OpenCV 웹캠 초기화
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("웹캠을 열 수 없습니다!")
        return

    # Mediapipe 초기화
    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

    song_start = pygame.USEREVENT + 1
    pygame.time.set_timer(song_start, 3000)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == song_start: # 노래 재생
                pygame.mixer.music.play()
        # OpenCV로 프레임 읽기
        ret, frame = cap.read()
        if not ret:
            print("웹캠 프레임을 읽을 수 없습니다!")
            break
        
        

        # Mediapipe로 포즈 감지
        frame = cv2.cvtColor(cv2.flip(frame, 1), cv2.COLOR_BGR2RGB)
        results = pose.process(frame)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        # OpenCV 이미지를 Pygame에서 사용할 수 있게 변환
        frame_resized = cv2.resize(frame, (1280, 720))
        frame_resized = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)
        frame_surface = pygame.surfarray.make_surface(frame_resized)
        frame_surface = pygame.transform.rotate(frame_surface, -90)

        # Pygame 화면에 그리기
        screen.blit(frame_surface, (0, 0))


        # 선택된 음악 표시
        music_text = font.render(f"Playing: {selected_music}", True, WHITE)
        screen.blit(music_text, (50, 50))

        pygame.display.flip()

    cap.release()
    pose.close()
