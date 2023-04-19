int state = 0;
void setup() {
  pinMode(2, OUTPUT);
  pinMode(3, OUTPUT);
  pinMode(4, OUTPUT);
  pinMode(5, OUTPUT);
  digitalWrite(2, HIGH);
  digitalWrite(3, LOW);
  digitalWrite(4, LOW);
  digitalWrite(5, HIGH);
  Serial.begin(9600); // Default communication rate of the Bluetooth module
}
void loop() {

if(Serial.available() > 0){ // Checks whether data is comming from the serial port
state = Serial.read(); // Reads the data from the serial port

 if (state == '1') {
  digitalWrite(2, HIGH);
  digitalWrite(3, LOW);
  digitalWrite(4, LOW);
  digitalWrite(5, HIGH);
  state = 0;
 }
 else if (state == '2') {
  digitalWrite(2, LOW);
  digitalWrite(3, HIGH);
  digitalWrite(4, HIGH);
  digitalWrite(5, LOW);
  state = 0;
 } 
}

}
