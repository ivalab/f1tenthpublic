#!/usr/bin/env python

import rospy
from race.msg import drive_param

from dynamic_reconfigure.server import Server
from race.cfg import carControlConfig

import sys, select, termios, tty


speed = 0
turn = 0

def callback(config, level):
    global speed 
    speed = config.Speed
    global turn
    turn = config.Turn
    return config

pub = rospy.Publisher('drive_parameters', drive_param, queue_size=10)

keyBindings = {
  'w':(1,0),
  'd':(1,1),
  'a':(1,-1),
  's':(0,0),
}

def getKey():
   tty.setraw(sys.stdin.fileno())
   select.select([sys.stdin], [], [], 0)
   key = sys.stdin.read(1)
   termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
   return key

#speed_factor = 1
#turn_factor = 1

if __name__=="__main__":

  settings = termios.tcgetattr(sys.stdin)
  rospy.init_node('keyboard', anonymous=True)
  
  speed_key = 0
  trun_key  = 0
  status = 0
  
  srv = Server(carControlConfig, callback)

  try:
    while(1):
       key = getKey()
       if key in keyBindings.keys():
          speed_key = keyBindings[key][0]
          turn_key = keyBindings[key][1]
       else:
          #speed = 0
          #turn = 0
          if (key == '\x03'):
             break
       msg = drive_param()

       #msg.velocity = speed*speed_factor
       #msg.angle = turn*turn_factor
       msg.velocity = speed_key*speed
       msg.angle = turn_key*turn

       pub.publish(msg)

  except:
    print 'error'

  finally:
    msg = drive_param()


    msg.velocity = 0
    msg.angle = 0
    pub.publish(msg)

    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    
