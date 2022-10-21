
import itertools
import pandas as pd
import json 
from pathlib import Path
import numpy as np
from itertools import islice
import asyncio
from asyncio import AbstractEventLoop

class Parser:
    extension = []

    def parse(path,dest):
        raise NotImplementedError

class JsonReader(Parser):
    extension = '.json'
  
    def read(self,file,path :Path =Path('.')):
        pass
  
    def read_all(self,path:Path,include_sub =True, multibatch=0):
        valid_files =[]
        
        if include_sub:
            evaluation = "path.rglob('*')"
        else:
            evaluation ='path.iterdir()'
        
        for file in eval(evaluation):
            if multibatch:
                if file.suffix == JsonReader.extension:
                    valid_files.append(file) 
                self._batch(valid_files,n_batches=multibatch)
            
            else:
                if file.suffix == JsonReader.extension:
                    self._read_file(file)
    

    def _read_file(self, filepath:Path):
        with open(filepath,'r') as file:
            json_data = json.load(file)
            return json_data
    
    @staticmethod
    def _batch(files,n_batches):
        raise NotImplementedError
        batch_size = np.ceil(len(files)/n_batches)        
        for index in range(0,len(files)):
            yield from (files[index],)

    def parse(self,path:Path,**kwargs):       
        self.read_all(path=path,**kwargs)

           
        