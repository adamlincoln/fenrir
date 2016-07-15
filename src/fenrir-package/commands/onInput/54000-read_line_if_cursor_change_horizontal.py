#!/bin/python

class command():
    def __init__(self):
        pass
    def run(self, environment):
        if environment['screenData']['newCursor']['x'] == environment['screenData']['oldCursor']['x'] or\
          environment['screenData']['newCursor']['y'] != environment['screenData']['oldCursor']['y']:
            return environment
        if environment['screenData']['newContentText'].split('\n')[environment['screenData']['newCursor']['y']][environment['screenData']['newCursor']['x']].replace(" ","").replace("\n","").replace("\t","") == '':
            environment['runtime']['outputManager'].speakText(environment, "blank")
        else:
            environment['runtime']['outputManager'].speakText(environment, environment['screenData']['newContentText'].split('\n')[environment['screenData']['newCursor']['y']][environment['screenData']['newCursor']['x']])
        return environment    
    def setCallback(self, callback):
        pass
    def shutdown(self):
        pass
