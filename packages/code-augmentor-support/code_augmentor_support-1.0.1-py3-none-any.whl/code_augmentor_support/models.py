import json
from types import SimpleNamespace as Object

class JsonDumpHelper(json.JSONEncoder):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def default(self, o):
        if isinstance(o, Object):
            return self._convertObjectToDict(o)
        return super().default(o)
        
    def _convertObjectToDict(self, o):
        d = dict(o.__dict__)
        for k in d.keys():
            v = d[k]
            if isinstance(v, Object):
                d[k] = self._convertObjectToDict(v)
        return d

class ProcessCodeContext:
    def __init__(self):
        self._header = None
        self._globalScope = {}
        self._fileScope = {}
        self._fileAugCodes = None
        self._augCodeIndex = 0
        self._srcFile = None

    # Intended for use by scripts
    def newGenCode(self):
        return Object(id = 0, contentParts = [])

    # Intended for use by scripts
    def newContent(self, content, exactMatch=False):
        return Object(content = content, exactMatch = exactMatch)
        
    @property
    def header(self):
        return self._header
        
    @header.setter
    def header(self, value):
        self._header = value

    #readonly
    @property
    def globalScope(self):
        return self._globalScope

    #readonly
    @property
    def fileScope(self):
        return self._fileScope
        
    @property
    def fileAugCodes(self):
        return self._fileAugCodes
    
    @fileAugCodes.setter
    def fileAugCodes(self, value):
        self._fileAugCodes = value
        
    @property
    def augCodeIndex(self):
        return self._augCodeIndex
        
    @augCodeIndex.setter
    def augCodeIndex(self, value):
       self._augCodeIndex = value
       
    @property
    def srcFile(self):
        return self._srcFile
        
    @srcFile.setter
    def srcFile(self, value):
        self._srcFile = value
