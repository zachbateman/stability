'''
Standard tkinter GUI for stability project.
'''
import tkinter
from tkinter import filedialog
import easy_gui
import os
from stability.tools import dup_finder
from stability.projects import Project, File



class GUI(easy_gui.EasyGUI):

    def __init__(self, *args, **kwargs):
        super().__init__()

        self.title(f'Welcome to Stability, {os.getlogin()}')
        self.iconbitmap(bitmap=os.path.join(os.path.dirname(__file__), 'resources', 'transparent.ico'))

        # Variables
        # self.project_names = tkinter.StringVar()
        self.projects: list = []

        # Menu
        self.add_menu(commands={'File': lambda: print('File button'), 'Help': lambda: print('Help')})

        # GUI widgets
        section1 = self.add_section('section1', return_section=True)
        section1.add_widget('btn', text='Find Dup Files', command=self.find_dup_files)
        section1.add_widget('btn', text='New Project', command=self.new_project)
        section1.add_widget('btn', text='Print Projects', command=self.print_projects)


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




if __name__ == '__main__':
    application = GUI()
    application.mainloop()
