import threading
import serveraction
import listener
import database
from connection import *
from packedmessage import *
      
if __name__ == '__main__':
   
   control = Connection(*database.DB.control_server)
   
   
   my_ip = socket.gethostbyname(socket.gethostname())
   print my_ip
   sendmsg = my_ip + ':2010:weeeeeeeee'

   control.send(Packer(601, sendmsg).get())

   l = listener.Listener()
   l.start()
   while 1: 
      #recieve incoming messages from the control server
      in_msg = control.receive()
      
      decoded = Unpacker(in_msg)
      dec_msg = decoded.get()
      
      s = serveraction.ServerAction(dec_msg[1], dec_msg[2], control, '')
      s.start()
