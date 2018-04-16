#include <Servo.h>

Servo servo_x;
Servo servo_y; 

String command; 
int pos_x = 0;
int pos_y = 0;
int ang_x = 0;
int ang_y = 0;
int opt = 0; 
int l_pos_x = 0;
int l_pos_y = 0; 
int sweep_x = 0; 
int sweep_y = 0;
int z = 0;

void setup() 

{
  servo_x.attach(6);
  servo_y.attach(7);
  
  Serial.begin(115200);
}


void loop() {

  if(Serial.available())
  {
    char c = Serial.read();
    //Serial.print(c);

    if(c == '\n')
    {
      //parsing string to find x and y offset
       parseCommand(command);

      //calculationg sweep angle for x
       sweepang(pos_x,0, l_pos_x, sweep_x);
      
      //calculationg sweep angle for y
       sweepang(pos_y,1, l_pos_y, sweep_y);

      l_pos_x = pos_x;
      l_pos_y = pos_y; 
      
      //Reset command
       command = "";

       servo_x.write(ang_x);
       delay(15);
       servo_y.write(ang_y);
       delay(15);
    }
    else 
    {
      command+= c;
    }
  }
}

void parseCommand(String com) 
{
  String x;
  String y;

  x = com.substring(0, com.indexOf(0 , com.indexOf(",")));

//  Serial.print(x);
//  Serial.print(" ");
  
  y = com.substring(com.indexOf(",") + 1 );

//  Serial.println(y);

  pos_x = x.toInt();
//  Serial.print(pos_x);
//  Serial.print(" ");
  pos_y = y.toInt();
//  Serial.print(pos_y);
//  Serial.println();
}

void sweepang(int x, int opt, int l_pos, int sweep)
{
  int dir = 0; 
  int diff = 0;
  int off_set = 0;
  int stat_set = 0;
  int x_abs = 0;

  x_abs = abs(x);
  diff = abs(l_pos - x);
  
  //stat_set = map(x_abs,0,320, 1, 3);
  //off_set = map(diff,0,100,1,10);
  off_set = 1;
  
  if ( x > 10 )
  {
   
    if (opt == 1 ) 
    {
      sweep = sweep + off_set + stat_set;
    }
    else 
    {
      sweep = sweep - off_set - stat_set;
    }

    if (sweep >= 181)
    {
      sweep = 180; 

    }

    if (sweep <= 0)
    {
      sweep = 0; 
    }
  }

  
  if ( x  <  -10 )
  {

       
    if (opt == 1 ) 
    {
      sweep = sweep - off_set - stat_set;
    }
    else 
    {
     sweep = sweep + off_set + stat_set; 
    }

    
    if (sweep >= 181)
    {
      sweep = 180; 

    }

    if (sweep <= 0)
    {
      sweep = 0; 
    }
  }

  if ( opt == 0 )
  {
    sweep_x = sweep; 
    ang_x = sweep; 
    
    //Serial.print(ang_x);
    //Serial.print(" ");
  }
  else if  (opt == 1)
  { 
    sweep_y = sweep;
    ang_y = sweep; 
    
    //Serial.print(ang_y);
    //Serial.println();
  }

  else 
  {
    return; 
  }
 
  
}

