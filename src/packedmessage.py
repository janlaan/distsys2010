import struct, log, logging

logInstance = log.logger('packer')
pplogger = logging.getLogger('packer')
log.logger.init(logInstance, pplogger)
pplogger.info('Packer log started')

class Packer:

   def __init__(self, msgtype, message):
      msglen = len(message)
      
      self.msg = struct.pack('!HH'+str(msglen)+'s', msglen + 4, msgtype, message)
   
   def get(self):
      return self.msg
   
class Unpacker:
   def __init__(self, packed):
      msglen = len(packed)
      pplogger.debug("Unpacking something with length %d" % msglen)
      self.msg = struct.unpack('!HH'+str(msglen - 4)+'s', packed)
   
   def get(self):
      return self.msg

