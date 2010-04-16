from connection import *
from packedmessage import *

def unicast(message_type, message, client)
  client.send(Packer(message_type, message).get())

def broadcast_all(message_type, message):
  sockets = database.get_all_connected()
  for s in sockets
    s.send(Packer(message_type, message).get())
  
def broadcast_clients():
  sockets = database.get_all_clients()
  for s in sockets
    s.send(Packer(message_type, message).get())
    
def broadcast_servers():
  sockets = database.get_all_servers()
  for s in sockets
    s.send(Packer(message_type, message).get())



def handle_100(message, address, client):
  if database.name_exists(message)
    unicast(510, "username already exists", client)
  else
    unicast(500,"", client)
    database.add_client(message, adress, client)
    broadcast_all(110, message)
  
def handle_110(message, address, client):
  database.add_client(message, adress, client)

def handle_120(message, address, client):
  name = message.split()[0]
  database.remove_by_name(name)
  
  broadcast_all(130, message)

def handle_130(message, address, client):
  name = message.split()[0]
  if(database.remove_by_name(name))
    broadcast_all(130)

def handle_140(message, address, client):
  unicast(150, message, client);

def handle_150(message, address, client):
  database.received_pong(message)

def handle_160(message, address, client):
  if(!database.name_exists(message))
    oldname = database.get_client_name(client)
    database.change_name(oldname, message)
    unicast(520,"", client)
    new_message = oldname + message;
    broadcast_all(170, new_message)
  else
    unicast(530, "name already exists", client)

def handle_170(message, address, client):
  names = message.split
  database.change_name(names[0], names[1])

def handle_200(message, address, client):
  destination = message.split()[0]
  
  if(destination == "#all")
    broadcast_all(300, message)
    
  elif(datbase.is_local_client(destination))
    client = database.get_name_client(destination)
    unicast(300, message, client)
    
  else
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
  program.DIE!
