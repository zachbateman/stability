'''
Standard tkinter GUI for stability project.
'''
import tkinter
from stability.tools import dup_finder


class GUI(tkinter.Frame):
    
    def __init__(self, root, *args, **kwargs):
        tkinter.Frame.__init__(self, root, *args, **kwargs)
        root.title('Stability')
        
        self.check_dups_btn = tkinter.Button(text='Dup Files', bg='#8899dd').grid(row=0, column=0)
        self.grid()
        
        
        
if __name__ == '__main__':
    root = tkinter.Tk()
    application = GUI(root)
    root.mainloop()
