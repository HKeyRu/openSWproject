import pygame
import cv2
import sys
import mediapipe as mp


pygame.mixer.init()
pygame.mixer.music.load("ymca.mp3")

def game_play_screen(screen, selected_music):
    from result_screen import results_screen
    WHITE = (255, 255, 255)
    font = pygame.font.Font(None, 70)
    
    # OpenCV 웹캠 초기화
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("웹캠을 열 수 없습니다!")
        return
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

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
    miss = 0
    notes = 25
    score = 0

    # 애니메이션에 사용할 이미지
    image_y = pygame.image.load("pose_y.png")  # pose_y.png 이미지 파일 불러오기
    image_y = pygame.transform.scale(image_y, (150, 150))  # 이미지 크기 조정
    image_y_rect = image_y.get_rect(topleft=(0, 0))  # 이미지의 초기 위치 (왼쪽 상단)

    image_c = pygame.image.load("pose_c.png")
    image_c = pygame.transform.scale(image_c, (150,150))
    image_c_rect = image_c.get_rect(topleft=(0,0))

    image_clap = pygame.image.load("clap.png")
    image_clap = pygame.transform.scale(image_clap, (150,150))
    image_clap_rect = image_clap.get_rect(topleft=(0,0))

    image_y2 = pygame.image.load("pose_y.png")
    image_y2 = pygame.transform.scale(image_y2, (150,150))
    image_y2_rect = image_y2.get_rect(topleft=(0,0))

    image_c2 = pygame.image.load("pose_c.png")
    image_c2 = pygame.transform.scale(image_c2, (150,150))
    image_c2_rect = image_c2.get_rect(topleft=(0,0))

    image_clap2 = pygame.image.load("clap.png")
    image_clap2 = pygame.transform.scale(image_clap2, (150,150))
    image_clap2_rect = image_clap2.get_rect(topleft=(0,0))


    # 애니메이션 변수
    animation_duration = 3000  # 애니메이션의 전체 지속 시간 (ms)
    animation_y_start_ms = 5000  # 애니메이션 시작 기준 시간 (ms)
    animation_c_start_ms = 6000
    animation_clap_start_ms = 4000
    animation_y2_start_ms = 9000
    animation_c2_start_ms = 10000
    animation_clap2_start_ms = 14000

    animation_y_started = False  # 애니메이션 시작 여부
    animation_c_started = False
    animation_clap_started = False
    animation_y2_started = False
    animation_c2_started = False
    animation_clap2_started = False

    animation_y_complete = False  # 애니메이션 완료 여부
    animation_c_complete = False
    animation_clap_complete = False
    animation_y2_complete = False 
    animation_c2_complete = False
    animation_clap2_complete = False
    
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

            #채보 초기화 & 제작
            left_hand_up_time = 1000000
            right_hand_up_time = 1000000
            clap_time = 1000000
            Y_pose_time = 1000000
            M_pose_time = 1000000
            C_pose_time = 1000000
            A_pose_time = 1000000

            clap_time = 5933
            Y_pose_time = 6900 # 3900 + 3초
            #M_pose_time = 7833
            C_pose_time = 8233
            #A_pose_time = 8500


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

            right_eye_x = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_EYE].x
            nose_x = results.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE].x
            nose_y = results.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE].y

            score = 10000000 * (perfect / notes)

            if status_text == None:
                #왼손 들기
                if ( left_hand_up_time - 200<= current_time <= left_hand_up_time + 200):
                    if (left_wrist_y < 0.5 and left_shoulder_y > left_elbow_y):
                        status_text = "Perfect"
                        perfect += 1
                    else:
                        status_text = "Miss" 
                        miss += 1
                    text_time = pygame.time.get_ticks()  
                #오른손 들기
                if ( right_hand_up_time - 200<= current_time <= right_hand_up_time + 200):
                    if (right_wrist_y < 0.5 and right_shoulder_y > right_elbow_y):
                        status_text = "Perfect"
                        perfect += 1
                    else:
                        status_text = "Miss" 
                        miss += 1
                    text_time = pygame.time.get_ticks() 
                #박수
                if(clap_time - 200 <= current_time <= clap_time + 200):
                    if(abs(left_wrist_x - right_wrist_x) < 0.2):
                        status_text = "Perfect"
                        perfect += 1
                    else:
                        status_text = "Miss"
                        miss += 1
                    text_time = pygame.time.get_ticks()
                #Y
                if(Y_pose_time -200 <= current_time <= Y_pose_time + 200):
                    if(left_elbow_x < left_wrist_x and left_shoulder_y > left_elbow_y and right_elbow_x > right_wrist_x and right_shoulder_y > right_elbow_y):
                        status_text = "Perfect"
                        perfect += 1
                    else:
                        status_text = "Miss"
                        miss += 1
                    text_time = pygame.time.get_ticks()
                #M
                if(M_pose_time -200 <= current_time <= M_pose_time + 200):
                    if(right_elbow_x < right_wrist_x and left_elbow_x > left_wrist_x and left_wrist_y < nose_y and right_wrist_y < nose_y):
                        status_text = "Perfect"
                        perfect += 1
                    else:
                        status_text = "Miss"
                        miss += 1
                    text_time = pygame.time.get_ticks()
                #C
                if(C_pose_time -200 <= current_time <= C_pose_time + 200):
                    if(right_wrist_x < nose_x and left_wrist_x < nose_x):
                        status_text = "Perfect"
                        perfect += 1
                    else:
                        status_text = "Miss"
                        miss += 1
                    text_time = pygame.time.get_ticks()
                #A
                if(A_pose_time -200 <= current_time <= A_pose_time + 200):
                    if(left_wrist_y < 0.5 and left_shoulder_y > left_elbow_y and right_wrist_x < 0.5 and right_shoulder_y > right_elbow_y
                       and abs(left_wrist_x - right_wrist_x) < 0.2):
                        status_text = "Perfect"
                        perfect += 1
                    else:
                        status_text = "Miss"
                        miss += 1
                    text_time = pygame.time.get_ticks()



        # Pygame 화면에 그리기
        screen.blit(frame_surface, (0, 0))

        if status_text:
            enable_time = pygame.time.get_ticks() - text_time
            if enable_time < 1200:
                status_screen = font.render(status_text,True,(255, 198, 13))
                screen.blit(status_screen, (580, 150))
            else:
                status_text = None

        # 스코어 표시
        score_text = font.render(f"Score: {score:.0f}", True, (100, 100, 100))
        screen.blit(score_text, (800, 600)) 


        # 애니메이션 이미지 그리기
        if not animation_y_complete:
            screen.blit(image_y, image_y_rect)  # 애니메이션 중 이미지 그리기
        if not animation_c_complete:
            screen.blit(image_c, image_c_rect)
        if not animation_clap_complete:
            screen.blit(image_clap, image_clap_rect)
        if not animation_y2_complete:
            screen.blit(image_y2, image_y2_rect)
        if not animation_c2_complete:
            screen.blit(image_c2, image_c2_rect)
        if not animation_clap2_complete:
            screen.blit(image_clap2, image_clap2_rect)
        # 애니메이션 시작 조건 확인
        if not animation_y_started and current_time <= animation_y_start_ms:
            animation_y_started = True  # 애니메이션 시작 시간 도달
        if not animation_c_started and current_time <= animation_c_start_ms:
            animation_c_started = True
        if not animation_clap_started and current_time <= animation_clap_start_ms:
            animation_clap_started = True
        if not animation_y2_started and current_time <= animation_y2_start_ms:
            animation_y2_started = True
        if not animation_c2_started and current_time <= animation_c2_start_ms:
            animation_c2_started = True
        if not animation_clap2_started and current_time <= animation_clap2_start_ms:
            animation_clap2_started = True

        # 애니메이션 진행
        if animation_y_started and not animation_y_complete:
            elapsed_time = current_time - animation_y_start_ms  # 애니메이션 시작 이후 경과 시간

            if elapsed_time < animation_duration:
                # 진행 비율에 맞게 이미지 이동
                progress = elapsed_time / animation_duration
                image_y_rect.x = int(1280 * progress - image_y_rect.width)
            else:
                # 애니메이션이 끝났다면 완료 플래그 설정
                image_y_rect.x = 640 - image_y_rect.width // 2  # 화면 중앙에 정렬
                animation_y_complete = True

        if animation_c_started and not animation_c_complete:
            elapsed_time = current_time - animation_c_start_ms  

            if elapsed_time < animation_duration:
                progress = elapsed_time / animation_duration
                image_c_rect.x = int(1280 * progress - image_c_rect.width)
            else:
                image_c_rect.x = 640 - image_c_rect.width // 2 
                animation_c_complete = True

        if animation_clap_started and not animation_clap_complete:
            elapsed_time = current_time - animation_clap_start_ms 

            if elapsed_time < animation_duration:
                progress = elapsed_time / animation_duration
                image_clap_rect.x = int(1280 * progress - image_clap_rect.width)
            else:
                image_clap_rect.x = 640 - image_clap_rect.width // 2 
                animation_clap_complete = True

        if animation_y2_started and not animation_y2_complete:
            elapsed_time = current_time - animation_y2_start_ms  

            if elapsed_time < animation_duration:
                progress = elapsed_time / animation_duration
                image_y2_rect.x = int(1280 * progress - image_y2_rect.width)
            else:
                image_y2_rect.x = 640 - image_y2_rect.width // 2  
                animation_y2_complete = True

        if animation_c2_started and not animation_c2_complete:
            elapsed_time = current_time - animation_c2_start_ms  

            if elapsed_time < animation_duration:
                progress = elapsed_time / animation_duration
                image_c2_rect.x = int(1280 * progress - image_c2_rect.width)
            else:
                image_c2_rect.x = 640 - image_c2_rect.width // 2 
                animation_c2_complete = True

        if animation_clap2_started and not animation_clap2_complete:
            elapsed_time = current_time - animation_clap2_start_ms 

            if elapsed_time < animation_duration:
                progress = elapsed_time / animation_duration
                image_clap2_rect.x = int(1280 * progress - image_clap2_rect.width)
            else:
                image_clap2_rect.x = 640 - image_clap2_rect.width // 2 
                animation_clap2_complete = True

        # 선택된 음악 표시
        music_text = font.render(f"Playing: {selected_music}", True, (100,100,100))
        screen.blit(music_text, (50, 600))

        if(current_time >= 41500):
            results_screen(screen, perfect, notes, selected_music)

        pygame.display.flip()

    cap.release()
    pose.close()
