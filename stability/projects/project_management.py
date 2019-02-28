'''
Python module containing Project management code.
'''
import datetime
import shutil
from stability.tools import FileData


class Project():

    def __init__(self, project_name: str, initial_folder: str) -> None:
        self.name = project_name
        self.initial_folder = initial_folder
        self.project_creation_date = datetime.datetime.now()

        self.files: dict = {}  # dict of File objects (which each contain list of FileData objects)
        self.create_project_archive()


    def create_project_archive(self, starting_path: str='C:'):
        self.archive_path = os.path.join(starting_path, 'stability', 'project_archives', self.name.lower())
        try:
            os.makedirs(self.archive_path)
        except OSError:  # if folder already exists
            pass

    def add_file(self, file_path: str, file_name: str):
        self.files[file_name] = File(file_path, file_name)
        self.copy_file_to_project_archive(file_name)

    def copy_file_to_project_archive(self, file_name: str, file_version: str='latest'):
        '''
        file_version arg determines which file gets copied (if multiple files are tracked for a the File)
          - 'latest' uses the most recent version
          - a specific file path string uses that exact file path
        '''
        if file_version == 'latest':
            file = self.files[file_name].latest_file()
        else:
            file = file_version
        shutil.copy(file, self.archive_path)



class File():

    def __init__(self, file_path: str, file_name: str) -> None:
        self.initial_filepath = file_path
        self.file_name = file_name  # not necessarily the _actual_ name of the file
        self.initial_tracking_date = datetime.datetime.now()

        self.filedatas: list = [FileData(initial_filepath)]  # FileData objects
        self.file_add_times: list = [datetime.datetime.now()]
        self.extension = self.filedatas[0].extension

    @property
    def num_versions(self):
        return len(self.filedatas)

    def latest_file(self) -> str:
        return self.filedatas[-1].filepath

    def add_updated_fileversion(self, filepath):
        if os.path.splitext(filepath)[-1] == self.extension:
            self.filedatas.append(FileData(filename))
            self.file_add_times.append(datetime.datetime.now())
        else:
            print(f'Error - Updated file version has different extension!')
            print(f'Expected: {self.extension}  Recieved: ...{filepath[-15:]}')
            print('File version update not saved.\n')

