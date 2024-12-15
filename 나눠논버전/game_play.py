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

    start_time = pygame.time.get_ticks()

    status_text = None

    perfect = 0
    notes = 10

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
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(frame_rgb)

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
            
            current_time = pygame.time.get_ticks() - start_time

            left_hand_up_time = 5000
            clap_time = 8000
            Y_pose_time = 10000
            M_pose_time = 13000
            C_pose_time = 16000
            A_pose_time = 19000

            left_wrist_x = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST].x
            left_elbow_x = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ELBOW].x
            left_shoulder_x = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].x

            right_wrist_x = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST].x
            right_elbow_x = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ELBOW].x
            right_shoulder_x = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].x

            left_wrist_y = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST].y
            left_shoulder_y = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].y
            left_elbow_y = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ELBOW].y

            right_wrist_y = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST].y
            right_shoulder_y = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].y
            right_elbow_y = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ELBOW].y

            nose_y = results.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE].y


            if status_text == None:
                #왼손 들기
                if ( left_hand_up_time - 200<= current_time <= left_hand_up_time + 200):
                    if (left_wrist_y < 0.5 and left_shoulder_y > left_elbow_y):
                        status_text = "Perfect"
                        perfect += 1
                    else:
                        status_text = "Miss" 
                    text_time = pygame.time.get_ticks()  
                #박수
                if(clap_time - 200 <= current_time <= clap_time + 200):
                    if(abs(left_wrist_x - right_wrist_x) < 0.2):
                        status_text = "Perfect"
                        perfect += 1
                    else:
                        status_text = "Miss"
                    text_time = pygame.time.get_ticks()
                #Y
                if(Y_pose_time -200 <= current_time <= Y_pose_time + 200):
                    if(left_elbow_x < left_wrist_x and left_shoulder_y > left_elbow_y and right_elbow_x > right_wrist_x and right_shoulder_y > right_elbow_y):
                        status_text = "Perfect"
                        perfect += 1
                    else:
                        status_text = "Miss"
                    text_time = pygame.time.get_ticks()
                #M
                if(M_pose_time -200 <= current_time <= M_pose_time + 200):
                    if(right_elbow_x < right_wrist_x and left_elbow_x > left_wrist_x and left_wrist_y < nose_y and right_wrist_y < nose_y):
                        status_text = "Perfect"
                        perfect += 1
                    else:
                        status_text = "Miss"
                    text_time = pygame.time.get_ticks()
                #C
                if(C_pose_time -200 <= current_time <= C_pose_time + 200):
                    if(right_shoulder_x > right_elbow_x and right_elbow_x > right_wrist_x and left_shoulder_x > left_elbow_x and left_elbow_x > left_wrist_x):
                        status_text = "Perfect"
                        perfect += 1
                    else:
                        status_text = "Miss"
                    text_time = pygame.time.get_ticks()
                #A
                if(A_pose_time -200 <= current_time <= A_pose_time + 200):
                    if(left_wrist_y < 0.5 and left_shoulder_y > left_elbow_y and right_wrist_x < 0.5 and right_shoulder_y > right_elbow_y
                       and abs(left_wrist_x - right_wrist_x) < 0.2):
                        status_text = "Perfect"
                        perfect += 1
                    else:
                        status_text = "Miss"
                    text_time = pygame.time.get_ticks()



        # Pygame 화면에 그리기
        screen.blit(frame_surface, (0, 0))

        if status_text:
            enable_time = pygame.time.get_ticks() - text_time
            if enable_time < 1200:
                status_screen = font.render(status_text,True,WHITE)
                screen.blit(status_screen, (50, 150))
            else:
                status_text = None


        # 선택된 음악 표시
        music_text = font.render(f"Playing: {selected_music}", True, WHITE)
        screen.blit(music_text, (50, 50))

        pygame.display.flip()

    cap.release()
    pose.close()
