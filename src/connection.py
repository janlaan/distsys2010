"""
Connection interface. Use the classes in this module to create a connection.
"""
import socket

#Control server address
CONTROL_SERVER = ('146.50.1.74', 2001)
CLIENT = 1
PARENT_SERVER = 2
CHILD_SERVER = 3

class Connection:
    """
    Connects to a certain host/port.
    """

    def __init__(self, host, port=None):
        """
        Initialize the connection with another host.
        """
        if port == None:
            self.sock = host
        else:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((host, port))
        
    def send(self, msg):
        """
        Send a message through your connection.
        """
        self.sock.send(msg)
        
    def receive(self, size=4096):
        """
        Try to receive a message from the host.
        
        Calling this function will block unless you have set a timeout with
        settimeout().  Returns the received data as string, if any.
        """
        return self.sock.recv(size)
    
    def getaddress(self):
        """
        Retrieve the address of the client you are connected to.
        """

        return self.sock.getpeername()

    def settimeout(self, secs=0):
        """
        Set a timeout for this connection.

        If you try to receive data with receive(), it will timeout and generate
        an exception after the specified time.
        """
        self.sock.settimeout(secs)
        
    def close(self):
        """
        Close the connection explicitly.
        """
        self.sock.close()
        
    def __del__(self):
        """
        On destruction, close the connection.
        """
        self.sock.close()

class Listen:
    """
    Creates a listening connection on the current host to serve as a server.
    """

    def __init__(self, port, max=5):
        """
        Initialize a listen connection, listen on a cpecified host, and accept
        a specified maximum of simultaneous connections.
        """
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((socket.gethostname(), port))
        self.sock.listen(max)
        
    def accept(self):
        """
        Accept an incoming connection.
        
        This function will block.  It returns a list with a new socket and the
        address of the requesting host.
        """
        return self.sock.accept()
    
    def __del__(self):
        """
        On destruction, close the connection.
        """
        self.sock.close()
