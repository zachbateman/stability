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
        self.title(f'Welcome to Stability, {os.getlogin()}')

        # Variables
        # self.project_names = tkinter.StringVar()
        self.projects: list = []

        # Menu
        self.add_menu(commands={'File': lambda: print('File button'), 'Help': lambda: print('Help')})

        # GUI widgets
        section1 = self.add_section('section1')
        section1.add_widget('btn', text='Find Dup Files', command_func=self.find_dup_files)
        section1.add_widget('btn', text='New Project', command_func=self.new_project)
        section1.add_widget('btn', text='Print Projects', command_func=self.print_projects)


    def find_dup_files(self, *args):
        os.system('cls')
        directory = filedialog.askdirectory()
        print(f'Searching {directory} for duplicate files.\n')
        dups = dup_finder.find_dup(directory)
        dup_finder.print_results(dups)

    def new_project(self, *args):

        with self.popup() as popup:
            # popup.wm_title('New Project')
            # popup.configure(background='#cfd2d2')
            # popup.geometry('300x200')  # size of initial window in pixels

            popup.add_widget('lbl', 'New Project Name')
            project_name = popup.add_widget('entry')

            initial_dir = ''
            def grab_directory(*args):
                popup.focus()
                initial_dir = filedialog.askdirectory()
                popup.focus()

            def create_project(*args):
                if project_name.get() == '':
                    print('Error.  Please provide Project Name.')
                else:
                    self.projects.append(Project(project_name.get(), initial_dir))
                popup.destroy()
                print(f'Created {self.projects[-1]}')

            popup.add_widget('lbl', 'Select initial directory')
            popup.add_widget('btn', 'Folder', command_func=grab_directory)
            popup.add_widget('btn', 'Create Project', command_func=create_project)

    def print_projects(self, *args):
        for proj in self.projects:
            print(proj)



if __name__ == '__main__':
    GUI()
