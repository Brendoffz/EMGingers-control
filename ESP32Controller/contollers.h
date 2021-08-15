void slider( Control* sender, int type ) {
  Serial.print("Slider: ID: ");
  Serial.print(sender->id);
  Serial.print(", Value: ");
  Serial.println( sender->value );}

void buttonCallback( Control* sender, int type ) {
  switch ( type ) {
    case B_DOWN:
      Serial.println( "Button DOWN" );
      break;

    case B_UP:
      Serial.println( "Button UP" );
      break;
  }
}

void padExample( Control* sender, int value ) {
  switch ( value ) {
    case P_LEFT_DOWN:
      if(sender->id==joystick1)
      {
        Left.state=1;
      }
      Serial.print( "left down" );
      break;

    case P_LEFT_UP:
      Serial.print( "left up" );
      if(sender->id==joystick1)
      {
        Left.state=0;
      }
      break;

    case P_RIGHT_DOWN:
      Serial.print( "right down" );
      if(sender->id==joystick1)
      {
        Right.state=1;
      }
      break;

    case P_RIGHT_UP:
      Serial.print( "right up" );
      if(sender->id==joystick1)
      {
        Right.state=0;
      }
      break;

    case P_FOR_DOWN:
      Serial.print( "for down" );
      if(sender->id==joystick1)
      {
        Up.state=1;
      }
      if(sender->id==joystick2)
      {
        ZUp.state=1;
      }
      break;

    case P_FOR_UP:
      Serial.print( "for up" );
      if(sender->id==joystick1)
      {
        Up.state=0;
      }
      if(sender->id==joystick2)
      {
        ZUp.state=0;
      }
      break;

    case P_BACK_DOWN:
      Serial.print( "back down" );
      if(sender->id==joystick1)
      {
        Down.state=1;
      }
      if(sender->id==joystick2)
      {
        ZDown.state=1;
      }
      break;

    case P_BACK_UP:
      Serial.print( "back up" );
      if(sender->id==joystick1)
      {
        Down.state=0;
      }
      if(sender->id==joystick2)
      {
        ZDown.state=0;
      }
      break;

    case P_CENTER_DOWN:
      Serial.print( "center down" );
      if(sender->id==joystick1)
      {
        Centre.state=1;
      }
      break;

    case P_CENTER_UP:
      Serial.print( "center up" );
      if(sender->id==joystick1)
      {
        Centre.state=0;
      }
      break;
  }
  Serial.print( " " );
  Serial.println( sender->id );
}

void switchExample( Control* sender, int value ) {
  switch ( value ) {
    case S_ACTIVE:
      Serial.print( "Active:" );
      if(sender->id==switch1)
      {
        modes=1;
        ESPUI.updateControlValue(status2,Modes[modes]);
      }
      break;

    case S_INACTIVE:
      Serial.print( "Inactive" );
      if(sender->id==switch1)
      {
        modes=0;
        ESPUI.updateControlValue(status2,Modes[modes]);
      }
      break;
  }

  Serial.print( " " );
  Serial.println( sender->id );
}