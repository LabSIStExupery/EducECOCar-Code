unsigned char pot;

void setup() {
  pinMode(A0, INPUT);
  Serial.begin(9600);
}

void loop() {
  pot = analogRead(A0);
  Serial.println(pot);
  delay(500);
}
