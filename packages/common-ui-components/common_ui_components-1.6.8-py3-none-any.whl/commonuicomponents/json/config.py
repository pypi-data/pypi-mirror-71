from pathlib import Path
from .json import Json, Result as BaseResult
from ..staticutils import StaticUtils

class Result(BaseResult):
   def __init__(self, created, json):
      super().__init__(created)
      
      


class Config(Json):
   def __init__(self):
      super().__init__(("config.json", "default_config.json", Path("..", "default_config.json")))
   
   def load(self):
      created = super().load()
      
      if created == None:
         raise ValueError("Config not loaded")
      
      StaticUtils.TITLE = self._json["title"]
      
      if created:
         if "version" not in json:
            json["version"] = "1.6.7"
         
         if self.isWindows():
            widgetFont = self._json.get("widgetFont", "")
            
            if type(widgetFont) != str and len(widgetFont) > 1:
               widgetFont[1] = StaticUtils.round(widgetFont[1] / 1.2)
      
      return Result(created)
