import cv2
import pickle

# Load the trained model and name-label mapping
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("classifier.yml")

with open("labels.pkl", "rb") as f:
    name_labels = pickle.load(f)

# Load face detector
faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Start video capture
video_capture = cv2.VideoCapture(0)

while True:
    ret, frame = video_capture.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        face_img = gray[y:y+h, x:x+w]
        label, confidence = recognizer.predict(face_img)

        # Get the person's name from label mapping
        person_name = name_labels.get(label, "Unknown")

        # Display results
        if confidence < 50:  # Lower confidence is better
            text = f"{person_name} ({round(confidence, 2)})"
        else:
            text = "Unknown"

        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        cv2.putText(frame, text, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    cv2.imshow("Face Recognition", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
