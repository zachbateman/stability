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
        root.title('Stability')
        root.iconbitmap(bitmap=os.path.join(os.path.dirname(__file__), 'resources', 'transparent.ico'))
        root.configure(background='#cfd2d2')
        root.geometry('600x450')  # size of initial window in pixels

        self.check_dups_btn = tkinter.Button(text='Find Dup Files', command=self.find_dup_files, **btn_kwargs())
        self.check_dups_btn.grid(row=0, column=0, **btn_grid_kwargs())

        self.new_proj_btn = tkinter.Button(text='New Project', command=self.new_project)
        self.new_proj_btn.grid(row=1, column=0)

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

        proj_name_lbl = tkinter.Label(popup, text='New Project Name')
        proj_name_lbl.grid(row=0, column=0)
        proj_name_entry = tkinter.Entry(popup)
        proj_name_entry.grid(row=0, column=1)

        initial_dir = ''
        def grab_directory():
            selected_folder = filedialog.askdirectory()
            initial_dir = selected_folder
            return selected_folder

        proj_initital_dir_lbl = tkinter.Label(popup, text='Select initial directory')
        proj_initital_dir_lbl.grid(row=1, column=0)
        proj_initital_dir_btn = tkinter.Button(popup, text='Folder', command=grab_directory)
        proj_initital_dir_btn.grid(row=1, column=1)

        create_proj_btn = tkinter.Button(popup, text='Create Project', command=popup.destroy)
        create_proj_btn.grid(row=2, column=0, columnspan=2)


def btn_kwargs() -> dict:
    return {'bg': '#88aabb', 'width': 20}

def btn_grid_kwargs() -> dict:
    '''Provides default kwargs to button widgets on .grid()'''
    return {'padx': 6, 'pady': 6}




if __name__ == '__main__':
    root = tkinter.Tk()
    application = GUI(root)
    root.mainloop()
