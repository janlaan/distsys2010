from connection import *
from packedmessage import *
from database import *


def unicast(message_type, message, client):
   """
   Method to send a message to one specific client. 
   Client variable is a socket.
   """
   client.send(Packer(message_type, message).get())


def broadcast_all(message_type, message):
   """
   Method to send a message to all clients and servers.
   """
   #sockets = DB.get_all_connections()
   sockets = DB.get_by_type(CLIENT)
   for s in sockets:
      print s
      s['socket'].send(Packer(message_type, message).get())
  
def broadcast_clients(message_type, message):
   """
   Method to send a message to all clients.
   """
   sockets = DB.get_by_type(CLIENT)
   for s in sockets:
      s['socket'].send(Packer(message_type, message).get())
    
def broadcast_servers(message_type, message):
   """
   Method to send a message to all servers.
   """
   sockets = DB.get_by_type(CHILD_SERVER) + DB.get_by_type(PARENT_SERVER)
   for s in sockets:
      s['socket'].send(Packer(message_type, message).get())
   


def handle_100(message, address, client):
   if (DB.get_by_name(message) != False):
      unicast(510, "Username already exists.", client)
   else:
      unicast(500,"", client)
      all_clients = DB.get_by_type(CLIENT)
      for c in all_clients:
         unicast(110, c['name'], client)
         
      DB.insert( address, client, message, CLIENT)
      broadcast_all(110, message)
      

def handle_110(message, address, client):
   DB.insert( address, client, message, CLIENT)

def handle_120(message, address, client):
   name = message.split()[0]
   if DB.remove_by_name(name):
      broadcast_all(130, message)

def handle_130(message, address, client):
   name = message.split()[0]
   if(DB.remove_by_name(name)):
      broadcast_all(130)

def handle_140(message, address, client):
   print DB.get_all_connections()
   unicast(150, message, client)

def handle_150(message, address, client):
   DB.received_pong(message)

def handle_160(message, address, client):
   if(DB.get_by_name(message) == False):
      oldname = DB.get_by_socket(client)["name"]
      DB.update_name(oldname, message)
      unicast(520,"", client)
      new_message = oldname + ' ' + message;
      broadcast_all(170, new_message)
   else:
      unicast(530, "Name already exists.", client)

def handle_170(message, address, client):
   names = message.split
   DB.update_name(names[0], names[1])

def handle_200(message, address, client):
   destination = message.split()[0]
   
   if(destination == "#all"):
      sender = DB.get_by_socket(client)
      broadcast_all(300, sender['name'] + ' ' + message)
   elif(DB.get_by_name(destination) != False):
      #client = database.get_name_client(destination)
      sock = DB.get_by_name(destination)["socket"]
      sender = DB.get_by_socket(client)
      unicast(300, sender['name'] + ' ' + message, sock)
   
   else:
      sender = DB.get_by_socket(client)
      message = sender['name'] +' '+ message
      broadcast_servers(300, message)

def handle_210(message, address, client):
   pass

def handle_300(message, address, client):
   #do stuff
   pass

def handle_310(message, address, client):
   handle_300(message, address, client)


def handle_500(message, address, client):
   #server -> client only
   pass

def handle_510(message, address, client):
   #server -> client only
   pass

def handle_520(message, address, client):
   #to client only
   pass

def handle_530(message, address, client):
   #from server to client only
   pass

def handle_600(message, address, client):
   """
   Another server applies to you to be your child server.
   """
   address,name = message.split()
   ip = address.split(':')
   DB.insert(ip[0], client, name, CHILD_SERVER)
  

def handle_601(message, address, client):
   #you don't recieve 601's
   pass

def handle_602(message, addres, client):
   """
   You are assigned a parent server
   """
   
   if message != 'none':
      #Only add a parent when you are actually given one.
      address = message.split(':')
      global sock
      sock = Connection('146.50.7.85', 2001)
      #sock = Connection(address[0], int(address[1]))
      
      unicast(600, '146.50.7.85:2001 :weeeeee', sock)
      DB.insert(address[0], sock, address[2], PARENT_SERVER)
   

def handle_603(message, address, client):
   #You don't recieve 603's
   pass

def handle_604(message, address, client):
   words = message.split()
   
   removed = DB.get_by_type(PARENT_SERVER)[0]
   
   if removed['type'] == CHILD_SERVER or removed['type'] == PARENT_SERVER:
      #TODO: remove all clients if this is a server
      pass
   
   #remove disconnected node itself
   DB.remove_by_name(removed[0]['name'])
   
   if words[1]:
      handle_602(words[1], address, client)

def handle_610(message, address, client):
   #sent from client to control server
   pass

def handle_611(message, address, client):
   #Sent from control server to client
   pass

def handle_700(message, address, client):
   pass
   #program.DIE!
