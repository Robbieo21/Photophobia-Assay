int state = 1;
char data;

void setup() {
  pinMode(2, OUTPUT);
  pinMode(3, OUTPUT);
  pinMode(4, OUTPUT);
  pinMode(5, OUTPUT);
  digitalWrite(2, HIGH); //red
  digitalWrite(3, LOW);  //blue
  digitalWrite(4, LOW);  //red
  digitalWrite(5, HIGH); //blue
  Serial.begin(9600); // Default communication rate of the Bluetooth module
}

void loop() {

if(Serial.available() > 0){ // Checks whether data is comming from the serial port
    data = Serial.read(); // Reads the data from the serial port

    if (data == '1' || data == '2'){
     if (state == 1){
        state = 2;
     }
      else if (state == 2){
        state = 1;
     }
    }
    
    if (state == 1) {
        digitalWrite(2, HIGH); //red
        digitalWrite(3, LOW);  //blue
        digitalWrite(4, LOW);  //red
        digitalWrite(5, HIGH); //blue
     }
     else if (state == 2) {
        digitalWrite(2, LOW);  //red
        digitalWrite(3, HIGH); //blue
        digitalWrite(4, HIGH); //red
        digitalWrite(5, LOW);  //blue
     } 
}

}
