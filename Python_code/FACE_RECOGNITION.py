import serial.tools.list_ports
import time
import cv2
import pickle

# List available serial ports
ports = serial.tools.list_ports.comports()
portsList = [p.device for p in ports]  # Extracting only device names
'''
for p in portsList:
    print(p)

com = input("Select the port for interfacing: ")

if com not in portsList:
    print("Invalid port selection. Exiting...")
    exit()
'''
com='/dev/cu.usbserial-120'
print(f"------------\n\n{com} is selected")

# Initialize Serial Connection
serialInst = serial.Serial()
serialInst.baudrate = 9600
serialInst.port = com

try:
    serialInst.open()
    time.sleep(2)  # Allow Arduino to reset
except serial.SerialException as e:
    print(f"Error opening serial port: {e}")
    exit()

# Load the trained model and name-label mapping
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('face_detection_training/classifier.yml')

with open("face_detection_training/labels.pkl", "rb") as f:
    name_labels = pickle.load(f)

# Load face detector
faceCascade = cv2.CascadeClassifier('face_detection_training/haarcascade_frontalface_default.xml')

# Start video capture
video_capture = cv2.VideoCapture(0)

solenoid_unlocked = False  # Track solenoid state
unlock_start_time = 0       # Store time when unlocked

try:
    while True:
        ret, frame = video_capture.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.3, 5)

        recognized = False  # Flag to check if a known face is detected

        for (x, y, w, h) in faces:
            face_img = gray[y:y + h, x:x + w]
            label, confidence = recognizer.predict(face_img)

            # Get person's name from label mapping
            person_name = name_labels.get(label, "Unknown")

            if confidence < 25 and person_name != "Unknown":  # Only unlock for known persons
                recognized = True
                text = f"{person_name} ({round(confidence, 2)})"
            else:
                text = "Unknown"

            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        # Unlock only if a known face is detected
        if recognized and not solenoid_unlocked:
            serialInst.write("UNLOCK\n".encode('utf-8'))
            print("Sent: UNLOCK")
            solenoid_unlocked = True
            unlock_start_time = time.time()  # Start unlock timer

        # **Lock after 7 seconds instead of 5**
        if solenoid_unlocked and time.time() - unlock_start_time >= 7:
            serialInst.write("LOCK\n".encode('utf-8'))
            print("Sent: LOCK")
            solenoid_unlocked = False

        cv2.imshow("Face Recognition", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    # Ensure "LOCK" is sent before closing
    serialInst.write("LOCK\n".encode('utf-8'))
    print("Sent: LOCK (Final)")

    serialInst.close()
    print("Serial communication closed.")

    video_capture.release()
    cv2.destroyAllWindows()
