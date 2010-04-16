import time

class Database:
  
  def __init__(self):
    self.control_server = ("146.50.1.102", 2001)
    self.db = []
    
  def insert(self, address, socket, name, conn_type):
    self.db.add({"address":adress, "socket":socket, "name":name, "type":conn_type, "last_action": time.time()})
    
    
  def get_by_name(self, name):
    for c in self.db:
      if c["name"] == name:
        return c
    return false
    
  def get_by_address(self, address):
    for c in self.db:
      if c["address"] == address:
        return c
    return false
    
  def get_by_type(self,conn_type):
    for c in self.db:
      if c["type"] == conn_type:
        yield c
        
  def update_name(self, oldname, newname):
    for c in self.db:
      if c["name"] == oldname:
        c["name"] = newname
        return true
    return false
    
  def update_last_action(self, socket):
    for c in self.db:
      if c["socket"] == socket:
        c["last_action"] = time.time()
        return true
    return false

  def get_all_connections(self):
    for c in self.db:
      if c["socket"]:
        yield c
        


DB = Database()