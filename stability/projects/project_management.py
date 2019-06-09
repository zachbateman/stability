'''
Python module containing Project management code.
'''
import os
import datetime
import shutil
import json
import copy
from stability.tools import FileData
from pprint import pprint as pp

DATE_FORMAT = '%b %d %Y %H:%M:%S'  # for use with strftime and strptime



class ProjectGroup():
    '''
    Class for handling all of the user's Projects
    '''
    def __init__(self, **kwargs) -> None:
        self.projects: dict = {}
        self.archived_projects: dict = {}

        for key in kwargs:  # will only be triggered if using self.fromdict()
            setattr(self, key, kwargs[key])


    def load_existing_projects(self) -> dict:
        try:
            with open(self._saved_group_filepath()) as json_file:
                d = json.load(json_file)
            for key in d:
                setattr(self, key, d[key])
        except FileNotFoundError:  # if user had not previously saved info
            print('No existing projects found.')

    def save_projects(self, starting_path: str='C:/'):
        with open(self._saved_group_filepath(), 'w') as json_file:
            json.dump(self.asdict(), json_file)
        print('Projects saved.')

    def _saved_group_filepath(self, starting_path: str='C:/') -> str:
        return os.path.join(starting_path, 'stability', 'project_group.json')

    def add_new_project(self, project_name: str='', initial_folder: str='', proj_obj=None) -> None:
        if proj_obj:
            self.projects[proj_obj.name] = proj_obj
            print(f'{proj_obj} added to Project Group!')
        else:
            self.projects[project_name] = Project(project_name=project_name, initial_folder=initial_folder)
            print(f'{self.projects[project_name]} created!')
        self.save_projects()

    def archive_project(self, project_name: str) -> None:
        pass

    def delete_archived_project(self, project_name: str) -> None:
        pass

    def __repr__(self) -> str:
        return 'Project Group: ' + '\n  - '.join(self.projects.keys()) + '\n'

    def __eq__(self, other) -> bool:
        if (self.projects == other.projects
            and self.archived_projects == other.archived_projects):
            return True
        return False

    def asdict(self) -> dict:
        '''Convert instance into representative dict'''
        d = {}
        d['projects'] = {name: proj.asdict() for name, proj in self.projects.items()}
        d['archived_projects'] = {name: proj.asdict() for name, proj in self.archived_projects.items()}
        return d

    @classmethod
    def fromdict(cls, d):
        '''Create class instance from dict'''
        kwargs = copy.deepcopy(d)
        kwargs['projects'] = {name: Project.fromdict(d) for name, d in kwargs['projects'].items()}
        kwargs['archived_projects'] = {name: Project.fromdict(d) for name, d in kwargs['archived_projects'].items()}
        return cls(**kwargs)



class Project():

    def __init__(self, project_name: str='', initial_folder: str='', **kwargs) -> None:
        self.name = project_name
        self.initial_folder = initial_folder

        # Now convert datetime.now() to a _ROUNDED_ time via DATE_FORMAT
        # Provides same date after using .asdict() and .fromdict() conversion.
        self.project_creation_date = datetime.datetime.strptime(datetime.datetime.now().strftime(DATE_FORMAT), DATE_FORMAT)

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
            self.files[file_obj.file_name] = file_obj
            self.copy_file_to_project_archive(file_obj.file_name)
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
        kwargs = copy.deepcopy(d)
        kwargs['project_creation_date'] = datetime.datetime.strptime(d['project_creation_date'], DATE_FORMAT)
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

        # Now convert datetime.now() to a _ROUNDED_ time via DATE_FORMAT
        # Provides same date after using .asdict() and .fromdict() conversion.
        self.initial_tracking_date = datetime.datetime.strptime(datetime.datetime.now().strftime(DATE_FORMAT), DATE_FORMAT)

        self.filedatas: list = [FileData(initial_filepath)]  # FileData objects
        self.file_add_times: list = [datetime.datetime.strptime(datetime.datetime.now().strftime(DATE_FORMAT), DATE_FORMAT)]
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
            self.file_add_times.append(datetime.datetime.strptime(datetime.datetime.now().strftime(DATE_FORMAT), DATE_FORMAT))
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
        d['file_add_times'] = [ftime.strftime(DATE_FORMAT) for ftime in self.file_add_times]
        d['extension'] = self.extension
        return d

    @classmethod
    def fromdict(cls, d):
        '''Create class instance from dict'''
        kwargs = copy.deepcopy(d)
        kwargs['initial_tracking_date'] = datetime.datetime.strptime(d['initial_tracking_date'], DATE_FORMAT)
        kwargs['filedatas'] = [FileData(fp) for fp in d['filedatas']]
        kwargs['file_add_times'] = [datetime.datetime.strptime(ftime, DATE_FORMAT) for ftime in d['file_add_times']]
        return cls(**kwargs)
