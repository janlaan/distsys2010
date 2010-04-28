import threading
import serveraction
import listener
import pinger
import sys
from database import *
from connection import *
from packedmessage import *
import log, logging

logInstance = log.logger('main')
mlogger = logging.getLogger('main')
log.logger.init(logInstance, mlogger)
mlogger.info('Listener started')

if __name__ == '__main__':
   """
   Main body of the chatserver, this starts all other components 
   and upholds the connection to the control server
   """
   #connect to control server
   control = Connection(*DB.control_server)
   
   DB.insert(control.getaddress()[0], control, 'control_server', CONTROL_SERVER)
   my_ip = socket.gethostbyname(socket.gethostname())
   sendmsg = my_ip + ':2001 :weeeeeeeee'
   mlogger.info('Connecting to control server')
   control.send(Packer(601, sendmsg).get())
   
   #start listening for incoming message from other servers/clients
   l = listener.Listener()
   l.start()
   
   #Start the pinger that pings inactive clients/servers
   p = pinger.Pinger()
   p.start()
   global sys_exit
   
   sys_exit = False
   #listen to the control server
   while 1: 
      if DB.get_exit():
         print "server going down"
         sys.exit()
      #recieve incoming messages from the control server
      in_msg = control.receive()
      if len(in_msg) == 0:
         mlogger.info("CONTROL SERVER CLOSED CONNECTION! (why?) Reconnecting now.")
         #create new connection to control server
         DB.remove_by_socket(control)
         control = Connection(*DB.control_server)
         DB.insert(control.getaddress()[0], control, 'control_server', CONTROL_SERVER)
         control.send(Packer(601, sendmsg).get())
         
      else:
         #process the message
         decoded = Unpacker(in_msg)
         dec_msg = decoded.get()
         
         s = serveraction.ServerAction(dec_msg[1], dec_msg[2], control, '')
         s.start()
