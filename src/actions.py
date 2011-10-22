from connection import *
from packedmessage import *
from database import *
import listener, pinger, main, serveraction
import log, logging, sys

logInstance = log.logger('message')
mlogger = logging.getLogger('message')
log.logger.init(logInstance, mlogger)
mlogger.info('Message logger started')

def unicast(message_type, message, client):
   """
   Method to send a message to one specific client. 
   Client variable is a socket.
   """
   mlogger.info("Sending message to %s, message: (%d) %s" % (client.getaddress()[0], message_type, message))
   client.send(Packer(message_type, message).get())


def broadcast_all(message_type, message):
   """
   Method to send a message to all clients and servers.
   """
   mlogger.info("Broadcasting to all, message: (%d) %s" % (message_type, message))
   sockets = DB.get_by_type(CLIENT) + DB.get_by_type(CHILD_SERVER) + DB.get_by_type(PARENT_SERVER)
   for s in sockets:
      if s['socket']:
         s['socket'].send(Packer(message_type, message).get())
  
def broadcast_clients(message_type, message):
   """
   Method to send a message to all clients.
   """
   mlogger.info("Broadcasting to CLIENTS, message: (%d) %s" % (message_type, message))
   sockets = DB.get_by_type(CLIENT)
   for s in sockets:
      if s['socket']:
         s['socket'].send(Packer(message_type, message).get())
    
def broadcast_servers(message_type, message, except_server = 0):
   """
   Method to send a message to all servers.
   """
   mlogger.info("Broadcasting to SERVERS, message: (%d) %s" % (message_type, message))
   
   sockets = DB.get_by_type(CHILD_SERVER) + DB.get_by_type(PARENT_SERVER)
      
   for s in sockets:
      if not (except_server and except_server == s['socket']):
         #skip this server if it is to be excepted (ie: your message came from there)
         s['socket'].send(Packer(message_type, message).get())
   
def drop_client_by_socket(sock):
   """
   Removes one of your clients from the tree by socket.
   (If the connection closed unexpectedly, or if it doesn't respond to pings)
   """
   conn = DB.get_by_socket(sock)
   
   if not conn:
      return False
   #Relay that this client or server is dead
   if conn['type'] == CLIENT:
      broadcast_all(130, conn['name'] + " Socket closed unexpectedly")
   else:
      control = DB.get_by_type(CONTROL_SERVER)
      unicast(603, conn['name'], control[0]['socket'])
   #remove it from our own database
   DB.remove_by_socket(sock)
      

def handle_100(message, address, client):
   """
   Allows for registering clients
   """
   DB.update_last_action(client)
   
   msg = message.split()
   if (len(msg) < 1):
      mlogger.warning('Invalid message length %s', len(msg))
      return
   
   name = msg[0]
   
   # The admin password is 'koekje', if valid
   # the admin flag is set in the database
   password = False
   if(len(msg) == 2):
      if (msg[1] == "koekje"):
         password = True
         
   if (DB.get_by_name(name) != False):
      unicast(510, "Username already exists.", client)
   else:
      unicast(500,"", client)
      all_clients = DB.get_by_type(CLIENT)
      for c in all_clients:
         unicast(110, c['name'], client)
         
      DB.insert(address, client, name, CLIENT, None, password)
      broadcast_all(110, name)
      

def handle_110(message, address, client):
   """
   Allows for adding clients
   """
   msg = message.split()
   if (len(msg) != 1):
      mlogger.warning('Invalid message length %s', len(msg))
      return
   
   if(DB.get_by_socket(client)):
      clients = DB.get_by_type(CLIENT) + DB.get_by_type(PARENT_SERVER) + DB.get_by_type(CHILD_SERVER)
      
      for c in clients:
         if c['socket'] and (c['socket'] != client):
            unicast(110, message, c['socket'])
      DB.insert(address, None, message, CLIENT, client)
   else:
      DB.insert( address, client, message, CLIENT)

def handle_120(message, address, client):
   """
   Delete clients when they disconnect
   """
   msg = message.split()
   if (len(msg) < 1):
      mlogger.warning('Invalid message length %s', len(msg))
      return
   c = DB.get_by_socket(client)
   if DB.remove_by_socket(client):
      broadcast_all(130, c['name'] + ' ' + message)
   del(client)
   del(c)

def handle_130(message, address, client):
   """
   Handles client disconnect message
   """
   DB.update_last_action(client)
   
   msg = message.split()
   if (len(msg) < 1):
      mlogger.warning('Invalid message length %s', len(msg))
      return
   
   name = message.split()[0]
   if(DB.remove_by_name(name)):
      broadcast_all(130, message)

def handle_140(message, address, client):
   """
   Received a ping request, send a pong back.
   """
   DB.update_last_action(client)
   
   msg = message.split()
   if (len(msg) != 1):
      mlogger.warning('Invalid message length %s', len(msg))
      return
   
   unicast(150, message, client)
   
def handle_150(message, address, client):
   """
   You received a pong, good.
   """
   DB.update_last_action(client)

def handle_160(message, address, client):
   """
   Sends new client name
   """
   DB.update_last_action(client)
   
   msg = message.split()
   if (len(msg) != 1):
      mlogger.warning('Invalid message length %s', len(msg))
      return
   
   if(DB.get_by_name(message) == False):
      oldname = DB.get_by_socket(client)["name"]
      DB.update_name(oldname, message)
      unicast(520,"", client)
      new_message = oldname + ' ' + message;
      broadcast_all(170, new_message)
   else:
      unicast(530, "Name already exists.", client)

def handle_170(message, address, client):
   """
   Allows for nick renaming
   """
   DB.update_last_action(client)
   
   msg = message.split()
   if (len(msg) != 2):
      mlogger.warning('Invalid message length %s', len(msg))
      return
      
   names = message.split
   DB.update_name(names[0], names[1])

def handle_200(message, address, client):
   """
   Handles messages sent by clients
   """
   DB.update_last_action(client)
   
   msg = message.split()
   if (len(msg) < 2):
      mlogger.warning('Invalid message length %s', len(msg))
      return
   
   destination = message.split()[0]
   sender = DB.get_by_socket(client)["name"]
   
   """
   Decide who to send to, and then do so.
   """
   if(destination == "#all"): #message to all
      broadcast_all(300, sender + ' ' + message)
   elif(DB.get_by_name(destination) != False): 
      if not (DB.get_by_name(destination)["socket"]):
         #message to remote client
         sock = DB.get_by_name(destination)["parent_sock"]
      else: 
         #message to local client
         sock = DB.get_by_name(destination)["socket"]
      unicast(300, sender + ' ' + message, sock)
   
   else:
      message = sender +' '+ message
      broadcast_servers(300, message)

def handle_210(message, address, client):
   """
   Can be handled by handle_200
   """
   handle_200(message, address, client)


def handle_300(message, address, client):
   """
   Handles messages sent by servers or clients.
   Messages are either private or global
   """
   DB.update_last_action(client)
   
   msg = message.split()
   if (len(msg) < 3):
      mlogger.warning('Invalid message length %s', len(msg))
      return
   
   sender = msg[0]
   destination = msg[1]
   if(destination == '#all'):
      #send to all your clients and to your other connected servers
      broadcast_clients(300, message)
      broadcast_servers(300, message, client) #except client, that is where the message came from.
   else:
      #find out if this is a local or remote client, and send the message accordingly
      if not (DB.get_by_name(destination)["socket"]):
         sock = DB.get_by_name(destination)["parent_sock"]
      else:
         sock = DB.get_by_name(destination)["socket"]
      unicast(300, message, sock) 

def handle_310(message, address, client):
   """
   Can be handled by handle_300
   """
   handle_300(message, address, client)


def handle_600(message, address, client):
   """
   Another server applies to you to be your child server.
   """
   address,name,ip = message.split(':')
   DB.insert(ip[0], client, name, CHILD_SERVER)

def handle_602(message, addres, client):
   """
   You are assigned a parent server
   """
   DB.update_last_action(client)
   
   if message != 'none':
      #Only add a parent when you are actually given one.
      address = message.split(':')
      global sock
      sock = Connection(address[0], 2001)
      #sock = Connection(address[0], int(address[1]))
      my_ip = socket.gethostbyname(socket.gethostname())
      unicast(600, "%s:2001 :weeeeee" % my_ip, sock)
      
      #get the connection in a separate thread, so you can keep receiving data
      s = listener.Clientconn(sock)
      s.start()
      
      DB.insert(address[0], sock, address[2], PARENT_SERVER)

def handle_604(message, address, client):
   """
   Handles server disconnecting
   """
   DB.update_last_action(client)
   
   msg = message.split()
   if (len(msg) < 1 or len(msg) > 2):
      mlogger.warning('Invalid message length %s', len(msg))
      return
   
   words = message.split()
   
   removed = DB.get_by_name(words[0])
   if not removed:
      #You don't have this in your database, it's probably already removed: Do nothing.
      return
   
   if removed['type'] == CHILD_SERVER or removed['type'] == PARENT_SERVER:
      clients = DB.get_by_type(CLIENT)
      for c in clients:
         if c["parent_sock"] == removed["socket"]:
            DB.remove_by_socket(c["socket"])
   
   #remove disconnected node itself
   DB.remove_by_name(removed[0]['name'])
   
   if words[1]:
      handle_602(words[1], address, client)

def handle_700(message, address, client):
   """
   Allows admin to stop server
   """
   c = DB.get_by_socket(client)
   if (c["password"]):
      mlogger.info("stopping server")
      DB.do_exit()

   
   
