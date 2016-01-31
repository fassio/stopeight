# Copyright (C) 2009-2012 Specific Purpose Software GmbH

from operator import itemgetter
from numpy import ndarray,sqrt,square,zeros_like,pi
from numpy.core.umath import arctan2, arctan2
#from SVG import Line
from stopeight.comparator.matrixTools import *

class NumpyLine(ndarray):

    def reorderToNStart(self,n):
        reordered = zeros_like(self)
        for count in range(len(self)):
            if ((count+n)<len(self)):
                reordered[count]=self[count+n]
            else:
                reordered[count]=self[count-len(self)+n]
        return reordered

    def reverse(self):
        reversed = zeros_like(self)
        for pos,p in enumerate(self):
            reversed[len(self)-pos-1]=p
        return reversed

    def getAverageLength(self):
        sumDbLength = 0
        for dbCount,dbPoint in enumerate(self):
            if dbCount<len(self)-1:
                currPoint = dbCount+1
            elif dbCount==len(self)-1:
                currPoint = 0
            length = getVectorLength(self[currPoint]-dbPoint)
            sumDbLength += length
        avgDbLength = sumDbLength / len(self)
        return avgDbLength

    def moveToZero(self):
        movement = idmatrix()
        movement = dot(translate(-self[0]),movement)
        vAtZero = zeros_like(self)
        for pos,moveme in enumerate(self):
            vAtZero[pos] = transform(moveme,movement)
        return vAtZero

    def getAngleToNegativeXAxis(self):
        rad = arctan2( self[1], self[0]);
        deg = (rad/pi)*180.0 + 180.0;
        return deg

#    def printVectors(self,filename):
#        scene = Scene(filename,255,255)
#        for count,v in enumerate(self[:len(self)-1]):
#            scene.add(Line(center(v),center(self[count+1])))
#        scene.write_svg()
#        scene.display()

    def to_tuple(self):
        line = [(float(L[0]),float(L[1])) for L in self]
        return line

def getDistance(point1,point2):
    return getVectorLength([point1[0]-point2[0],point1[1]-point2[1]])

def getVectorLength(vector):
    return sqrt(square(vector[0]) + square(vector[1]))
