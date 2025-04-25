# Voice assisted lock system with Face recognition
This project develops an advanced face recognition system using Haar Cascade classifiers, enabling an Arduino-controlled automatic locking mechanism that enhances security and streamlines access for authorized users. It includes features like motion-triggered LED lighting, dynamic One-Time Password (OTP) generation for added verification, and a voice module for audio guidance, significantly improving both security and user-friendliness.
## Features
👁️‍🗨️ Face recognition using Haar Cascade<br>
🎤 Voice module (ISD1820) for audio guidance<br>
🔐 Automated locking mechanism using solenoid and relay<br>
📱 OTP generation via API to registered mobile devices<br>
🌙 Automatic LED lighting using LDR and PIR sensors<br>
🔢 Keypad and LCD module for OTP entry and user feedback<br>

## ⚙️ How It Works
- <u>Activation</u> : The system activates upon detecting motion
- <u>Face Scan</u>: CAM captures and compares the face using Haar Cascade.
- <u>Authentication</u>: If the face matches a registered user: the solenoid lock unlocks
- <u>OTP Verification</u>: An OTP is sent to the user's mobile via API.
- <u>OTP Entry</u>: The user enters the OTP on the keypad.
- <u>Access Granted</u>: On valid OTP, the door unlocks via solenoid control.
- <u>Lighting</u>: If ambient light is low and motion is detected, LEDs automatically turn on.
- <u>Voice Feedback</u>: ISD1820 provides guidance messages for visitors.

## 🛠️ Hardware Setup
![Alt Text](circuit_image.png)

## 🧪 Steps to Execute

### ✅ Step 1: Train the Face Recognition Model

Navigate to: `Python_code/Face_detection_training`

1. **Capture Faces**  
   Run:
   ```bash
   python "Capture Faces with Names.py"
   ```
   This opens the webcam and saves multiple face images with user-provided names.

2. **Train the Model**  
   Run:
   ```bash
   python "Train the Model with Names.py"
   ```
   Trains a face recognition model based on the captured dataset.

3. **Optional: Real-Time Testing**  
   Run:
   ```bash
   python "Real-Time Face Recognition.py"
   ```
   Useful to validate the trained model in real-time before deployment.

---

### ✅ Step 2: Upload Arduino Code

💻 Navigate to the `Ardunio_Code` folder and open `otp_fr.ino` using the Arduino IDE:

1. Connect your Arduino board.
2. Choose the correct port and board settings.
3. Upload the code.

> ⚠️ **Note**: Close the **Serial Monitor** before running any Python script involving serial communication.

---

### ✅ Step 3: Face Recognition & Solenoid Unlock

🎯 Navigate to the main `Python_code` directory and execute:

```bash
python "FACE_RECOGNITION.py"
```

This will:
- Activate webcam-based recognition.
- Match faces using the trained model.
- Communicate with the Arduino to trigger the solenoid lock if an authorized face is detected.

> 🛠️ **Tip:** Adjust the `confidence` value in `FACE_RECOGNITION.py` to increase or decrease sensitivity as per your environment. (e.g., lower value = stricter match)

---

### ✅ Step 4: OTP-Based Unlock (Alternative Access)

🔐 If face recognition fails or alternate entry is required:

```bash
python "otp.py"
```

This script:
- Generates an OTP.
- Sends it via an SMS API (e.g., Twilio, Fast2SMS).
- Accepts input from the keypad.
- Unlocks the door if OTP is correct.

---

### 📌 Final Notes

- Make sure all wiring is as per the `circuit_image.png`.
- Modules like:
  - ✅ PIR + LDR → for motion/light-triggered LED
  - ✅ ISD1820 → for voice prompts
  - ✅ LCD + Keypad → for user interaction
  - ✅ Solenoid Lock + Relay → for secured access  
  ...are correctly configured and powered.

- Install required Python libraries:
  ```bash
  pip install opencv-python pyserial
  ```

---
Great! Here's the **updated section** with video references added at the end, in a clean and consistent format for your `README.md`:

---
---

### 🎥 Reference Videos

- 🔗 [SMS API](https://youtu.be/-_bEXSdgaAk?si=nLvt_agTo0ZubyUU)
- 🔗 [Face Recognition](https://youtu.be/mkAx_81Pcww?si=CPLfq2qZxeL5l7R7)
- 🔗 [Voice Module Setup](https://youtube.com/shorts/AdDgmcNUhLQ?si=qTF7W46JalDDf1aq)

