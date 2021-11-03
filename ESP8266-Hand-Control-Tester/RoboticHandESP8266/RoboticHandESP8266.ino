// Import required libraries
#include <Arduino.h>
#include <Arduino.h>
#ifdef ESP32
  #include <WiFi.h>
  #include <AsyncTCP.h>
#else
  #include <ESP8266WiFi.h>
  #include <ESPAsyncTCP.h>
#endif
#include <ESPAsyncWebServer.h>

//servo
#include <Wire.h>

#include <Adafruit_PWMServoDriver.h>
Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver(0x40);
#define SERVOMIN  150 // This is the 'minimum' pulse length count (out of 4096)
#define SERVOMAX  600 // This is the 'maximum' pulse length count (out of 4096)
#define USMIN  600 // This is the rounded 'minimum' microsecond length based on the minimum pulse of 150
#define USMAX  2400 // This is the rounded 'maximum' microsecond length based on the maximum pulse of 600
#define SERVO_FREQ 50 // Analog servos run at ~50 Hz updates
uint8_t servonum1 = 0;
uint8_t servonum2 = 1;
uint8_t servonum3 = 2;
uint8_t servonum4 = 3;
uint8_t servonum5 = 4;
uint8_t servonum6 = 5;
uint8_t servonum7 = 6;
uint8_t servonum8 = 7;
uint8_t servonum9 = 8;
uint8_t servonum10 = 9;
//servo

// Replace with your network credentials
const char* ssid = "ASUS";
const char* password = "bingrui123";

//Other Var
unsigned long previousMillis2 = 0;
const long interval2 = 500; 
int value1=90;
int value2=90;
int value3=90;
int value4=90;
int value5=90;
int value6=88;
int value7=88;
int value8=88;
int value9=88;
int value10=88;
int microsec1;
int microsec2;
int microsec3;
int microsec4;
int microsec5;
int microsec6;
int microsec7;
int microsec8;
int microsec9;
int microsec10;
//Other Var

// current temperature & humidity, updated in loop()
const char* PARAM_INPUT_1 = "input1";
const char* PARAM_INPUT_2 = "input2";
const char* PARAM_INPUT_3 = "input3";
const char* PARAM_INPUT_4 = "input4";
const char* PARAM_INPUT_5 = "input5";
const char* PARAM_INPUT_6 = "input6";
const char* PARAM_INPUT_7 = "input7";
const char* PARAM_INPUT_8 = "input8";
const char* PARAM_INPUT_9 = "input9";
const char* PARAM_INPUT_10 = "input10";
// Create AsyncWebServer object on port 80
AsyncWebServer server(80);

const char index_html[] PROGMEM = R"rawliteral(
<!DOCTYPE HTML><html>
<head>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.15.1/css/all.css" integrity="998e14e9de" crossorigin="anonymous">
  <style>
    html {
     font-family: Arial;
     display: inline-block;
     margin: 0px auto;
     text-align: center;
    }
    h2 { font-size: 3.0rem; }
    p { font-size: 3.0rem; }
    .units { font-size: 1.2rem; }
    .labels{
      font-size: 1.5rem;
      vertical-align:middle;
      padding-bottom: 15px;
    }
  </style>
</head>
<body>
  <h2>Robotic Hand Web Server</h2>
  <p>
    <i class="fas fa-hand-point-up" style="color:#059e8a;"></i>
    <span class="labels">Thumb Finger Flex</span> 
    <span id="thumbfingerflex">%THUMBFINGERFLEX%</span>
    <sup class="units">&deg;</sup>
    <form action="/get">
    Thumb Finger Flex Position: <input type="text" name="input1">
    <input type="submit" value="Submit">
  </form><br>
  </p>
  
  <p>
    <i class="fas fa-hand-point-up" style="color:#059e8a;"></i>
    <span class="labels">Thumb Finger Yaw</span> 
    <span id="thumbfingeryaw">%THUMBFINGERYAW%</span>
    <sup class="units">&deg;</sup>
    <form action="/get">
    Thumb Finger Yaw Position: <input type="text" name="input2">
    <input type="submit" value="Submit">
  </form><br>
  </p>
  
  <p>
    <i class="fas fa-hand-point-up" style="color:#000cff;"></i>
    <span class="labels">Index Finger Flex</span> 
    <span id="indexfingerflex">%INDEXFINGERFLEX%</span>
    <sup class="units">&deg;</sup>
    <form action="/get">
    Index Finger Flex Position: <input type="text" name="input3">
    <input type="submit" value="Submit">
  </form><br>
  </p>

  <p>
    <i class="fas fa-hand-point-up" style="color:#000cff;"></i>
    <span class="labels">Index Finger Yaw</span> 
    <span id="indexfingeryaw">%INDEXFINGERYAW%</span>
    <sup class="units">&deg;</sup>
    <form action="/get">
    Index Finger Yaw Position: <input type="text" name="input4">
    <input type="submit" value="Submit">
  </form><br>
  </p>
  
  <p>
    <i class="fas fa-hand-point-up" style="color:#FF00DC;"></i>
    <span class="labels">Middle Finger Flex</span> 
    <span id="middlefingerflex">%MIDDLEFINGERFLEX%</span>
    <sup class="units">&deg;</sup>
    <form action="/get">
    Middle Finger Flex Position: <input type="text" name="input5">
    <input type="submit" value="Submit">
  </form><br>
  </p>

  <p>
    <i class="fas fa-hand-point-up" style="color:#FF00DC;"></i>
    <span class="labels">Middle Finger Yaw</span> 
    <span id="middlefingeryaw">%MIDDLEFINGERYAW%</span>
    <sup class="units">&deg;</sup>
    <form action="/get">
    Middle Finger Yaw Position: <input type="text" name="input6">
    <input type="submit" value="Submit">
  </form><br>
  </p>
  
  <p>
    <i class="fas fa-hand-point-up" style="color:#FF0000;"></i>
    <span class="labels">Ring Finger Flex</span> 
    <span id="ringfingerflex">%RINGFINGERFLEX%</span>
    <sup class="units">&deg;</sup>
    <form action="/get">
    Ring Finger Flex Position: <input type="text" name="input7">
    <input type="submit" value="Submit">
  </form><br>
  </p>

  <p>
    <i class="fas fa-hand-point-up" style="color:#FF0000;"></i>
    <span class="labels">Ring Finger Yaw</span> 
    <span id="ringfingeryaw">%RINGFINGERYAW%</span>
    <sup class="units">&deg;</sup>
    <form action="/get">
    Ring Finger Yaw Position: <input type="text" name="input8">
    <input type="submit" value="Submit">
  </form><br>
  </p>
  
  <p>
    <i class="fas fa-hand-point-up" style="color:#F7FF00;"></i>
    <span class="labels">Pinky Finger Flex</span> 
    <span id="pinkyfingerflex">%PINKYFINGERFLEX%</span>
    <sup class="units">&deg;</sup>
    <form action="/get">
    Pinky Finger Flex Position: <input type="text" name="input9">
    <input type="submit" value="Submit">
  </form><br>
  </p>

  <p>
    <i class="fas fa-hand-point-up" style="color:#F7FF00;"></i>
    <span class="labels">Pinky Finger Yaw</span> 
    <span id="pinkyfingeryaw">%PINKYFINGERYAW%</span>
    <sup class="units">&deg;</sup>
    <form action="/get">
    Pinky Finger Yaw Position: <input type="text" name="input10">
    <input type="submit" value="Submit">
  </form><br>
  </p>
  
</body>
<script>
setInterval(function ( ) {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      document.getElementById("thumbfingerflex").innerHTML = this.responseText;
    }
  };
  xhttp.open("GET", "/thumbfingerflex", true);
  xhttp.send();
}, 10000 ) ;

setInterval(function ( ) {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      document.getElementById("thumbfingeryaw").innerHTML = this.responseText;
    }
  };
  xhttp.open("GET", "/thumbfingeryaw", true);
  xhttp.send();
}, 10000 ) ;

setInterval(function ( ) {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      document.getElementById("indexfingerflex").innerHTML = this.responseText;
    }
  };
  xhttp.open("GET", "/indexfingerflex", true);
  xhttp.send();
}, 10000 ) ;

setInterval(function ( ) {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      document.getElementById("indexfingeryaw").innerHTML = this.responseText;
    }
  };
  xhttp.open("GET", "/indexfingeryaw", true);
  xhttp.send();
}, 10000 ) ;

setInterval(function ( ) {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      document.getElementById("middlefingerflex").innerHTML = this.responseText;
    }
  };
  xhttp.open("GET", "/middlefingerflex", true);
  xhttp.send();
}, 10000 ) ;

setInterval(function ( ) {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      document.getElementById("middlefingeryaw").innerHTML = this.responseText;
    }
  };
  xhttp.open("GET", "/middlefingeryaw", true);
  xhttp.send();
}, 10000 ) ;

setInterval(function ( ) {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      document.getElementById("ringfingerflex").innerHTML = this.responseText;
    }
  };
  xhttp.open("GET", "/ringfingerflex", true);
  xhttp.send();
}, 10000 ) ;

setInterval(function ( ) {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      document.getElementById("ringfingeryaw").innerHTML = this.responseText;
    }
  };
  xhttp.open("GET", "/ringfingeryaw", true);
  xhttp.send();
}, 10000 ) ;

setInterval(function ( ) {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      document.getElementById("pinkyfingerflex").innerHTML = this.responseText;
    }
  };
  xhttp.open("GET", "/pinkyfingerflex", true);
  xhttp.send();
}, 10000 ) ;

setInterval(function ( ) {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      document.getElementById("pinkyfingeryaw").innerHTML = this.responseText;
    }
  };
  xhttp.open("GET", "/pinkyfingeryaw", true);
  xhttp.send();
}, 10000 ) ;



</script>
</html>)rawliteral";


String processor(const String& var){
  //Serial.println(var);
  if(var == "THUMBFINGERFLEX"){
    return String(value1);
  }
  else if(var == "THUMBFINGERYAW"){
    return String(value2);
  }
  else if(var == "INDEXFINGERFLEX"){
    return String(value3);
  }
  else if(var == "INDEXFINGERYAW"){
    return String(value4);
  }
  else if(var == "MIDDLEFINGERFLEX"){
    return String(value5);
  }
  else if(var == "MIDDLEFINGERYAW"){
    return String(value6);
  }else if(var == "RINGFINGERFLEX"){
    return String(value7);
  }
  else if(var == "RINGFINGERYAW"){
    return String(value8);
  }else if(var == "PINKYFINGERFLEX"){
    return String(value9);
  }
  else if(var == "PINKYFINGERYAW"){
    return String(value10);
  }
  return String();
}

void setup(){
  // Serial port for debugging purposes
  Serial.begin(115200);
  pwm.begin();//start servo
  pwm.setOscillatorFrequency(27000000);
  pwm.setPWMFreq(SERVO_FREQ);  // Analog servos run at ~50 Hz updates

  
  // Connect to Wi-Fi
  WiFi.begin(ssid, password);
  Serial.println("Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println(".");
  }

  // Print ESP8266 Local IP Address
  Serial.println(WiFi.localIP());

  // Route for root / web page
  server.on("/", HTTP_GET, [](AsyncWebServerRequest *request){
    request->send_P(200, "text/html", index_html, processor);
  });
  server.on("/thumbfingerflex", HTTP_GET, [](AsyncWebServerRequest *request){
    request->send_P(200, "text/plain", String(value1).c_str());
  });
  server.on("/thumbfingeryaw", HTTP_GET, [](AsyncWebServerRequest *request){
    request->send_P(200, "text/plain", String(value2).c_str());
  });
  server.on("/indexfingerflex", HTTP_GET, [](AsyncWebServerRequest *request){
    request->send_P(200, "text/plain", String(value3).c_str());
  });
  server.on("/indexfingeryaw", HTTP_GET, [](AsyncWebServerRequest *request){
    request->send_P(200, "text/plain", String(value4).c_str());
  });
  server.on("/middlefingerflex", HTTP_GET, [](AsyncWebServerRequest *request){
    request->send_P(200, "text/plain", String(value5).c_str());
  });
  server.on("/middlefingeryaw", HTTP_GET, [](AsyncWebServerRequest *request){
    request->send_P(200, "text/plain", String(value6).c_str());
  });
  server.on("/ringfingerflex", HTTP_GET, [](AsyncWebServerRequest *request){
    request->send_P(200, "text/plain", String(value7).c_str());
  });
  server.on("/ringfingeryaw", HTTP_GET, [](AsyncWebServerRequest *request){
    request->send_P(200, "text/plain", String(value8).c_str());
  });
  server.on("/pinkyfingerflex", HTTP_GET, [](AsyncWebServerRequest *request){
    request->send_P(200, "text/plain", String(value9).c_str());
  });
  server.on("/pinkyfingeryaw", HTTP_GET, [](AsyncWebServerRequest *request){
    request->send_P(200, "text/plain", String(value10).c_str());
  });

  // Send a GET request to <ESP_IP>/get?input1=<inputMessage>
  server.on("/get", HTTP_GET, [] (AsyncWebServerRequest *request) {
    String inputMessage;
    String inputParam;
    // GET input1 value on <ESP_IP>/get?input1=<inputMessage>
    if (request->hasParam(PARAM_INPUT_1)) {
      inputMessage = request->getParam(PARAM_INPUT_1)->value();
      inputParam = PARAM_INPUT_1;
    }
    // GET input2 value on <ESP_IP>/get?input2=<inputMessage>
    else if (request->hasParam(PARAM_INPUT_2)) {
      inputMessage = request->getParam(PARAM_INPUT_2)->value();
      inputParam = PARAM_INPUT_2;
    }
    // GET input3 value on <ESP_IP>/get?input3=<inputMessage>
    else if (request->hasParam(PARAM_INPUT_3)) {
      inputMessage = request->getParam(PARAM_INPUT_3)->value();
      inputParam = PARAM_INPUT_3;
    }
    else if (request->hasParam(PARAM_INPUT_4)) {
      inputMessage = request->getParam(PARAM_INPUT_4)->value();
      inputParam = PARAM_INPUT_4;
    }
    else if (request->hasParam(PARAM_INPUT_5)) {
      inputMessage = request->getParam(PARAM_INPUT_5)->value();
      inputParam = PARAM_INPUT_5;
    }
    else if (request->hasParam(PARAM_INPUT_6)) {
      inputMessage = request->getParam(PARAM_INPUT_6)->value();
      inputParam = PARAM_INPUT_6;
    }
    else if (request->hasParam(PARAM_INPUT_7)) {
      inputMessage = request->getParam(PARAM_INPUT_7)->value();
      inputParam = PARAM_INPUT_7;
    }
    else if (request->hasParam(PARAM_INPUT_8)) {
      inputMessage = request->getParam(PARAM_INPUT_8)->value();
      inputParam = PARAM_INPUT_8;
    }
    else if (request->hasParam(PARAM_INPUT_9)) {
      inputMessage = request->getParam(PARAM_INPUT_9)->value();
      inputParam = PARAM_INPUT_9;
    }
    else if (request->hasParam(PARAM_INPUT_10)) {
      inputMessage = request->getParam(PARAM_INPUT_10)->value();
      inputParam = PARAM_INPUT_10;
    }
    else {
      inputMessage = "No message sent";
      inputParam = "none";
    }
    if (inputParam == PARAM_INPUT_1)
    {
    value1=round(inputMessage.toInt());
    if(value1>180)
    {
      value1=180;
    }
    else if (value1<0)
    {
      value1=0;
    }
    Serial.println("PARAM_INPUT_1");
    Serial.println(value1);
    
    }
    else if(inputParam == PARAM_INPUT_2)
    {
    value2=round(inputMessage.toInt());
    if(value2>180)
    {
      value2=180;
    }
    else if (value2<0)
    {
      value2=0;
    }
    Serial.println("PARAM_INPUT_2");
    Serial.println(value2);
    
    }
    else if(inputParam == PARAM_INPUT_3)
    {
    value3=round(inputMessage.toInt());
    if(value3>180)
    {
      value3=180;
    }
    else if (value3<0)
    {
      value3=0;
    }
    Serial.println("PARAM_INPUT_35");
    Serial.println(value3);
    
    }
    else if(inputParam == PARAM_INPUT_4)
    {
    value4=round(inputMessage.toInt());
    if(value4>180)
    {
      value4=180;
    }
    else if (value4<0)
    {
      value4=0;
    }
    Serial.println("PARAM_INPUT_4");
    Serial.println(value4);
    
    }
    else if(inputParam == PARAM_INPUT_5)
    {
    value5=round(inputMessage.toInt());
    if(value5>180)
    {
      value5=180;
    }
    else if (value5<0)
    {
      value5=0;
    }
    Serial.println("PARAM_INPUT_5");
    Serial.println(value5);
    
    }
    else if(inputParam == PARAM_INPUT_6)
    {
    value6=round(inputMessage.toInt());
    if(value6>180)
    {
      value6=180;
    }
    else if (value6<0)
    {
      value6=0;
    }
    Serial.println("PARAM_INPUT_6");
    Serial.println(value6);
    
    }
    else if(inputParam == PARAM_INPUT_7)
    {
    value7=round(inputMessage.toInt());
    if(value7>180)
    {
      value7=180;
    }
    else if (value7<0)
    {
      value7=0;
    }
    Serial.println("PARAM_INPUT_7");
    Serial.println(value7);
    
    }
    else if(inputParam == PARAM_INPUT_8)
    {
    value8=round(inputMessage.toInt());
    if(value8>180)
    {
      value8=180;
    }
    else if (value8<0)
    {
      value8=0;
    }
    Serial.println("PARAM_INPUT_8");
    Serial.println(value8);
    
    }
    else if(inputParam == PARAM_INPUT_9)
    {
    value9=round(inputMessage.toInt());
    if(value9>180)
    {
      value9=180;
    }
    else if (value9<0)
    {
      value9=0;
    }
    Serial.println("PARAM_INPUT_9");
    Serial.println(value9);
    
    }
    else if(inputParam == PARAM_INPUT_10)
    {
    value10=round(inputMessage.toInt());
    if(value10>180)
    {
      value2=180;
    }
    else if (value10<0)
    {
      value10=0;
    }
    Serial.println("PARAM_INPUT_10");
    Serial.println(value10);
    
    }
    request->send_P(200, "text/html", index_html, processor);
    });

  // Start server
  server.begin();
}
void UpdateMS()
{
    microsec1= map(value1,0,180,USMIN,USMAX);
    microsec2= map(value2,0,180,USMIN,USMAX);
    microsec3= map(value3,0,180,USMIN,USMAX);
    microsec4= map(value4,0,180,USMIN,USMAX);
    microsec5= map(value5,0,180,USMIN,USMAX);
    microsec6= map(value6,0,180,USMIN,USMAX);
    microsec7= map(value7,0,180,USMIN,USMAX);
    microsec8= map(value8,0,180,USMIN,USMAX);
    microsec9= map(value9,0,180,USMIN,USMAX);
    microsec10= map(value10,0,180,USMIN,USMAX); 
}
void loop(){  
  unsigned long currentMillis = millis();
  UpdateMS();
  if (currentMillis - previousMillis2 >= interval2) 
  {
      previousMillis2 = currentMillis;
      pwm.writeMicroseconds(servonum1,microsec1);
      pwm.writeMicroseconds(servonum2,microsec2);
      pwm.writeMicroseconds(servonum3,microsec3);
      pwm.writeMicroseconds(servonum4,microsec4);
      pwm.writeMicroseconds(servonum5,microsec5);
      pwm.writeMicroseconds(servonum6,microsec6);
      pwm.writeMicroseconds(servonum7,microsec7);
      pwm.writeMicroseconds(servonum8,microsec8);
      pwm.writeMicroseconds(servonum9,microsec9);
      pwm.writeMicroseconds(servonum10,microsec10);
  }

  #ifdef ESP8266
    yield();  // take a breather, required for ESP8266
  #endif
}
