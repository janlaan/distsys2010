from connection import *
from packedmessage import *
import database


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
   sockets = DB.get_all_connected()
   for s in sockets:
      s.send(Packer(message_type, message).get())
  
def broadcast_clients():
      """
      Method to send a message to all clients.
      """
   sockets = DB.get_all_clients()
   for s in sockets:
      s.send(Packer(message_type, message).get())
    
def broadcast_servers():
      """
      Method to send a message to all servers.
      """
   sockets = DB.get_all_servers()
   for s in sockets:
      s.send(Packer(message_type, message).get())
   


def handle_100(message, address, client):
   if (DB.get_by_name(message) != false):
      unicast(510, "Username already exists.", client)
   else:
      unicast(500,"", client)
      DB.insert( adress, client, message, CLIENT)
      broadcast_all(110, message)

def handle_110(message, address, client):
   DB.insert( adress, client, message, CLIENT)

def handle_120(message, address, client):
   name = message.split()[0]
   if DB.remove_by_name(name):
      broadcast_all(130, message)

def handle_130(message, address, client):
   name = message.split()[0]
   if(DB.remove_by_name(name)):
      broadcast_all(130)

def handle_140(message, address, client):
   unicast(150, message, client)

def handle_150(message, address, client):
   DB.received_pong(message)

def handle_160(message, address, client):
   if(DB.get_by_name(message) == false):
      oldname = database.get_by_socket(client)["name"]
      DB.change_name(oldname, message)
      unicast(520,"", client)
      new_message = oldname + message;
      broadcast_all(170, new_message)
   else:
      unicast(530, "Name already exists.", client)

def handle_170(message, address, client):
   names = message.split
   DB.update_name(names[0], names[1])

def handle_200(message, address, client):
   destination = message.split()[0]
   
   if(destination == "#all"):
      broadcast_all(300, message)
      
   elif(DB.get_by_adress(destination)["socket"] != None):
      #client = database.get_name_client(destination)
      unicast(300, message, DB.get_by_adress(destination)["socket"])
      
   else:
      message = adress +' '+ message
      broadcast_servers(300, message)

def handle_210(message, address, client):
   pass

def handle_300(message, address, client):
   pass

def handle_310(message, address, client):
   pass


def handle_500(message, address, client):
   pass

def handle_510(message, address, client):
   pass

def handle_520(message, address, client):
   pass

def handle_530(message, address, client):
   pass

def handle_600(message, address, client):
   database.add_server(message)

def handle_601(message, address, client):
   pass

def handle_602(message, addres, client):
   database.set_parent(message)

def handle_603(message, address, client):
   pass

def handle_604(message, address, client):
   pass

def handle_610(message, address, client):
   pass

def handle_611(message, address, client):
   pass

def handle_700(message, address, client):
   pass
   #program.DIE!
