import cv2
from simple_facerec import SimpleFaceRec

# Encode faces from a folder
sfr = SimpleFaceRec()
sfr.load_encoding_images("FaceRecognition_Project/known_faces/")

# Load Camera
cap = cv2.VideoCapture(0)


while True:
    ret, frame = cap.read()

    if not ret:
        break

    # Detect Faces
    face_locations, face_names = sfr.detect_known_faces(frame)
    for face_loc, name in zip(face_locations, face_names):
        y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]

        cv2.putText(frame, name,(x1, y1 - 10), cv2.FONT_HERSHEY_DUPLEX, 1, (179, 9, 54), 2)
        cv2.rectangle(frame, (x1, y1), (x2, y2), (179, 9, 54), 2)

    cv2.imshow("Face Recognition", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("Exiting...")
        break

cap.release()
cv2.destroyAllWindows()