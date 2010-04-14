"""
Module for logging all the messages from the server modules.
Each module logs to it's own file.

Usage:
in module <name>:
    import logging, log

    logger = logging.getLogger('name')
    logger.info('This is example info') 

Author  : Ravish
Date    : 11-4-2010
Version : 1.0
"""

import logging, logging.handlers

class logger:
    
    # Set up logging variables
    logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)2s %(module)-12s %(levelname)-4s %(message)s',
                    datefmt='%d-%m %H:%M')
    datefmt = '%d-%m %H:%M'
    format = logging.Formatter('%(asctime)2s %(module)-2s %(levelname)-4s %(message)s', datefmt)
    
    # Server action log
    sLogger = logging.getLogger('serveraction')
    sFile = logging.FileHandler('../log/serveraction.log')
    sFile.setFormatter(format)
    sLogger.addHandler(sFile)
    
    # Connection log
    cLogger = logging.getLogger('connection')
    cFile = logging.FileHandler('../log/connection.log')
    cFile.setFormatter(format)
    cLogger.addHandler(cFile)
    
    # Actions log
    aLogger = logging.getLogger('action')
    aFile = logging.FileHandler('../log/action.log')
    aFile.setFormatter(format)
    aLogger.addHandler(aFile)
    
    # Listener log
    lLogger = logging.getLogger('listener')
    lFile = logging.FileHandler('../log/listener.log')
    lFile.setFormatter(format)
    aLogger.addHandler(lFile)
    
if __name__ == '__main__':
    logging.info('This is info')

