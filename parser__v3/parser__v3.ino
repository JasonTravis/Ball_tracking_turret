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
int vel_x = 0;
int vel_y = 0;

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
       
       Serial.flush();

      //calculationg sweep angle for x
       sweepang(pos_x,0, l_pos_x, sweep_x, vel_x);
      
      //calculationg sweep angle for y
       sweepang(pos_y,1, l_pos_y, sweep_y, vel_y);

      l_pos_x = pos_x;
      l_pos_y = pos_y; 
      
      //Reset command
       command = "";

       servo_x.write(ang_x);
       //delay(15);
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
  String v_1;
  String v_2;
  String v_3;
  String v_4;

  String test; 
  
  int i = 1;
  int com_num = 4; 
  String v_name; 


  String temp; 
    
    v_1 = com.substring(0, com.indexOf(0 , com.indexOf(",")));
    temp = com.substring(com.indexOf(",") + 1 );
    
    v_2 = temp.substring(0, temp.indexOf(0 , temp.indexOf(",")));
    temp = v_2.substring(v_2.indexOf(",") + 1 );
    
    v_3 = temp.substring(0, temp.indexOf(0 , temp.indexOf(",")));
    temp = v_3.substring(v_3.indexOf(",") + 1 );
    
    v_4 = temp.substring(0, temp.indexOf(0 , temp.indexOf(",")));
      
   

  pos_x = v_1.toInt();
  pos_y = v_2.toInt();
  vel_x = v_3.toInt();
  vel_y = v_4.toInt();

//
//   Serial.print(pos_x); 
//   Serial.print(" "); 
//   Serial.print(pos_y); 
//   Serial.print(" ");
//   Serial.print(vel_x);
//   Serial.print(" "); 
//   Serial.println(vel_y); 
//   
}

void sweepang(int x, int opt, int l_pos, int sweep, int vel)
{
  int dir = 0; 
  int diff = 0;
  int off_set = 0;
  int stat_set = 0;
  int x_abs = 0;
  int v_abs = 0;

  v_abs = abs(vel);

  x_abs = abs(x);
  diff = abs(l_pos - x);
  
  stat_set = map(v_abs,300,2000, 1, 2);
  off_set = map(x_abs, 2, 200,0.1,5);
  
  //off_set = 1;
  
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

