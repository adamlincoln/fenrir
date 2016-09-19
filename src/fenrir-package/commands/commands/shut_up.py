#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from core import debug

class command():
    def __init__(self):
        pass
    def initialize(self, environment):
        pass
    def shutdown(self, environment):
        pass
    def getDescription(self, environment):
        return 'interrupts the current presentation'        
    def run(self, environment):
        environment['runtime']['outputManager'].interruptOutput(environment)
    def setCallback(self, callback):
        pass
