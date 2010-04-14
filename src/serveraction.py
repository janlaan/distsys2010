import threading
from actions import *

class ServerAction(threading.Thread):
   """
   Parent ServerAction class.
   let other classes be child of this one.
   """
   def __init__(self, atype, message, client, address):
      super(ServerAction, self).__init__()
      self.action_type = atype
      self.message = message
      self.client = client
      self.address = address
   
   
   def run(self):
      #implement this for child-classes
      print 'i got a message, i am going to process it now'
      print "msg: (%d) %s from: %s" % (self.action_type, self.message, self.address)
      print self.client

      
      fn = globals().get("handle_" + str(self.action_type))
      if fn and callable(fn):
         fn(self.message, self.address, self.client)
      else:
         print 'fail'

