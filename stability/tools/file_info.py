'''
Python module containing file-handling code.
'''
import os


class FileData():

    def __init__(self, filepath: str) -> None:
        self.filepath = filepath
        self.extension = os.path.splitext(filepath)[-1]


    @property
    def last_modified(self):
        '''Return last time file was modified'''
        return os.path.getmtime(self.filepath)

    @property
    def size(self) -> float:
        '''Return size of file in kilobytes (KB)'''
        return os.path.getsize(self.filepath) / 1000

