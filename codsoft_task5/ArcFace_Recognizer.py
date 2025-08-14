import cv2
import os
import numpy as np
from insightface.app import FaceAnalysis

# ===================== Initialize ArcFace Model =====================
app = FaceAnalysis(name='buffalo_l', providers=['CPUExecutionProvider'])
app.prepare(ctx_id=0, det_size=(640, 640))

# ===================== Cosine Similarity Function =====================
def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# ===================== Load Known Faces =====================
known_embeddings = []
known_names = []

known_dir = 'FaceRecognition_Project/known_faces'

print("📂 Loading known faces...")

for filename in os.listdir(known_dir):
    path = os.path.join(known_dir, filename)

    # Load image
    img = cv2.imread(path)
    if img is None:
        print(f"❌ Could not read image: {path}")
        continue

    # Convert BGR to RGB (required by insightface)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Detect face
    faces = app.get(img_rgb)
    if len(faces) == 0:
        print(f"⚠ No face found in: {path}")
        continue

    # Save embedding
    known_embeddings.append(faces[0].embedding)
    known_names.append(os.path.splitext(filename)[0])
    print(f"✅ Loaded: {filename}")

if not known_embeddings:
    print("❌ No known faces loaded. Exiting.")
    exit()

# ===================== Start Webcam =====================
cap = cv2.VideoCapture(0)
print("🎥 Webcam started. Press 'q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("❌ Failed to capture frame")
        break

    # Convert frame to RGB for insightface
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    faces = app.get(frame_rgb)

    for face in faces:
        embedding = face.embedding
        name = "Unknown"
        max_sim = -1

        # Compare against all known embeddings
        for i, known_emb in enumerate(known_embeddings):
            sim = cosine_similarity(embedding, known_emb)
            if sim > 0.35 and sim > max_sim:  # Tune 0.35 threshold if needed
                name = known_names[i]
                max_sim = sim

        # Draw bounding box and label
        x1, y1, x2, y2 = face.bbox.astype(int)
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(frame, name, (x1, y2 + 25), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

    # Show frame
    cv2.imshow("🧠 ArcFace Recognition", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# ===================== Cleanup =====================
cap.release()
cv2.destroyAllWindows()
