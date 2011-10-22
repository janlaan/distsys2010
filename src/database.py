import time, logging, log

class Database:
   
  def __init__(self):
    self.control_server = ("146.50.1.102", 2001)
    self.db = []
    self.logger = logging.getLogger('database')
    self.logger.info('DB init')
    self.sys_exit = False
    
  def insert(self, address, socket, name, \
             conn_type, parent_sock = None, admin = False):
    """
    Add new client/server to the database
    """
    self.db.append({"address":address, "socket":socket, "name":name,\
       "type":conn_type, "last_action": time.time(), "parent_sock": parent_sock,\
       "password": admin})
       
  def do_exit(self):
    """
    Set the systems exit status to true
    Warning: This will shut down the server.
    """
    self.sys_exit = True
    
  def get_exit(self):
    """
    Retreive the server exit status.
    This determines whether the server should be shut down or not.
    """
    return self.sys_exit
    
  def get_by_name(self, name):
    """
    Retreive a clients details based on its name
    """
    for c in self.db:
      if c["name"] == name:
        return c
    return False
    
  def get_by_address(self, address):
    """
    Retrieve a cliets details based on its address (not used)
    """
    for c in self.db:
      if c["address"] == address:
        return c
    return False
    
  def get_by_socket(self, socket):
    """
    Retreive a clients details based on its socket
    """
    for c in self.db:
      if c["socket"] == socket:
        return c
    return False
    
  def get_by_type(self,conn_type):
    """
    Retreive all servers of a certain type (CLIENT, CHILD_SERVER, etc.)
    """
    ret = []
    for c in self.db:
      if c["type"] == conn_type:
        ret.append(c)
    return ret
        
  def update_name(self, oldname, newname):
    """
    Update the name of a client
    """
    for c in self.db:
      if c["name"] == oldname:
        c["name"] = newname
        return True
    return False
    
  def update_last_action(self, socket):
    """
    Update the last active time of a client.
    Used to determine whether we need to ping it or not.
    """
    for c in self.db:
      if c["socket"] == socket:
        c["last_action"] = time.time()
        return True
    return False

  def get_all_connections(self):
    """
    Retreive all connections
    """
    ret = []
    for c in self.db:
      if c["socket"]:
        ret.append(c)
    return ret
        
   
  def remove_by_name(self, name):
    """
    Remove a clients based on its name
    """
    for c in self.db:
      if c["name"] == name:
        self.db.remove(c)
        return True
    return False

  def remove_by_socket(self, sock):
    """
    Remove a client based on its socket
    """
    for c in self.db:
      if c["socket"] == sock:
        self.db.remove(c)
        return True
    return False
     
#start the database
global DB
DB = Database()