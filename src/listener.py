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
   """
   Opens a listen connection on port 2001.
   This enables clients and other servers to conenct to this one.
   """
   def run(self):
      listen = Listen(2001)

      while 1:
         #wait for new connections (blocking)
         conn = listen.accept()[0]
         c = Connection(conn)
         t = Clientconn(c)
         t.start()

class Clientconn(threading.Thread):
   """
   Maintain a connection with newly acquired clients/servers
   Enables you to read incoming messages.
   """
   def __init__(self, conn):
      super(Clientconn, self).__init__()
      self.client = conn

   def run(self):
      while 1:
         #wait for the next message, 
         msg = self.client.receive()
         
         if len(msg) == 0:
            #for some reason, the connection was closed from the other end.
            #remove the client.
            logger.debug("empty message from %s. Assuming client dead." % self.client.getaddress()[0])
            actions.drop_client_by_socket(self.client)
            del(self.sock)
            return
         
         logger.debug("Recieved message from %s" % self.client.getaddress()[0])
         
         if msg:
            #unpack the received message and process it.
            decoded = Unpacker(msg).get()
            s = serveraction.ServerAction(decoded[1], decoded[2], self.client, '')
            s.start()
