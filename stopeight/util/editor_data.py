from future.utils import with_metaclass
from stopeight.util.runnable import Singleton

class ScribbleData(with_metaclass(Singleton,list)):
#class ScribbleData(Singleton):
    #def __init__(self, **kwargs):
    #    super(ScribbleData,self).__init__(**kwargs)
    pass

#class WaveData(with_metaclass(Singleton)):
#    pass