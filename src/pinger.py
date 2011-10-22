import threading
import time
import actions
from database import *

logInstance = log.logger('pinger')
plogger = logging.getLogger('pinger')
log.logger.init(logInstance, plogger)
plogger.info('Pinger started')

class Pinger(threading.Thread):
   """
   Pings all connected clients for activity.
   Drops them when they are not responding to pings.
   """

   def run(self):
      pinged = {}
      
      while 1:
         allclients = DB.get_all_connections()
         for c in allclients:
            #go through all connected clients and see if they need to be pinged for inactivity.
            if c['socket'] and c['last_action'] < (time.time() - 30):
               if pinged[c['name']]:
                  #You've already pinged this client, check if it has ponged in time.
                  if pinged[c['name']] < time.time() - 5:
                     #irresponsive client, drop it
                     plogger.info("Client %s (%s) didn't respond to ping, dropping it."\
                        % (c['name'], c['socket'].getaddress()[0]))
                     actions.drop_client_by_socket(c['socket'])
                     
               else:
                  #Clients needs to be pinged: do it.
                  pinged[c['name']] = time.time()
                  plogger.info("Client %s (%s) inactive for over 30 s. Sending ping"\
                     % (c['name'], c['socket'].getaddress()[0]))
                  actions.unicast(140, 'letsping', c['socket'])
               
            else:
               #This client has recent activity, don't ping.
               pinged[c['name']] = None
         time.sleep(1)
