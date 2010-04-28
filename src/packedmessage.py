import struct, log, logging

logInstance = log.logger('packer')
pplogger = logging.getLogger('packer')
log.logger.init(logInstance, pplogger)
pplogger.info('Packer log started')

class Packer:
   """
   Packs a message
   """
   def __init__(self, msgtype, message):
      msglen = len(message)
      pplogger.info("Packing (%d) %s" % (msgtype, message))
      self.msg = struct.pack("!HH%ds" % msglen, msglen + 4, msgtype, message)
   
   def get(self):
      return self.msg
   
class Unpacker:
   """
   Unpacks a message
   """
   def __init__(self, packed):
      msglen = len(packed)
      pplogger.info("Unpacking something with length %d" % msglen)
      self.msg = struct.unpack("!HH%ds" % (msglen - 4), packed)
   
   def get(self):
      return self.msg

