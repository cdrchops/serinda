import mediapipe as mp
import cv2
import numpy as np

# Initialize MediaPipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(max_num_faces=1)

# Calibrated focal length (from calibration step)
focal_length = 1000  # in pixels
eye_to_eye_real = 0.06  # 6 cm, average eye-to-eye distance in meters

cap = cv2.VideoCapture(0)
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb_frame)

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            # Get eye landmarks (e.g., indices 33 and 263 for outer eye corners)
            left_eye = face_landmarks.landmark[33]
            right_eye = face_landmarks.landmark[263]
            pixel_dist = np.sqrt(
                ((left_eye.x - right_eye.x) * frame.shape[1])**2 +
                ((left_eye.y - right_eye.y) * frame.shape[0])**2
            )
            # Calculate distance
            distance = (focal_length * eye_to_eye_real) / pixel_dist
            print(f"Estimated distance: {distance:.2f} meters")

    cv2.imshow("Frame", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()