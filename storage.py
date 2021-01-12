import os

from abc import ABC,abstractmethod
from env import env,envpath

class ExistsError(FileExistsError):
    pass

class NotFoundError(FileNotFoundError):
    pass

class Storage(ABC):
    """
    Abstract class for implementing storage backends
    """
    def __init__(self):
        self.setUp()

    @abstractmethod
    def setUp(self):
        """
        Run @ instantiation
        """
        pass

    @abstractmethod
    def store(self,data:bytes,fid:str)->int:
        """
        Store bytes as FID
        """
        pass

    @abstractmethod
    def retrieve(self,fid:str)->bytes:
        """
        Retrieve bytes associated with FID
        """
        pass

class FileStorage(Storage):

    def store(self,data,fid):
        p = self._rel_path(fid)
        if not os.path.exists(p):
            with open(p,"wb") as f:
                written = f.write(data)
            return written
        else:
            raise ExistsError 

    def retrieve(self,fid):
        try:
            with open(self._rel_path(fid),"rb") as f:
                d = f.read()
            return d
        except FileNotFoundError:
            raise NotFoundError

    def setUp(self):
        self.path = envpath("STORAGE_PATH","storage")
        try:
            os.makedirs(self.path)
        except FileExistsError:
            pass

    def _rel_path(self,path):
        return os.path.join(self.path,path)

