from connection import *
from packedmessage import *
import threading
import serveraction

class Listener(threading.Thread):
   
   def run(self):
      listen = Listen(2010)

      while 1:
         conn = listen.accept()[0]
         c = Connection(conn)
         t = Clientconn(c)
         t.start()

class Clientconn(threading.Thread):
   def __init__(self, conn):
      super(Clientconn, self).__init__()
      self.client = conn

   def run(self):
      while 1:
         msg = self.client.receive()
         decoded = Unpacker(msg).get()
         s = serveraction.ServerAction(decoded[1], decoded[2], self.client, '')
         s.start()
      
