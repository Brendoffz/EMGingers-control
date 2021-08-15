class Buttons {
private:
  int ID;
public:
  bool state;
  unsigned long interval =100;
  Buttons(int ID){
  this->ID=ID;
  init();
  }
  void init()
  {
    state=0;
  }
};
