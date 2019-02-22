'''
Main module of Stability package.
'''
from .gui import GUI
import tkinter

def main():
    root = tkinter.Tk()
    GUI(root)
    root.mainloop()
