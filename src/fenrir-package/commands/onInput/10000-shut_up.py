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
        return ''               
    
    def run(self, environment):
        if not environment['runtime']['settingsManager'].getSettingAsBool(environment, 'keyboard', 'interruptOnKeyPress'):
            return 
        if environment['runtime']['inputManager'].noKeyPressed(environment):
            return
        if environment['screenData']['newTTY'] != environment['screenData']['oldTTY']:
            return               

        environment['runtime']['outputManager'].interruptOutput(environment)

    def setCallback(self, callback):
        pass
