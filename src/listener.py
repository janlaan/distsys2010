from connection import *
from packedmessage import *
import threading
import serveraction
import actions
import log, logging

logInstance = log.logger('listener')
logger = logging.getLogger('listener')
log.logger.init(logInstance, logger)
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
            #for some reason, the connection was closed from the other end.
            #remove the client.
            logger.debug("empty message from %s. Assuming client dead." % self.client.getaddress()[0])
            actions.drop_client_by_socket(self.client)
            del(self.sock)
            return
         
         logger.debug("Recieved message from %s" % self.client.getaddress()[0])
         logger.debug("Message = %s" % msg)
         
         if msg:
            decoded = Unpacker(msg).get()
            s = serveraction.ServerAction(decoded[1], decoded[2], self.client, '')
            s.start()
