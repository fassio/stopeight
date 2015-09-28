# matchline: Comparing sequences of points in 2 dimensions.
# Copyright (C) 2009-2012 Specific Purpose Software GmbH
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; NO OTHER VERSION than version 2.0 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

from ZSI import TC
from vectorTools import *
import numpy

class ABCPoint():
    #******** Never add additional parameters to __init__(self) because it will break ZSI!
    def __init__(self):
        pass
#ABCPoint.typecode = TC.Struct(ABCPoint,[TC.InonNegativeInteger('x'),TC.InonNegativeInteger('y')],pname='item',aname='ABCPoint')
ABCPoint.typecode = TC.Struct(ABCPoint,[TC.Iint('x'),TC.Iint('y')],pname='item',aname='ABCPoint')

#class ABCLine(numpy.ndarray):
#    def __new__(cls,obj):
#        array.__init__([[]],'f') # If you want floating point
#        return numpy.array(obj).view(cls)
class ABCLine():
    #******** Never add additional parameters to __init__(self) because it will break ZSI!
    def __init__(self):
        self.points=[]
        pass
    def add_point(self,p):
        self.points.append(p)
    def __getitem__(self,number):
        return self.points[number]
    @staticmethod
    def from_numpy_array(mynumpyarray):
        line = ABCLine()
        for vector in mynumpyarray:
            point = ABCPoint()
            point.x=vector[0]
            point.y=vector[1]
            line.add_point(point)
        return line
    # This method is also being used by DBLine!
    def to_numpy_array(self):
        # we are using int in ZSI and float internally.
        # if switching to int internally, make sure to leave enough space for rotations beyond range of input: i.e. Input <256, space <4096?
        #line = numpy.array([(p.x,p.y) for p in self.points],dtype=numpy.dtype('u2'))
        line = numpy.array([(p.x,p.y) for p in self.points],dtype=numpy.dtype('f8'))
        return line
    def to_tuple(self):
        line = [(float(p.x),float(p.y)) for p in self.points]
        return line

ABCLine.typecode = TC.Struct(ABCLine,
                                [TC.Iint('id'),
                                TC.Array('Array',ABCPoint.typecode,'points',undeclared=True)], # Specifies xsd:type in Array
                                pname='item',
                                aname='ABCLine')

# if you want to use the above class from within zsiServer, you have to use an inventive name like the one below
#class TheSameBloodyShitClassWithADifferentName(ABCLine):
#    pass

class ABCSymbol():
    #******** Never add additional parameters to __init__(self) because it will break ZSI!
    def __init__(self):
        self.lines=[]
        pass
    def add_line(self,v):
        self.lines.append(v)
    def __getitem__(self,number):
        return self.lines[number]
ABCSymbol.typecode = TC.Struct(ABCSymbol,
                                [TC.Iint('id'),
                                TC.Array('Array',ABCLine.typecode,'lines',undeclared=True)],#,childnames="ABCLine")], # Specifies xsd:type in Array
                                pname='ABCSymbol',
                                aname='ABCSymbol')

# if you want to use the above class from within zsiServer, you have to use an inventive name like the one below
#class AnotherBloodyShitClassWithADifferentName(ABCSymbol):
#    pass
