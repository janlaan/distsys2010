import threading
import serveraction
import listener
import pinger
import sys
from database import *
from connection import *
from packedmessage import *
      
if __name__ == '__main__':
   
   control = Connection(*DB.control_server)
   
   DB.insert(control.getaddress()[0], control, 'control_server', CONTROL_SERVER)
   my_ip = socket.gethostbyname(socket.gethostname())
   sendmsg = my_ip + ':2001 :weeeeeeeee'
   
   control.send(Packer(601, sendmsg).get())

   l = listener.Listener()
   l.start()
   
   p = pinger.Pinger()
   p.start()
   while 1: 
      #recieve incoming messages from the control server
      in_msg = control.receive()
      if len(in_msg) == 0:
         print "CONTROL SERVER CLOSED CONNECTION!!! (why?)"
         sys.exit()
      decoded = Unpacker(in_msg)
      dec_msg = decoded.get()
      
      s = serveraction.ServerAction(dec_msg[1], dec_msg[2], control, '')
      s.start()
