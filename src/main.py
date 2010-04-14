import threading
import serveraction
import listener
from connection import *
from packedmessage import *

class ListenThread(threading.Thread):
   
   def run(self):
      listen = Listen(2000)
      
      #keep accepting new incoming requests
      while 1:
         #when you found a new connection, send the data in a new thread, to be able to keep
         #listening in this thread for other requests.
         conn = listening.accept()
         s = ServerAction()
         s.addinfo(conn[0], conn[1])
         s.start()
      
      
if __name__ == '__main__':
   control = Connection(*CONTROL_SERVER)
   
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
