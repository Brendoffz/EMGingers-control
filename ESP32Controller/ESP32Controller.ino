#include <DNSServer.h>
#include <ESPUI.h>
#include "secrets.h"
#include "buttons.h"
//#include "servocontrol.h"
#include <Preferences.h>
//6.10.1JSON

Preferences preferences;
 

const byte DNS_PORT = 53;
IPAddress apIP( 192, 168, 1, 1 );
DNSServer dnsServer;

#if defined(ESP32)
#include <WiFi.h>
#else
#include <ESP8266WiFi.h>
#endif

const char* ssid = SECRET_SSID;
const char* password = SECRET_PASS;
const char* hostname = "EMGingers";

uint16_t status1;
uint16_t status2;
uint16_t joystick1;
uint16_t joystick2;
uint16_t switch1;
uint16_t xlabel;
uint16_t ylabel;
uint16_t zlabel;
uint16_t xlabel2;
uint16_t ylabel2;
uint16_t zlabel2;
uint16_t rotlabel2;
uint16_t rotlabel;



float BatteryLevel;
String Modes[2]={"Joystick","Manual"};
bool modes=0;
float value1 = 0.0;
float value2 = 100.0;
float value3 = 100.0;
float value4 = 34.0;
float value5 = 29.0;
float value6 = 100.0;


Buttons Up(6);
Buttons Down(6);
Buttons Left(6);
Buttons Right(6);
Buttons Centre(6);
Buttons ZUp(7);
Buttons ZDown(7);
Buttons RotLeft(7);
Buttons RotRight(7);

unsigned long previousMillis=0;

int x,y,z;
int previousx=0;
int previousy=0;
int previousz=0;
float previousa=0.0;
float rotangle;
uint16_t coordianteprecision=1;
float angleprecision=0.5;


#include "contollers.h"




void setup( void ) {
  Serial.begin( 115200 );
  preferences.begin("coordinates", false);
  x = preferences.getInt("x", 0);
  Serial.println(x);
  y= preferences.getInt("y", 0);
  z = preferences.getInt("z", 0);
  rotangle = preferences.getFloat("rotangle", 0);
  pwm.begin();
  pwm.setPWMFreq(SERVO_FREQ);
#if defined(ESP32)
  WiFi.setHostname( hostname );
#else
  WiFi.hostname( hostname );
#endif

  // try to connect to existing network
  WiFi.begin( ssid, password );

  {
    Serial.println("WiFi Start");
    uint8_t timeout = 10;

    // Wait for connection, 5s timeout
    do {
      delay( 500 );
      timeout--;
    } while ( timeout && WiFi.status() != WL_CONNECTED );

    // not connected -> create hotspot
    if ( WiFi.status() != WL_CONNECTED ) {

      WiFi.mode( WIFI_AP );
      WiFi.softAPConfig( apIP, apIP, IPAddress( 255, 255, 255, 0 ) );
      WiFi.softAP( ssid );

      timeout = 5;

      do {
        delay( 500 );
        timeout--;
      } while ( timeout );
    }
  }
  Serial.println("WiFi Connected");
  
  dnsServer.start( DNS_PORT, "*", apIP );
  Serial.println( "\n\nWiFi parameters:" );
  Serial.print( "Mode: " );
  Serial.println( WiFi.getMode() == WIFI_AP ? "Station" : "Client" );
  Serial.print( "IP address: " );
  Serial.println( WiFi.getMode() == WIFI_AP ? WiFi.softAPIP() : WiFi.localIP() );


  uint16_t tab1 = ESPUI.addControl( ControlType::Tab, "Settings 1", "Joystick" );
  uint16_t tab2 = ESPUI.addControl( ControlType::Tab, "Settings 2", "Manual Control"  );
  uint16_t tab3 = ESPUI.addControl( ControlType::Tab, "Settings 3", "Other Data"  );

  // shown above all tabs
  status1 = ESPUI.addControl( ControlType::Label, "Battery %:", String(BatteryLevel,2), ControlColor::Turquoise );
  status2 = ESPUI.addControl( ControlType::Label, "Mode:", Modes[modes], ControlColor::Emerald );


  //tab 1 
  joystick1=ESPUI.addControl( ControlType::PadWithCenter, "Joystick", "", ControlColor::Peterriver, tab1, &padExample );
  joystick2=ESPUI.addControl( ControlType::Pad, "Up Down & Wrist Rotation", "", ControlColor::Wetasphalt, tab1, &padExample );
  xlabel2=ESPUI.addControl( ControlType::Label, "X Position:", String(x), ControlColor::Sunflower, tab1 );
  ylabel2=ESPUI.addControl( ControlType::Label, "Y Position:", String(y), ControlColor::Carrot, tab1 );
  zlabel2=ESPUI.addControl( ControlType::Label, "Z Position:", String(z), ControlColor::Alizarin, tab1 );
  rotlabel2=ESPUI.addControl( ControlType::Label, "Wrist Angle:", String(rotangle), ControlColor::Turquoise, tab1 );
  
  //tab 2
  switch1 = ESPUI.addControl( ControlType::Switcher, "Manual Control", "", ControlColor::Alizarin, tab2, &switchExample );
  ESPUI.addControl( ControlType::Slider, "Servo 1", "50", ControlColor::Turquoise, tab2, &slider );
  ESPUI.addControl( ControlType::Slider, "Servo 2", "0", ControlColor::Emerald, tab2, &slider );
  ESPUI.addControl( ControlType::Slider, "Servo 3", "0", ControlColor::Peterriver, tab2, &slider );
  ESPUI.addControl( ControlType::Slider, "Servo 4", "0", ControlColor::Wetasphalt, tab2, &slider );
  ESPUI.addControl( ControlType::Slider, "Servo 5", "0", ControlColor::Sunflower, tab2, &slider );
  ESPUI.addControl( ControlType::Slider, "Servo 6", "0", ControlColor::Carrot, tab2, &slider );

  //tab 3
  xlabel=ESPUI.addControl( ControlType::Label, "X Position:", String(x), ControlColor::Emerald, tab3 );
  ylabel=ESPUI.addControl( ControlType::Label, "Y Position:", String(y), ControlColor::Peterriver, tab3 );
  zlabel=ESPUI.addControl( ControlType::Label, "Z Position:", String(z), ControlColor::Wetasphalt, tab3 );
  rotlabel=ESPUI.addControl( ControlType::Label, "Wrist Angle:", String(rotangle), ControlColor::Turquoise, tab3 );

  //ESPUI.sliderContinuous = true;
  Serial.print( "Here" );
  ESPUI.begin("EMGingers's Robotic Arm");
  Serial.print( "Here" );
}


void updatecoordinate(int &x,int &y,int &z, float &rotangle)
{
  
  if (Up.state==1 && previousMillis+Up.interval<millis())
  {
    y+=coordianteprecision;
    previousMillis=millis();
  }
  if (Down.state==1 && previousMillis+Down.interval<millis())
  {
    y-=coordianteprecision;
    previousMillis=millis();
  }
  if (Left.state==1 && previousMillis+Left.interval<millis())
  {
    x-=coordianteprecision;
    previousMillis=millis();
  }
  if (Right.state==1 && previousMillis+Right.interval<millis())
  {
    x+=coordianteprecision;
    previousMillis=millis();
  }
  if (ZUp.state==1 && previousMillis+ZUp.interval<millis())
  {
    z+=coordianteprecision;
    previousMillis=millis();
  }
  if (ZDown.state==1 && previousMillis+ZDown.interval<millis())
  {
    z-=coordianteprecision;
    previousMillis=millis();
  }
  if (RotLeft.state==1 && previousMillis+ZDown.interval<millis())
  {
    rotangle-=angleprecision;
    previousMillis=millis();
  }
  if (RotRight.state==1 && previousMillis+ZDown.interval<millis())
  {
    rotangle+=angleprecision;
    previousMillis=millis();
  }
  
}
void UpdateValues()
{
  static long oldTime = 0;
  static long oldTime2 = 0;
  if ( millis() - oldTime > 500) 
  {
    if(previousx!=x)
    {
      ESPUI.updateControlValue(xlabel,String(x));
      ESPUI.updateControlValue(xlabel2,String(x));
      previousx=x;
      Serial.println(String(x)+','+String(y)+','+String(z));
    }
    if(previousy!=y)
    {
      ESPUI.updateControlValue(ylabel,String(y));
      ESPUI.updateControlValue(ylabel2,String(y));
      previousy=y;
      Serial.println(String(x)+','+String(y)+','+String(z));
    }

    if (previousz!=z) 
    {
      ESPUI.updateControlValue(zlabel,String(z));
      ESPUI.updateControlValue(zlabel2,String(z));
      previousz=z;
      Serial.println(String(x)+','+String(y)+','+String(z));
    }
    if (previousa!=rotangle) 
    {
      ESPUI.updateControlValue(rotlabel,String(rotangle));
      ESPUI.updateControlValue(rotlabel2,String(rotangle));
      previousa=rotangle;
      Serial.println(String(x)+','+String(y)+','+String(z));
    }
    oldTime = millis();
    Serial.println(String(x)+','+String(y)+','+String(z));
  }
  
}

void UpdateSpiffs()
{
    preferences.putInt("x", x);
    preferences.putInt("y", y);
    preferences.putInt("z", z);
    preferences.putFloat("rotangle", rotangle);
}
unsigned long previousMillis2=0;
const long interval2 = 500; 

void controlmotor()
{
  if (millis() - previousMillis2 >= interval2) 
  {
      previousMillis2 = millis();
      pwm.writeMicroseconds(0,map(map(value1,0,100,0,180),0,180,500,2500));//771-2193 for MG996R
      pwm.writeMicroseconds(1,map(map(value2,0,100,0,180),0,180,500,2500));
      pwm.writeMicroseconds(2,map(map(value3,0,100,0,180),0,180,500,2500));
      pwm.writeMicroseconds(3,map(map(value4,0,100,0,180),0,180,500,2400)); //500-2400 for SG90
      pwm.writeMicroseconds(4,map(map(value5,0,100,0,180),0,180,500,2400));
      pwm.writeMicroseconds(5,map(map(value6,0,100,0,180),0,180,500,2400));
      //Serial.println(String(value1)+','+String(value2)+','+String(value3));
}
}
void loop( void ) 
{
  dnsServer.processNextRequest();
  updatecoordinate(x,y,z,rotangle);
  UpdateValues();
  UpdateSpiffs();
  controlmotor();
  
}
