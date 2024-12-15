import pygame
import cv2
import sys
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
    song_started = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == song_start and not song_started: # 노래 재생
                pygame.mixer.music.play()
                song_started = True
        # OpenCV로 프레임 읽기
        ret, frame = cap.read()
        if not ret:
            print("웹캠 프레임을 읽을 수 없습니다!")
            break
        
        

        # Mediapipe로 포즈 감지
        frame = cv2.cvtColor(cv2.flip(frame, 1), cv2.COLOR_BGR2RGB)
        results = pose.process(frame)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        # 포즈 랜드마크가 감지되면 표시
        if results.pose_landmarks:
            mp_drawing.draw_landmarks(
                image=frame,
                landmark_list=results.pose_landmarks,
                connections=mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=2),
                connection_drawing_spec=mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2)
            )

        # OpenCV 이미지를 Pygame에서 사용할 수 있게 변환
        frame_resized = cv2.resize(frame, (1280, 720))
        frame_resized = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)
        frame_surface = pygame.surfarray.make_surface(frame_resized)
        frame_surface = pygame.transform.rotate(frame_surface, -90)

        #Mediapipe 포즈 
        if results.pose_landmarks:
            left_wrist_x = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST].x
            right_wrist_x = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST].x

            left_wrist_y = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST].y
            right_wrist_y = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST].y
            left_shoulder_y = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].y
            left_elbow_y = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ELBOW].y
            right_shoulder_y = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].y
            right_elbow_y = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ELBOW].y

            #왼,오른손 들기
            if (left_wrist_y < 0.5 and left_shoulder_y > left_elbow_y):
                text = "Left Hand Up"
            elif (right_wrist_y < 0.5 and right_shoulder_y > right_elbow_y):
                text = "Right Hand Up"
            else:
                text = "No Hands Up"

            status_text = font.render(text, True, WHITE)
            screen.blit(status_text, (50, 50))

            #박수
            if(abs(left_wrist_x - right_wrist_x) < 0.2):
                text1 = "Clap"
            else:
                text1 = "no Clap"

            clap_text = font.render(text1, True, WHITE)
            screen.blit(clap_text, (50, 100))

        # Pygame 화면에 그리기
        screen.blit(frame_surface, (0, 0))


        # 선택된 음악 표시
        music_text = font.render(f"Playing: {selected_music}", True, WHITE)
        screen.blit(music_text, (50, 50))

        pygame.display.flip()

    cap.release()
    pose.close()
