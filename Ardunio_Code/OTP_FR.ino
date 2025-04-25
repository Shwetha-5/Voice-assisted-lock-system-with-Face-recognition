
#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <Keypad.h>

// LCD config
LiquidCrystal_I2C lcd(0x27, 16, 2);

// Pins
const int solenoidPin = 5;
const int ldr = A0;
const int pir = 2;
const int led = 3;
const int buzzer = 4;

// Keypad config
const byte ROWS = 4;
const byte COLS = 4;
char hexaKeys[ROWS][COLS] = {
  {'1', '2', '3', 'A'},
  {'4', '5', '6', 'B'},
  {'7', '8', '9', 'C'},
  {'*', '0', '#', 'D'}
};
byte rowPins[ROWS] = {13, 12, 11, 10};
byte colPins[COLS] = {9, 8, 7, 6};
Keypad keypad = Keypad(makeKeymap(hexaKeys), rowPins, colPins, ROWS, COLS);

// Variables
String correctPasscode = "";
String enteredPasscode = "";
String command = "";
bool otpMode = false;

void setup() {
  pinMode(solenoidPin, OUTPUT);
  pinMode(ldr, INPUT);
  pinMode(pir, INPUT);
  pinMode(led, OUTPUT);
  pinMode(buzzer, OUTPUT);
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(solenoidPin, HIGH); // Locked

  Serial.begin(9600);
  lcd.begin();
  lcd.backlight();
  showWelcome();
  buzz(1);
}

void loop() {
  automatic_light();

  // Handle serial input (from Python or other logic)
  if (Serial.available()) {
    command = Serial.readStringUntil('\n');
    command.trim();

    if (command.equals("UNLOCK")) {
      msg("Face Recognized", "Unlocking...");
      buzz(1);
      unlockSolenoid();
    } 
    else if (command.equals("LOCK")) {
      msg("Face Not Found", "Door Locked");
      buzz(2);
      lockSolenoid();
    } 
    else { // assume OTP
      correctPasscode = command;
      otpMode = true;
      enteredPasscode = "";
      msg("OTP Received", "Enter on Keypad");
    }
  }

  // OTP keypad input (if enabled)
  if (otpMode) {
    char key = keypad.getKey();
    if (key) {
      if (key == 'C') {
        enteredPasscode = "";
        msg("Passcode", "Cleared");
        delay(1000);
        msg("Enter OTP", enteredPasscode);
      } 
      else if (key == 'D') {
        if (enteredPasscode == correctPasscode) {
          msg("Correct OTP", "Unlocking...");
          buzz(1);
          unlockSolenoid();
          otpMode = false;
        } else {
          msg("Wrong OTP", "Try Again");
          buzz(2);
          delay(1500);
          enteredPasscode = "";
          msg("Enter OTP", "");
        }
      } 
      else if (enteredPasscode.length() < 6) {
        enteredPasscode += key;
        msg("Enter OTP", enteredPasscode);
      }
    }
  }
}

void unlockSolenoid() {
  digitalWrite(solenoidPin, LOW);
  digitalWrite(LED_BUILTIN, HIGH);
  delay(7000);
  lockSolenoid();
  showWelcome();
}

void lockSolenoid() {
  digitalWrite(solenoidPin, HIGH);
  digitalWrite(LED_BUILTIN, LOW);
  showWelcome();
}

void showWelcome() {
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Welcome Home");
  lcd.setCursor(0, 1);
  lcd.print("Door Locked");
}

void msg(String line1, String line2) {
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print(line1);
  lcd.setCursor(0, 1);
  lcd.print(line2);
}

void buzz(int times) {
  for (int i = 0; i < times; i++) {
    digitalWrite(buzzer, HIGH);
    delay(200);
    digitalWrite(buzzer, LOW);
    delay(200);
  }
}

void automatic_light() {
  int ldrState = analogRead(ldr);
  ldrState = ldrState > 500 ? 1 : 0;
  int pirState = digitalRead(pir);
  digitalWrite(led, (pirState == HIGH && ldrState == HIGH) ? HIGH : LOW);
}
