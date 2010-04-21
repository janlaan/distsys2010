from connection import *
from packedmessage import *
import threading
import serveraction
import log, logging

logInstance = log.logger('listener')
logger = logging.getLogger('listener')
log.logger.init(logInstance, self.logger)
logger.info('Listener started')
class Listener(threading.Thread):
   
   def __init__(self):
      super(Listener, self).__init__()
      
   def run(self):
      listen = Listen(2001)

      while 1:
         conn = listen.accept()[0]
         c = Connection(conn)
         t = Clientconn(c)
         t.start()

class Clientconn(threading.Thread):
   def __init__(self, conn):
      super(Clientconn, self).__init__()
      self.client = conn
      #self.client.settimeout(2)

   def run(self):
      while 1:
         msg = self.client.receive()
         
         if len(msg) == 0:
            logger.debug("empty message from %s" % self.client.getaddress()[0])
            self.sock.close()
            break
         logger.debug("message received from %s" % self.client.getaddress()[0])
         logger.debug("message = %s" % msg)
         
         if msg:
            decoded = Unpacker(msg).get()
            s = serveraction.ServerAction(decoded[1], decoded[2], self.client, '')
            s.start()
