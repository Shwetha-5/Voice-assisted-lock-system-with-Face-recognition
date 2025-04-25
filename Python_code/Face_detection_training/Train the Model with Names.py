import cv2
import os
import numpy as np
import pickle

dataset_dir = "../face_dataset"
recognizer = cv2.face.LBPHFaceRecognizer_create()
faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

faces, labels = [], []
name_labels = {}  # Dictionary to store name-label mapping
current_label = 0  # Initial label

# Read images from dataset and assign labels
for person_name in os.listdir(dataset_dir):
    person_path = os.path.join(dataset_dir, person_name)
    if not os.path.isdir(person_path):
        continue

    # Assign a unique label to each person
    name_labels[current_label] = person_name

    for img_name in os.listdir(person_path):
        img_path = os.path.join(person_path, img_name)
        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

        faces.append(img)
        labels.append(current_label)

    current_label += 1  # Increment label for next person

# Train the recognizer
recognizer.train(faces, np.array(labels))
recognizer.write("classifier.yml")  # Save model

# Save name-label mapping for recognition
with open("labels.pkl", "wb") as f:
    pickle.dump(name_labels, f)

print("Training complete. Model and labels saved.")
