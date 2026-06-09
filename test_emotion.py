import cv2
import numpy as np
from tensorflow.keras.models import load_model

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

def predict_emotion(image_path):

    img = cv2.imread(image_path)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    gray = cv2.resize(gray, (48, 48))

    gray = gray.astype("float32") / 255.0

    gray = np.expand_dims(gray, axis=0)
    gray = np.expand_dims(gray, axis=-1)

    prediction = model.predict(gray)

    emotion = emotion_labels[np.argmax(prediction)]

    return emotion

result = predict_emotion("test.jpg")

print("Emotion:", result)