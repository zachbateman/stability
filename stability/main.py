'''
Main module of Stability package.
'''
from .gui import GUI
import tkinter

def main():
    application = GUI()
    application.mainloop()
