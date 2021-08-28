void slider( Control* sender, int type ) {

}
void buttonCallback( Control* sender, int type ) {
  switch ( type ) {
    case B_DOWN:
      break;

    case B_UP:
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
      if(sender->id==joystick2)
      {
        RotLeft.state=1;
      }

      break;

    case P_LEFT_UP:

      if(sender->id==joystick1)
      {
        Left.state=0;
      }
      if(sender->id==joystick2)
      {
        RotLeft.state=0;
      }
      break;

    case P_RIGHT_DOWN:

      if(sender->id==joystick1)
      {
        Right.state=1;
      }
      if(sender->id==joystick2)
      {
        RotRight.state=1;
      }
      break;

    case P_RIGHT_UP:

      if(sender->id==joystick1)
      {
        Right.state=0;
      }
      if(sender->id==joystick2)
      {
        RotRight.state=0;
      }
      break;
 
    case P_FOR_DOWN:

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

      if(sender->id==joystick1)
      {
        Centre.state=1;
      }
      break;

    case P_CENTER_UP:

      if(sender->id==joystick1)
      {
        Centre.state=0;
      }
      break;
  }

}

void switchExample( Control* sender, int value ) {
  switch ( value ) {
    case S_ACTIVE:

      if(sender->id==switch1)
      {
        modes=1;
        ESPUI.updateControlValue(status2,Modes[modes]);
      }
      break;

    case S_INACTIVE:

      if(sender->id==switch1)
      {
        modes=0;
        ESPUI.updateControlValue(status2,Modes[modes]);
      }
      break;
  }

}
