# Copyright (C) 2018 Fassio Blatter

import stopeight.legacy
from stopeight.util.editor.data import ScribbleData
from PyQt5.QtWidgets import QFileDialog
from stopeight.util.runnable import EditorApp

import stopeight.logging as log

def stroke_parallel(data:ScribbleData)->ScribbleData:
    return _convert(stopeight.legacy.stroke_parallel(list(map(tuple,data['coords'].tolist()))))

def stroke_sequential(data:ScribbleData)->ScribbleData:
    # type: (ScribbleData) -> ScribbleData
    return _convert(stopeight.legacy.stroke_sequential(list(map(tuple,data['coords'].tolist()))))

def _parse_file(filename):
    legacy_data= stopeight.legacy.parse_file(filename)
    return _convert(legacy_data)

def _convert(legacy_data):
    scribbledata = ScribbleData(size=len(legacy_data))
    for i,v in enumerate(legacy_data):
        scribbledata[i]['coords'] = [v[0],v[1]]
    return scribbledata

def open_SP()->ScribbleData:
    filename = QFileDialog.getOpenFileName(EditorApp().window)
    data = _parse_file(filename[0])
    return data

def TCT_to_bezier(data:ScribbleData)->ScribbleData:
    return stopeight.legacy.TCT_to_bezier(data)

##import stopeight.finders
##from stopeight.grapher import *
##
##def findTurns(data):
##    log.info("Invoking findTurns...")
##    ql = stopeight.getters.QListDpoint(data)
##    turns = stopeight.finders.Turns(ql)
##    print(turns)
##    assert type(turns) == list
##    return turns
##findTurns.__annotations__ = {'data': ScribbleData, 'return': list}
##
##def sequencial(data):
##    log.info("Invoking findCliffs...")
##    ql = stopeight.getters.QListDpoint(data)
##    turns = stopeight.finders.Cliffs(ql)
##    print(turns)
##    assert type(turns) == list
##    return turns
##sequencial.__annotations__ = {'data': ScribbleData, 'return': list}
##
##def parallel(data):
##    log.info("Invoking findSpiralCliffs...")
##    ql = stopeight.getters.QListDpoint(data)
##    turns = stopeight.finders.Spirals(ql)
##    print(turns)
##    assert type(turns) == list
##    return turns
##parallel.__annotations__ = {'data': ScribbleData, 'return': list}
##
##
import stopeight.getters
import numpy as np

def getFirstTurnByTriplets(data:ScribbleData)->ScribbleData:
    log.info("Invoking getFirstTurnByTriplets...")
    ql = stopeight.getters.QListDpoint(data)
    ta = stopeight.getters.Turn(ql)
    turn = np.array(ta.next())
    assert type(turn) == np.ndarray
    return turn.view(ScribbleData)
