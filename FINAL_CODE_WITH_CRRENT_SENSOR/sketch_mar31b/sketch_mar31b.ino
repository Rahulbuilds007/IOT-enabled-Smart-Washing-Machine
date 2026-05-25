int sensorPin = A0;

float sensitivity = 0.066;   // 30A sensor
float offsetVoltage = 2.5;   // adjust later if needed

void setup() {
  pinMode(13, OUTPUT);    // drain
  pinMode(12, OUTPUT);    // inlet
  pinMode(6, OUTPUT);     // motor ON/OFF
  pinMode(7, OUTPUT);     // direction

  Serial.begin(9600);

  // All OFF (active LOW relay)
  digitalWrite(13, HIGH);
  digitalWrite(12, HIGH);
  digitalWrite(6, HIGH);
  digitalWrite(7, HIGH);
}

// 🔥 Function to read current
void readCurrent() {
  int adcValue = analogRead(sensorPin);

  float voltage = (adcValue * 5.0) / 1023.0;
  float current = (voltage - offsetVoltage) / sensitivity;

  Serial.print("ADC: ");
  Serial.print(adcValue);

  Serial.print(" | Voltage: ");
  Serial.print(voltage);

  Serial.print(" V | Current: ");
  Serial.print(current);
  Serial.println(" A");
}

// 🔥 Delay with current monitoring
void smartDelay(int duration) {
  int interval = 200;  // read every 200ms

  for (int t = 0; t < duration; t += interval) {
    readCurrent();
    delay(interval);
  }
}

void loop() {

  Serial.println("-------------------------------------------");

  // Drain
  digitalWrite(13, LOW);   // ON
  smartDelay(5000);
  digitalWrite(13, HIGH);  // OFF
  Serial.println("Drained");

  Serial.println("-------------------------------------------");

  // Fill
  digitalWrite(12, LOW);   // ON
  smartDelay(5000);
  digitalWrite(12, HIGH);  // OFF
  Serial.println("Filled");

  Serial.println("-------------------------------------------");

  Serial.println("Wash cycle (2 times)");

  // Wash cycle
  for (int i = 0; i < 2; i++) {

    // Clockwise
    digitalWrite(7, LOW);
    digitalWrite(6, LOW);
    Serial.println("Clockwise");
    smartDelay(10000);

    digitalWrite(6, HIGH);
    Serial.println("Motor OFF");
    smartDelay(5000);

    // Anti-clockwise
    digitalWrite(7, HIGH);
    digitalWrite(6, LOW);
    Serial.println("Anti-clockwise");
    smartDelay(10000);

    digitalWrite(6, HIGH);
    Serial.println("Motor OFF");
    smartDelay(5000);
  }

  Serial.println("-------------------------------------------");

  Serial.println("Rinse cycle (4 times)");

  // Rinse cycle
  for (int i = 0; i < 4; i++) {

    // CW
    digitalWrite(7, LOW);
    digitalWrite(6, LOW);
    smartDelay(10000);

    digitalWrite(6, HIGH);
    smartDelay(5000);

    // ACW
    digitalWrite(7, HIGH);
    digitalWrite(6, LOW);
    smartDelay(10000);

    digitalWrite(6, HIGH);
    smartDelay(5000);
  }

  Serial.println("Cycle Complete");

  delay(10000); // wait before restart
}