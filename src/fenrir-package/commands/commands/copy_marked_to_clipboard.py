#!/bin/python
try:
    from utils import mark_utils
except Exception as e:
    print(e)
class command():
    def __init__(self):
        pass
    def run(self, environment):

        if (environment['commandBuffer']['Marks']['1'] == None) or \
          (environment['commandBuffer']['Marks']['2'] == None):
            environment['runtime']['outputManager'].presentText(environment, "two marks needed", interrupt=True)
            return environment

        # use the last first and the last setted mark as range
        startMark = environment['commandBuffer']['Marks']['1'].copy()
        endMark = environment['commandBuffer']['Marks']['2'].copy() 
        if environment['commandBuffer']['Marks']['3'] != None:
            endMark = environment['commandBuffer']['Marks']['3'].copy()    

        marked = mark_utils.getTextBetweenMarks(startMark, endMark, environment['screenData']['newContentText'])

        environment['commandBuffer']['clipboard'] = [marked] + environment['commandBuffer']['clipboard'][:environment['runtime']['settingsManager'].getSettingAsFloat(environment, 'general', 'numberOfClipboards') -1]
        environment['commandBuffer']['currClipboard'] = 0
        environment['commandBuffer']['Marks']['1'] = None
        environment['commandBuffer']['Marks']['2'] = None
        environment['commandBuffer']['Marks']['3'] = None
        
        if marked.strip() == '':
            environment['runtime']['outputManager'].presentText(environment, "blank", soundIcon='EmptyLine', interrupt=True)
        else:
            environment['runtime']['outputManager'].presentText(environment, marked, interrupt=True)
        return environment    
    def setCallback(self, callback):
        pass
    def shutdown(self):
        pass