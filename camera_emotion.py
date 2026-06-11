import cv2
import numpy as np
import uuid
from datetime import datetime
from tensorflow.keras.models import load_model
import json

# تحميل الموديل
model = load_model("model/best_model.h5")

emotion_labels = [
    "Angry",
    "Disgust",
    "Fear",
    "Happy",
    "Neutral",
    "Sad",
    "Surprise"
]

# معلومات الجلسة
session_id = str(uuid.uuid4())
start_time = datetime.now()

emotion_count = {
    "Angry": 0,
    "Disgust": 0,
    "Fear": 0,
    "Happy": 0,
    "Neutral": 0,
    "Sad": 0,
    "Surprise": 0
}

confidence_list = []

total_frames = 0
face_frames = 0

# كاشف الوجه
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades +
    "haarcascade_frontalface_default.xml"
)

cap = cv2.VideoCapture(0)

while True:

    ret, frame = cap.read()

    if not ret:
        break

    total_frames += 1

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.3,
        minNeighbors=5
    )

    print("Faces found:", len(faces))

    if len(faces) > 0:
        face_frames += 1

    for (x, y, w, h) in faces:

        face = gray[y:y+h, x:x+w]

        face = cv2.resize(face, (48, 48))

        face = face.astype("float32") / 255.0

        face = np.expand_dims(face, axis=0)

        face = np.expand_dims(face, axis=-1)

        prediction = model.predict(
            face,
            verbose=0
        )[0]

        for emotion_name, prob in zip(
            emotion_labels,
            prediction
        ):
            print(
                f"{emotion_name}: {prob:.3f}"
            )

        emotion = emotion_labels[
            np.argmax(prediction)
        ]

        confidence = float(
            np.max(prediction)
        )

        emotion_count[emotion] += 1

        confidence_list.append(
            confidence
        )

        cv2.rectangle(
            frame,
            (x, y),
            (x+w, y+h),
            (0, 255, 0),
            2
        )

        cv2.putText(
            frame,
            f"{emotion} ({confidence:.2f})",
            (x, y-10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.9,
            (0, 255, 0),
            2
        )

    cv2.imshow(
        "EmoBridge AI",
        frame
    )

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    if cv2.getWindowProperty("EmoBridge AI", cv2.WND_PROP_VISIBLE) < 1:
        break

# نهاية الجلسة
end_time = datetime.now()

dominant_emotion = max(
    emotion_count,
    key=emotion_count.get
)

if len(confidence_list) > 0:
    average_confidence = (
        sum(confidence_list)
        / len(confidence_list)
    )
else:
    average_confidence = 0

if total_frames > 0:
    engagement_rate = (
        face_frames
        / total_frames
    ) * 100
else:
    engagement_rate = 0

session_data = {
    "session_id": session_id,
    "start_time": str(start_time),
    "end_time": str(end_time),
    "dominant_emotion": dominant_emotion,
    "average_confidence": round(
        average_confidence,
        2
    ),
    "engagement_rate": round(
        engagement_rate,
        2
    )
}

print("\n===== SESSION REPORT =====")
print(session_data)

with open("session_report.json", "w") as f:
    json.dump(session_report, f, indent=4)

cap.release()
cv2.destroyAllWindows()