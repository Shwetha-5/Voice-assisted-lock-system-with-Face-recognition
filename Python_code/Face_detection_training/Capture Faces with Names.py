import cv2
import os

# Create a dataset directory if it doesn't exist
dataset_dir = "../face_dataset"
if not os.path.exists(dataset_dir):
    os.makedirs(dataset_dir)

# Load the Haarcascade Face Detector
faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Open the camera
video_capture = cv2.VideoCapture(0)

person_name = input("Enter the person's name: ")
person_dir = os.path.join(dataset_dir, person_name)
if not os.path.exists(person_dir):
    os.makedirs(person_dir)

count = 0
while count < 700:  # Capture 100 images per person
    ret, frame = video_capture.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        count += 1
        face_img = gray[y:y + h, x:x + w]
        cv2.imwrite(f"{person_dir}/{count}.jpg", face_img)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

    cv2.imshow("Capturing Faces", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

print(f"Captured {count} images for {person_name}")
video_capture.release()
cv2.destroyAllWindows()
