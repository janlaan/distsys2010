"""
Module for logging all the messages from the server modules.
Each module logs to it's own file.

Usage:
in module <name>:
   import logging, log

   logInstance = log.logger('name')
   logger = logging.getLogger('name')
   log.logger.init(logInstance, logger)
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

   def __init__(self, name):
      self.name = name

   def init(self, Logger):
      File = logging.FileHandler('../log/' + self.name + '.log')
      File.setLevel(logging.DEBUG)
      File.setFormatter(self.format)
      Logger.addHandler(File)

if __name__ == '__main__':
   logging.info('This is info')
