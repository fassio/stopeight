#!/usr/bin/env python

# Copyright (C) 2017 Fassio Blatter

from stopeight.util import runnable

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QComboBox,QApplication,QMainWindow,QToolBar,QPushButton,QGroupBox,QHBoxLayout
from stopeight.util.scribble_area import ScribbleArea
from PyQt5.QtCore import Qt

from stopeight.logging import logSwitch
log = logSwitch.logPrint()
_LOGDIR = '.stopeight' # this is not for logging messages; it is for data files

import types
# false if part of stopeight-clibs
_DATA = {'Modules': [('stopeight.legacy', False),
#                            ('stopeight.comparator.matrixTools',True),
                            ('stopeight.util.file', True),
                             ('stopeight.util.file_wave',True),
                            ('stopeight.analyzer', False),
                            ('stopeight.grapher', False)
                    ]
         }

import importlib
for module in _DATA['Modules']:
    try:
        importlib.import_module(module[0])
        #output class name
        log.info("Successfully imported module "+module[0])
    except:
        log.info("Removing module "+module[0]+"!")
        _DATA['Modules'].remove(module)

class MyScribble(ScribbleArea):
    def __init__(self, parent = None):
        super(MyScribble, self).__init__(parent)

from sys import modules as loader

class Algorithm_Select(QComboBox):
    def __init__(self, module, **kwargs):
        super(Algorithm_Select,self).__init__(**kwargs)
        self.module = module
        
        module_name = module[0]
        for key in dir(loader[module_name]):
            if not key.startswith('_'):
                if isinstance(loader[module_name].__dict__[key],types.BuiltinFunctionType) or \
                isinstance(loader[module_name].__dict__[key],types.FunctionType):
                    self.addItem(loader[module_name].__dict__[key].__name__)
#        self.addItem(module_name)

from stopeight.util.editor_data import ScribbleData, ScribbleBackup
class Algorithm_Run(QPushButton):
    def __init__(self, module, **kwargs):
        super(Algorithm_Run,self).__init__(**kwargs)
        self.setText("Run")
        self.module = module

    @staticmethod
    def _auto_out(module_name,package_type,function_name):
        top = module_name+'.'+function_name
        import os
        from subprocess import check_output
        sub = 'HEAD'
        if (package_type==True):
            #get head from current directory (os.getcwd()).endswith('stopeight')
            try:
                sub = check_output(['git','rev-parse','--short','HEAD']).decode('utf-8').rstrip()
            except:
                sub = check_output(['git','rev-parse','--short','HEAD']).rstrip()
        else:
            #get head from stopeight-clibs
            try:
                sub = check_output(['git','rev-parse','--short','HEAD'],cwd=os.path.join('stopeight-clibs')).decode('utf-8').rstrip()
            except:
                sub = check_output(['git','rev-parse','--short','HEAD'],cwd=os.path.join('stopeight-clibs')).rstrip()
        top = os.path.join(top,sub)
        return top
    
    def _identify(self,scribblearea):
        import os
            
        #if (os.getcwd()).endswith('stopeight'):
        #    if (self.select.module_name=='stopeight.util.file'):
        if hasattr(scribblearea,'tablet_id'):
            sub = str(scribblearea.tablet_id)
        else:
            sub = 'MouseData'
        return sub

    def run(self,currentText):
        #inspect.signature()[return]
        #if (len(self.select.module[2].OUTPUT)>0):
        #    self.select.module[2].INPUT = self.select.module[2].OUTPUT
        #    self.select.module[2].OUTPUT= []
        #currentText = self.select.currentText()
        import time
        time = time.time()
        data = ScribbleData()
        backup = ScribbleBackup()#get singleton
        backup = data[:]#assign copy
        try:
            log.debug("Invoking "+currentText+" with "+str(len(ScribbleData()))+" Points...")
            data = loader[self.module[0]].__dict__[currentText](ScribbleData())
            #if backup == data:
            #    raise Exception("Backup not successful or function values unchanged")
        #except:
        except BaseException as e:
            log.error("Error during method invokation: "+self.module[0]+'.'+currentText)
            
            from stopeight.util import file
            from os.path import expanduser,join
            file._write(backup,time,outdir=join(expanduser("~"),_LOGDIR
                                                ,self._auto_out(self.module[0],self.module[1],currentText)
                                                #,self._identify(_DATA['MyScribble'])
                                                ))
            del data[:]
            if (len(data)>0):
                raise Exception("Data clear failed!")
            log.error(e)
        log.info("Size after call: Input "+str(len(backup))+", Output "+str(len(ScribbleData())))

class Connector:
    def __init__(self,data,select,button,scribble):
        self.data = data
        self.select = select
        self.button = button
        self.scribble = scribble
        self.button.clicked.connect(self.run)
        self.colors = [Qt.blue, Qt.red]

    def run(self):
        log.debug(self.select.currentText())
        self.button.run(self.select.currentText())
        self.scribble.clearImage()
        #for d,c in self.data,self.colors:
            #self.scribble.plot(d,c)
        self.scribble.plot(ScribbleBackup(),self.colors[0])
        self.scribble.plot(ScribbleData(),self.colors[1])

if __name__ == '__main__':
    #from stopeight.util.editor_data import ScribbleData, ScribbleBackup

    import sys
    app = QApplication(sys.argv)
    window = QMainWindow()
    window.setWindowTitle("Editor")

    #list or dict?
    connections = []


    from stopeight.util.wave_area import WaveArea
    wave = WaveArea()

    wbar = QToolBar()
    wgroup = QGroupBox()
    wbox = QtWidgets.QVBoxLayout()
    # Just some button connected to `plot` method
    plotbutton = QtWidgets.QPushButton('Plot')
    from stopeight.util import file_wave
    #wave.data = file_wave._open()
    #plotbutton.clicked.connect(wave.plot)
    # set the layout
    wbox.addWidget(wave.plotbar)
    wbox.addWidget(plotbutton)
    wgroup.setLayout(wbox)
    wbar.addWidget(wgroup)
    window.addToolBar(wbar)

    window.setCentralWidget(wave.canvas)
    #window.addDockWidget(Qt.TopDockWidgetArea,wave)    

    # Find modules
    scribbles = []
    from funcsigs import signature
    for module in _DATA['Modules']:
        #def zoo(a: str)->int:
        #if (signature(zoo).return_annotation!=Signature.empty):
        #if (signature(zoo).return_annotation==ScribbleData):
        scribbles.append(module)

    # Create results area
    scribble = MyScribble()
    window.addDockWidget(Qt.BottomDockWidgetArea,scribble)

    # Hook up modules
    toolbox = QToolBar()
    #toolbox = QtWidgets.QDockWidget()
    for module in scribbles:
        connections.append(Connector([ScribbleBackup(),ScribbleData()],Algorithm_Select(module),Algorithm_Run(module),scribble))
    for connection in connections:
        group = QGroupBox()
        box = QHBoxLayout()
        box.addWidget(connection.select)
        box.addWidget(connection.button)
        group.setLayout(box)
        toolbox.addWidget(group)
    window.addToolBar(Qt.BottomToolBarArea,toolbox)
    #window.addDockWidget(Qt.BottomDockWidgetArea,toolbox)
    
    window.show()
    sys.exit(app.exec_())
