import threading
import serveraction
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
   
   sendmsg = '146.50.7.26:2000:weeeeeeeee'
   msg = MessagePacker(601, sendmsg)
   #print msg.get()
   control.send(msg.get())
   #control.send(str(21) + str(601) + '123213312312331:1')
   
   while 1: 
      #recieve incoming messages from the control server
      in_msg = control.receive()
      
      decoded = Unpacker(in_msg)
      dec_msg = decoded.get()
      
      s = serveraction.ServerAction(dec_msg[1], dec_msg[2], control, '')
      s.run()