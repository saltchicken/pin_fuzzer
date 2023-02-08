const int outputPin = 22;
const int inputPin = 30;

void setup() {
  for ( int i = 0; i < 8; i++) {
    pinMode(outputPin + i, OUTPUT);
    pinMode(inputPin + i, INPUT);
  }
  Serial.begin(9600);
  Serial.println("Serial started");
}

void loop() {
  //String output;
  while (Serial.available() > 0) {
    String incomingData = Serial.readStringUntil('\n');
    incomingData.trim();
    if (incomingData[2] == '1'){
      digitalWrite(outputPin + int(incomingData[0] - 48), HIGH);
    } else {
      digitalWrite(outputPin + int(incomingData[0] - 48), LOW);
    }
  }
  for ( int i = 0; i < 8; i++) {
    int inputState = digitalRead(inputPin + i);
    Serial.print(inputState);
  }
  Serial.println(""); 
  delay(100);
}
