'''
Python module containing Project management code.
'''
import os
import datetime
import shutil
import json
from stability.tools import FileData
from pprint import pprint as pp

DATE_FORMAT = '%b %d %Y %H:%M:%S'  # for use with strftime and strptime
# DATE_FORMAT = '%B %d %Y'


class ProjectGroup():
    '''
    Class for handling all of the user's Projects
    '''
    def __init__(self) -> None:
        self.projects: dict = self.load_all_existing_projects()
        self.archived_projects: dict = self.load_all_archived_projects()


    def load_all_existing_projects(self) -> dict:
        with open(self._saved_group_filepath()) as json_file:
            # LOAD DATA
            pass
        projects = {'project 1': ...}
        return projects

    def load_all_archived_projects(self) -> dict:
        pass

    def save_projects(self, starting_path: str='C:/'):
        with open(self._saved_group_filepath()) as json_file:
            json.dump(object, json_file)
        print('Projects saved.')

    def _saved_group_filepath(self) -> str:
        return os.path.join(starting_path, 'stability', 'project_group.json')

    def add_new_project(self, project_name: str, initial_folder: str) -> None:
        pass

    def archive_project(self, project_name: str) -> None:
        pass

    def delete_archived_project(self, project_name: str) -> None:
        pass

    def __repr__(self) -> str:
        return 'Project Group: ' + '\n  - '.join(self.projects.keys()) + '\n'

    def asdict(self) -> dict:
        '''Convert instance into representative dict'''
        # TODO
        return {}


class Project():

    def __init__(self, project_name: str='', initial_folder: str='', **kwargs) -> None:
        self.name = project_name
        self.initial_folder = initial_folder
        self.project_creation_date = datetime.datetime.now()

        self.files: dict = {}  # dict of File objects (which each contain list of FileData objects)
        self.create_project_archive()

        for key in kwargs:
            setattr(self, key, kwargs[key])


    def create_project_archive(self, starting_path: str='C:/'):
        self.archive_path = os.path.join(starting_path, 'stability', 'project_archives', self.name.lower())
        try:
            os.makedirs(self.archive_path)
        except OSError:  # if folder already exists
            pass

    def add_file(self, file_path: str='', file_name: str='', file_obj=None):
        if file_obj:
            file_name = file_obj.file_name
            self.files[file_name] = file_obj
        else:
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

    def __repr__(self) -> str:
        return f'Project: {self.name}'

    def __eq__(self, other) -> bool:
        if (self.name == other.name
            and self.file_name == other.file_name
            and self.initial_folder == other.initial_folder
            and self.project_creation_date == other.project_creation_date):
            return True
        breakpoint()
        return False

    def asdict(self) -> dict:
        '''Convert instance into representative dict'''
        d = {}
        d['name'] = self.name
        d['initial_folder'] = self.initial_folder
        d['project_creation_date'] = self.project_creation_date.strftime(DATE_FORMAT)
        d['files'] = {file_name: file.asdict() for file_name, file in self.files.items()}
        return d

    @classmethod
    def fromdict(cls, d):
        '''Create class instance from dict'''
        kwargs = {k: v for k, v in d.items()}
        kwargs['files'] = {file_name: File.fromdict(file_dict) for file_name, file_dict in d['files'].items()}
        return cls(**kwargs)


class File():

    def __init__(self, initial_filepath: str='', file_name: str='', **kwargs) -> None:
        '''
        Create File object using specified initial_filepath and file_name.
        Alternatively, (if using File.fromdict()) create instance from representative dict.
        '''
        self.initial_filepath = initial_filepath
        self.file_name = file_name  # not necessarily the _actual_ name of the file

        # Now convert datetime.now() to a time rounded via DATE_FORMAT
        # Provides same date after using .asdict() and .fromdict() conversion.
        self.initial_tracking_date = datetime.datetime.strptime(datetime.datetime.now().strftime(DATE_FORMAT), DATE_FORMAT)

        self.filedatas: list = [FileData(initial_filepath)]  # FileData objects
        self.file_add_times: list = [datetime.datetime.now()]
        self.extension = self.filedatas[0].extension

        for key in kwargs:
            setattr(self, key, kwargs[key])


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

    def __repr__(self) -> str:
        return f'File: {self.file_name}'

    def __eq__(self, other) -> bool:
        if (self.initial_filepath == other.initial_filepath
            and self.file_name == other.file_name
            and self.initial_tracking_date == other.initial_tracking_date):
            return True
        return False

    def asdict(self) -> dict:
        '''Convert instance into representative dict'''
        d = {}
        d['initial_filepath'] = self.initial_filepath
        d['file_name'] = self.file_name
        d['initial_tracking_date'] = self.initial_tracking_date.strftime(DATE_FORMAT)
        d['filedatas'] = [fd.filepath for fd in self.filedatas]
        d['file_add_times'] = self.file_add_times
        d['extension'] = self.extension
        return d

    @classmethod
    def fromdict(cls, d):
        '''Create class instance from dict'''
        kwargs = {k: v for k, v in d.items()}
        kwargs['initial_tracking_date'] = datetime.datetime.strptime(d['initial_tracking_date'], DATE_FORMAT)
        kwargs['filedatas'] = [FileData(fp) for fp in d['filedatas']]
        return cls(**kwargs)
