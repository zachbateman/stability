'''
Standard tkinter GUI for stability project.
'''
import tkinter
from tkinter import filedialog
import os
from stability.tools import dup_finder
from stability.projects import Project, File


class GUI(tkinter.Frame):

    def __init__(self, root, *args, **kwargs):
        tkinter.Frame.__init__(self, root, *args, **kwargs)
        root.title(f'Welcome to Stability, {os.getlogin()}')
        root.iconbitmap(bitmap=os.path.join(os.path.dirname(__file__), 'resources', 'transparent.ico'))
        root.configure(background='#cfd2d2')
        root.geometry('600x450')  # size of initial window in pixels

        # Variables
        # self.project_names = tkinter.StringVar()
        self.projects: list = []

        # Menu
        self.menu = tkinter.Menu(root)
        self.menu.add_command(label='File')
        self.menu.add_command(label='Help')
        root.config(menu=self.menu)

        # GUI widgets
        self.check_dups_btn = tkinter.Button(text='Find Dup Files', command=self.find_dup_files, **btn_kwargs())
        self.check_dups_btn.grid(row=0, column=0, **btn_grid_kwargs())

        self.new_proj_btn = tkinter.Button(text='New Project', command=self.new_project, **btn_kwargs())
        self.new_proj_btn.grid(row=1, column=0, **btn_grid_kwargs())

        self.print_proj_btn = tkinter.Button(text='Print Projects', command=self.print_projects, **btn_kwargs())
        self.print_proj_btn.grid(row=2, column=0, **btn_grid_kwargs())

        self.grid()


    def find_dup_files(self):
        os.system('cls')
        directory = filedialog.askdirectory()
        print(f'Searching {directory} for duplicate files.\n')
        dups = dup_finder.find_dup(directory)
        dup_finder.print_results(dups)

    def new_project(self):
        popup = tkinter.Toplevel()
        popup.wm_title('New Project')
        popup.iconbitmap(bitmap=os.path.join(os.path.dirname(__file__), 'resources', 'transparent.ico'))
        popup.configure(background='#cfd2d2')
        popup.geometry('300x200')  # size of initial window in pixels


        project_name = tkinter.StringVar()
        proj_name_lbl = tkinter.Label(popup, text='New Project Name')
        proj_name_lbl.grid(row=0, column=0)
        proj_name_entry = tkinter.Entry(popup, textvariable=project_name)
        proj_name_entry.grid(row=0, column=1)

        initial_dir = ''
        def grab_directory():
            popup.focus()
            initial_dir = filedialog.askdirectory()
            popup.focus()

        def create_project():
            if project_name.get() == '':
                print('Error.  Please provide Project Name.')
            else:
                self.projects.append(Project(project_name.get(), initial_dir))
            popup.destroy()
            print(f'Created {self.projects[-1]}')

        proj_initital_dir_lbl = tkinter.Label(popup, text='Select initial directory')
        proj_initital_dir_lbl.grid(row=1, column=0)
        proj_initital_dir_btn = tkinter.Button(popup, text='Folder', command=grab_directory, **btn_kwargs())
        proj_initital_dir_btn.grid(row=1, column=1, **btn_grid_kwargs())

        create_proj_btn = tkinter.Button(popup, text='Create Project', command=create_project, **btn_kwargs())
        create_proj_btn.grid(row=2, column=0, columnspan=2, **btn_grid_kwargs())

    def print_projects(self):
        for proj in self.projects:
            print(proj)


def btn_kwargs() -> dict:
    return {'bg': '#88aabb', 'width': 20}

def btn_grid_kwargs() -> dict:
    '''Provides default kwargs to button widgets on .grid()'''
    return {'padx': 6, 'pady': 6}




if __name__ == '__main__':
    root = tkinter.Tk()
    application = GUI(root)
    root.mainloop()
