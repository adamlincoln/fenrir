#!/usr/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.
# generic driver

from core import debug
from threading import Thread
from queue import Queue, Empty
#import subprocess, os
from subprocess import Popen, PIPE

class speakQueue(Queue):
    def clear(self):
        try:
            while True:
                self.get_nowait()
        except Empty:
            pass

class driver():
    def __init__(self):
        self.proc = None
        self.speechThread = Thread(target=self.worker)
        self.textQueue = speakQueue()
        self.volume = None
        self.rate = None
        self.pitch = None
        self.module = None
        self.language = None        
        self.voice = None
    def initialize(self, environment):   
        self.env = environment  
        self.minVolume = self.env['runtime']['settingsManager'].getSettingAsInt('speech', 'fenrirMinVolume')
        self.maxVolume = self.env['runtime']['settingsManager'].getSettingAsInt('speech', 'fenrirMaxVolume')        
        self.minPitch = self.env['runtime']['settingsManager'].getSettingAsInt('speech', 'fenrirMinPitch')        
        self.maxPitch = self.env['runtime']['settingsManager'].getSettingAsInt('speech', 'fenrirMaxPitch')
        self.minRate = self.env['runtime']['settingsManager'].getSettingAsInt('speech', 'fenrirMinRate')
        self.maxRate = self.env['runtime']['settingsManager'].getSettingAsInt('speech', 'fenrirMaxRate')
        
        self.speechCommand = self.env['runtime']['settingsManager'].getSetting('speech', 'genericSpeechCommand')
        if self.speechCommand == '':
            self.speechCommand = 'espeak -a fenrirVolume -s fenrirRate -p fenrirPitch -v fenrirVoice "fenrirText"'
        if False: #for debugging overwrite here
            self.speechCommand = 'spd-say --wait "fenrirText"'  
        
        self._isInitialized = True   
        if self._isInitialized:
            self.speechThread.start()   
    def shutdown(self):
        if not self._isInitialized:
            return
        self.cancel()    
        self.textQueue.put(-1)

    def speak(self,text, queueable=True):
        if not self._isInitialized:
            return
        if not queueable: 
            self.cancel()        
        utterance = {
          'text': text,
          'volume': self.volume,
          'rate': self.rate,
          'pitch': self.pitch,
          'module': self.module,
          'language': self.language,
          'voice': self.voice,
        }        
        self.textQueue.put(utterance.copy())

    def cancel(self):
        if not self._isInitialized:
            return
        self.clear_buffer()
        if self.proc:
            self.proc.kill()
        
    def setCallback(self, callback):
        print('SpeechDummyDriver: setCallback')    

    def clear_buffer(self):
        if not self._isInitialized:
            return
        if not self.textQueue.not_empty:
            self.textQueue.clear()     
    def setVoice(self, voice):
        if not self._isInitialized:
            return
        self.voice = str(voice)

    def setPitch(self, pitch):
        if not self._isInitialized:
            return
        self.pitch = self.minPitch + pitch * (self.maxPitch - self.minPitch )

    def setRate(self, rate):
        if not self._isInitialized:
            return
        self.rate = self.minRate + rate * (self.maxRate - self.minRate )

    def setModule(self, module):
        if not self._isInitialized:
            return 
        self.module = str(module)

    def setLanguage(self, language):
        if not self._isInitialized:
            return
        self.language = str(language)

    def setVolume(self, volume):
        if not self._isInitialized:
            return     
        self.volume = self.minVolume + volume * (self.maxVolume - self.minVolume )
    
    def worker(self):
        while True:
            utterance = self.textQueue.get()
            if isinstance(utterance, int):
                if utterance == -1:
                    return
            elif not isinstance(utterance, dict):
                continue

            for key in ['volume','module','language','voice','pitch','rate','text']:
                if not key in utterance:
                    utterance[key] = ''
                if not utterance[key]:
                    utterance[key] = ''
            print(utterance)                    
            popenSpeechCommand = self.speechCommand
            popenSpeechCommand = popenSpeechCommand.replace('fenrirVolume', str(utterance['volume'] ).replace('"',''))
            popenSpeechCommand = popenSpeechCommand.replace('fenrirModule', str(utterance['module']).replace('"',''))
            popenSpeechCommand = popenSpeechCommand.replace('fenrirLanguage', str(utterance['language']).replace('"','')) 
            popenSpeechCommand = popenSpeechCommand.replace('fenrirVoice', str(utterance['voice']).replace('"',''))
            popenSpeechCommand = popenSpeechCommand.replace('fenrirPitch', str(utterance['pitch']).replace('"',''))               
            popenSpeechCommand = popenSpeechCommand.replace('fenrirRate', str(utterance['rate']).replace('"',''))               
            popenSpeechCommand = popenSpeechCommand.replace('fenrirText', str(utterance['text']).replace('"','').replace('\n',''))
                  
            try:
                self.proc = Popen(popenSpeechCommand , stdout=PIPE, stderr=PIPE, shell=True)
                stdout, stderr = self.proc.communicate()
                screenEncoding = self.env['runtime']['settingsManager'].getSetting('screen', 'encoding')
                stderr = stderr.decode(screenEncoding, "replace").encode('utf-8').decode('utf-8')
                stdout = stdout.decode(screenEncoding, "replace").encode('utf-8').decode('utf-8')
                if stderr != '':
                    print('err' + stderr)
                if stdout != '':
                    print('out' + stdout)
            except Exception as e:
                    print('except' + str(e))
