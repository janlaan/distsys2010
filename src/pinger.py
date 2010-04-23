import threading
import time
from actions import *
from database import *

logInstance = log.logger('pinger')
plogger = logging.getLogger('pinger')
log.logger.init(logInstance, plogger)
plogger.info('Pinger started')

class Pinger(threading.Thread):

   def run(self):
      pinged = {}
      
      while 1:
         allclients = DB.get_all_connections()
         for c in allclients:
            if c['last_action'] < (time.time() - 30):
               if pinged[c['name']]:
                  if pinged[c['name']] < time.time() - 5:
                     #irresponsive client, drop it
                     plogger.info("Client %s (%s) didn't respond to ping, dropping it."\
                        % (c['name'], c['socket'].getaddress()[0]))
                     drop_client_by_socket(c['socket'])
                     
                  continue
                  
               pinged[c['name']] = time.time()
               plogger.info("Client %s (%s) inactive for over 30 s. Sending ping"\
                  % (c['name'], c['socket'].getaddress()[0]))
               unicast(140, 'letsping', c['socket'])
               
            else:
               pinged[c['name']] = None
         time.sleep(1)
