from datetime import datetime
import json

from typing import List 
from pathlib import Path
import shutil
import sys
import colorama 
from markdown import extensions, markdown
import os

class Parser: #base clase 
    extensions : List[str] = [] #annotations for the developer? dont actually impose constraints of the object type being parsed.
   # def valid_extension(self,extension):
   #     return extension in self.extensions

    def parse(self,path: Path, source: Path, dest: Path): #because this is the base class we dont want it being ran by itself. 
        raise NotImplementedError

    def read(self,path: Path):
        with open(path,'r') as file:
           return file.read()
#
    def write(self,dest,content,filename,ext ='.txt',nl=False):
        newline = '' if not nl else '\n'
        full_path :Path = dest/ f'{filename}{ext}'
#
        with open(full_path,'a') as file:
            file.write(newline +str(content))
#
   # def copy(self,path: Path,source,dest):
   #     shutil.copy2(path,dst=dest/path.relative_to(source))

    def create_dir(self,path: Path,dest: Path,source: Path):
        directory =  path.relative_to(source)/dest 
        directory.mkdir(parents=True,exist_ok=True)

    @staticmethod
    def validate_path(dest):
        return True if dest in (path.name.lower() for path in Path('.').iterdir())  else  False
    
    @staticmethod
    def validate_file(path: Path,filename):
        return (True if filename in 
                [file.name.split('.')[0] for file in path.rglob('*') if file.is_file()] 
                else False)

        


class JsonParser(Parser):
    extension ='.json'

    def _JSON(self,data:str):
        data = data.replace('true','"True"')
        json_object = json.loads(data)
        return json_object

    def parse(self, path:Path, dest ,data,source =Path('.'),filename =None):
        filename = filename or 'file'

        if not self.validate_path(dest):
            self.create_dir(path,dest,source) 
        
        content = self._JSON(data)

        if not self.validate_file(path=path,filename = filename):
            self.write(dest= path,content='[{}]',filename=filename, ext =JsonParser.extension)
        
        self._file_handle(path,filename,JsonParser.extension)
        self.write(dest= path,content=',',filename=filename, ext =JsonParser.extension)
        self.write(dest= path,content=content,filename=filename, ext =JsonParser.extension,nl=True)
        self.write(dest= path,content=']',filename=filename, ext =JsonParser.extension)
        
        print(colorama.Fore.GREEN +f'Saved to file. {filename}. @{datetime.utcnow().time().__str__()}')
    
    @staticmethod
    def _file_handle(path:Path,filename,ext ='.txt'):
        full_path :Path = path/ f'{filename}{ext}'
        with open(full_path, 'rb+') as filehandle:
            filehandle.seek(-1, os.SEEK_END)
            filehandle.truncate()
#j.parse(path=Path('recorded'),dest ='',data ='{"one":1}')