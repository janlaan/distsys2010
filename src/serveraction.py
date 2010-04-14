import threading
from actions import *

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
      print "msg: (%d) %s from: %s" % (self.action_type, self.message, self.client.getaddress())
      
      #Try to call th function associated with this message type.
      fn = globals().get("handle_" + str(self.action_type))
      if fn and callable(fn):
         fn(self.message, self.address, self.client)
      else:
         print "Received unknown message type %d" % self.action_type

