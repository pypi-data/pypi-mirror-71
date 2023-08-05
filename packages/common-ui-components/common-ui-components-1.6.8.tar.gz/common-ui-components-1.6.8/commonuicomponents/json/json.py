from json import dump, load
from platform import system
from ..staticutils import StaticUtils

class Result:
   __SYSTEM = system()
   
   def __init__(self, created):
      self.__created = created
   
   def __bool__(self):
      return self.__created
   
   @staticmethod
   def isLinux():
      return Result.__SYSTEM == "Linux"
   
   @staticmethod
   def isWindows():
      return Result.__SYSTEM == "Windows"


class Json:
   def __init__(self, paths):
      self.__paths = paths if StaticUtils.isIterable(paths) else tuple(paths)
   
   def dump(self):
      try:
         with open(self.__paths[0], "w", encoding = "utf-8") as f:
            dump(self._json, f, ensure_ascii = False, indent = 3)
      
      except Exception as e:
         StaticUtils.showerror(e)
   
   def load(self):
      for configCreated, path in enumerate(self.__paths):
         try:
            with open(path, encoding = "utf-8") as f:
               self._json = load(f)
         
         except FileNotFoundError:
            pass
         
         else:
            return not not configCreated
