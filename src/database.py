import time, logging, log

class Database:
   
  def __init__(self):
    self.control_server = ("146.50.1.102", 2001)
    self.db = []
    self.logger = logging.getLogger('database')
    self.logger.info('DB init')
    
  def insert(self, address, socket, name, conn_type, parent_sock = None):
    self.db.append({"address":address, "socket":socket, "name":name,\
       "type":conn_type, "last_action": time.time(), "parent_sock": parent_sock})
    
    
  def get_by_name(self, name):
    for c in self.db:
      if c["name"] == name:
        return c
    return False
    
  def get_by_address(self, address):
    for c in self.db:
      if c["address"] == address:
        return c
    return False
    
  def get_by_socket(self, socket):
    for c in self.db:
      if c["socket"] == socket:
        return c
    return False
    
  def get_by_type(self,conn_type):
    ret = []
    for c in self.db:
      if c["type"] == conn_type:
        ret.append(c)
    return ret
        
  def update_name(self, oldname, newname):
    for c in self.db:
      if c["name"] == oldname:
        c["name"] = newname
        return True
    return False
    
  def update_last_action(self, socket):
    for c in self.db:
      if c["socket"] == socket:
        c["last_action"] = time.time()
        return True
    return False

  def get_all_connections(self):
    ret = []
    for c in self.db:
      if c["socket"]:
        ret.append(c)
    return ret
        
   
  def remove_by_name(self, name):
    for c in self.db:
      if c["name"] == name:
        self.db.remove(c)
        return True
    return False

  def remove_by_socket(self, sock):
    for c in self.db:
      if c["socket"] == sock:
        self.db.remove(c)
        return True
    return False
     
global DB

DB = Database()