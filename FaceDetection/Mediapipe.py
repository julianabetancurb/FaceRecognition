import cv2
import mediapipe as mp
import numpy as np


def capture_look():
    #CARA
    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5)
    cap = cv2.VideoCapture(0)
    #MANOS
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)
    looking = None
    mouth_open = False
    pressed_m = False
    arm = None

    while cap.isOpened() and not pressed_m:
        success, image = cap.read()

        # Flip the image horizontally for a later selfie-view display
        # Also convert the color space from BGR to RGB
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)

        # To improve performance
        image.flags.writeable = False

        # Get the result
        results = face_mesh.process(image)

        # To improve performance
        image.flags.writeable = True

        # Convert the color space from RGB to BGR
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        img_h, img_w, img_c = image.shape
        face_3d = []
        face_2d = []

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                for idx, lm in enumerate(face_landmarks.landmark):
                    if idx == 33 or idx == 263 or idx == 1 or idx == 61 or idx == 291 or idx == 199:
                        if idx == 1:
                            nose_2d = (lm.x * img_w, lm.y * img_h)
                            nose_3d = (lm.x * img_w, lm.y * img_h, lm.z * 8000)

                        x, y = int(lm.x * img_w), int(lm.y * img_h)

                        # Get the 2D Coordinates
                        face_2d.append([x, y])

                        # Get the 3D Coordinates
                        face_3d.append([x, y, lm.z])

                # Convert it to the NumPy array
                face_2d = np.array(face_2d, dtype=np.float64)

                # Convert it to the NumPy array
                face_3d = np.array(face_3d, dtype=np.float64)

                # The camera matrix
                focal_length = 1 * img_w

                cam_matrix = np.array([[focal_length, 0, img_h / 2],
                                       [0, focal_length, img_w / 2],
                                       [0, 0, 1]])

                # The Distance Matrix
                dist_matrix = np.zeros((4, 1), dtype=np.float64)

                # Solve PnP
                success, rot_vec, trans_vec = cv2.solvePnP(face_3d, face_2d, cam_matrix, dist_matrix)

                # Get rotational matrix
                rmat, jac = cv2.Rodrigues(rot_vec)

                # Get angles
                angles, mtxR, mtxQ, Qx, Qy, Qz = cv2.RQDecomp3x3(rmat)

                # Get the y rotation degree
                x = angles[0] * 360
                y = angles[1] * 360

                # Determine looking direction
                if y < -10:
                    looking = "left"
                    text = "Looking Left"
                elif y > 10:
                    looking = "right"
                    text = "Looking Right"
                elif x < -5:
                    looking = "down"
                    text = "Looking Down"
                elif x > 15:
                    looking = "up"
                    text = "Looking Up"
                else:
                    looking = "forward"
                    text = "Forward"


                #DETECTAR BOCA ABIERTA
                upper_lip_top = face_landmarks.landmark[13].y * img_h
                lower_lip_bottom = face_landmarks.landmark[14].y * img_h
                mouth_height = lower_lip_bottom - upper_lip_top

                if mouth_height > 10:
                    mouth_open = True
                    text = "Mouth Open"

                cv2.putText(image, text, (50,100 ), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

                # Detectar manos
                results_hands = hands.process(image)

                # Verificar si se detectaron manos
                if results_hands.multi_hand_landmarks:
                    # Iterar sobre todas las manos detectadas
                    for hand_landmarks in results_hands.multi_hand_landmarks:
                        # Ejemplo: Verificar si se levantan dos dedos
                        if len(results_hands.multi_hand_landmarks) > 0:
                            hand_landmarks = results_hands.multi_hand_landmarks[
                                0]  # Tomar solo la primera mano detectada
                            finger_states = [0, 0, 0, 0, 0]  # Estado de los 5 dedos (0 = cerrado, 1 = abierto)
                            for i, landmark in enumerate(hand_landmarks.landmark):

                                if i in [8, 12, 16,
                                         20]:  # Índices de los puntos de referencia de los dedos que queremos verificar (punta del dedo)
                                    finger_states[i // 5] = 1 if landmark.y < hand_landmarks.landmark[i - 5].y else 0

                            if sum(finger_states) == 0:  # Verificar si se levantan exactamente 2 dedos
                                cv2.putText(image, "Arma 1", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                                arm = 1
                            if sum(finger_states) == 1:  # Verificar si se levantan exactamente 2 dedos
                                cv2.putText(image, "Arma 2", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                                arm = 2
                            if sum(finger_states) == 2:  # Verificar si se levantan exactamente 2 dedos
                                cv2.putText(image, "Arma 3", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                                arm = 3
                            if sum(finger_states) == 3:  # Verificar si se levantan exactamente 2 dedos
                                cv2.putText(image, "Arma 4", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                                arm = 4

                        # Ejemplo: Obtener las coordenadas de la punta del dedo índice
                        index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                        index_finger_tip_x = int(index_finger_tip.x * img_w)
                        index_finger_tip_y = int(index_finger_tip.y * img_h)

                        # Ejemplo: Dibujar un círculo en la punta del dedo índice
                        cv2.circle(image, (index_finger_tip_x, index_finger_tip_y), 10, (0, 255, 0), -1)

        cv2.imshow('Head Pose Estimation', image)

        if cv2.waitKey(1) & 0xFF == ord('m'):
            return looking, mouth_open, arm

    cap.release()
    cv2.destroyAllWindows()

#capture_look()


