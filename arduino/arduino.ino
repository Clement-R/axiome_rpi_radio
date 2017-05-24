int potPin= A0;  //Declare potPin to be analog pin A0
int potPin2= A1;  //Declare potPin2 to be analog pin A1
int LEDPin= 9;  // Declare LEDPin to be arduino pin 9
int readValue;  // Use this variable to read Potentiometer
int readValue2;  // Use this variable to read Potentiometer
int writeValue; // Use this variable for writing to LED

void setup() {
  pinMode(potPin, INPUT);  //set potPin to be an input
  pinMode(potPin2, INPUT);  //set potPin2 to be an input
  pinMode(LEDPin, OUTPUT); //set LEDPin to be an OUTPUT
  pinMode(13, OUTPUT);
  Serial.begin(9600);      // turn on Serial Port
}
 
void loop() {
  readValue = analogRead(potPin);
  readValue2 = analogRead(potPin2);
  writeValue = (255./1023.) * readValue; //Calculate Write Value for LED
  // analogWrite(LEDPin, writeValue);
  Serial.print("You are reading a value of ");
  Serial.println(readValue);
  Serial.print("You are reading a value of ");
  Serial.println(readValue2);
  Serial.println("-----------------------");

  if(readValue == 0) {
    digitalWrite(11, LOW);
    digitalWrite(12, LOW);
    digitalWrite(13, LOW);
  } else if (readValue > 0 && readValue <= 204) {
    digitalWrite(11, HIGH);
    digitalWrite(12, LOW);
    digitalWrite(13, LOW);
  } else if (readValue >= 205 && readValue <= 409) {
    digitalWrite(11, LOW);
    digitalWrite(12, HIGH);
    digitalWrite(13, LOW);
  } else if (readValue >= 410 && readValue <= 614) {
    digitalWrite(11, HIGH);
    digitalWrite(12, HIGH);
    digitalWrite(13, LOW);
  } else if (readValue >= 615 && readValue <= 819) {
    digitalWrite(11, LOW);
    digitalWrite(12, LOW);
    digitalWrite(13, HIGH);
  } else if (readValue >= 820) {
    digitalWrite(11, HIGH);
    digitalWrite(12, LOW);
    digitalWrite(13, HIGH);
  }

  if (readValue2 >= 0 && readValue2 <= 330) {
    digitalWrite(10, LOW);
  } else {
    digitalWrite(10, HIGH);
  }
}
