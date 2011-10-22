import threading
from actions import *
import log, logging

global alogger

logInstance = log.logger('action')
alogger = logging.getLogger('action')
log.logger.init(logInstance, alogger)
alogger.info('Action logger started')

class ServerAction(threading.Thread):
   """
   Serveraction class. This class takes a message and decides what action to take.
   """
   def __init__(self, atype, message, client, address):
      """
      Add relevant info
      """
      super(ServerAction, self).__init__()
      self.action_type = atype
      self.message = message
      self.client = client
      self.address = address
   
   
   def run(self):
      """
      Process the received message based on its type.
      """
      alogger.info("Recieved message from %s, Message: (%d) %s" % (self.client.getaddress(), self.action_type, self.message))
      
      #Try to call th function associated with this message type.
      #format = "handle_<type>" (eg: handle_100)
      fn = globals().get("handle_" + str(self.action_type))
      if fn and callable(fn):
         fn(self.message, self.address, self.client)
      else:
         alogger.info("Received unknown message from %s, type: %d" % (self.client.getaddress(), self.action_type))

