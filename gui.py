#!/usr/local/bin/python3
"""
gui.py - provides the interface for the GUI
 
Written by Bruce Fuda for Intermediate Programming
Modified with permission by Edwin Griffin
"""

# Comment out the tkinter line not appropriate for your Python version
from tkinter import *   # Python 3
#from Tkinter import *  # Python 2

import time

class simpleapp_tk(Tk):#This class is the entire window that the game is run in.
  def __init__(self,parent):
    Tk.__init__(self,parent)
    self.parent = parent
    self.initialize()

  def initialize(self):
    self.grid()

    # used for polling for user input only
    # i.e. wait variable
    self.inputVariable = StringVar()

    scrollbar = Scrollbar(self)
    scrollbar.grid(row=0, column=2, sticky=N+S)

    self.text = Text(self, wrap=WORD, yscrollcommand=scrollbar.set)
    self.text.grid(column=0,row=0,columnspan=2,sticky='NSEW')
    self.text.config(state=DISABLED)

    scrollbar.config(command=self.text.yview)

    self.entryVariable = StringVar()
    self.entry = Entry(self,textvariable=self.entryVariable)
    self.entry.grid(column=0,row=1,sticky='SEW')
    self.entry.bind("<Return>", self.OnPressEnter)

    button = Button(self,text=u"Enter",
                    command=self.OnButtonClick)
    button.grid(column=1,row=1)

    self.grid_columnconfigure(0,weight=1)
    self.grid_rowconfigure(0,weight=1)
    self.resizable(True,True)
    self.update()
    self.geometry(self.geometry())       
    self.entry.focus_set()
    self.entry.selection_range(0, END)

  def OnButtonClick(self):
    self.inputVariable.set( self.entryVariable.get() )

  def OnPressEnter(self,event):
    self.inputVariable.set( self.entryVariable.get() )

  # The write function simulates the behaviour of the print method
  # but uses the input textfield and text display instead of the usual
  # standard input/output we're used to from our previous programs
  def write(self,msg):
    self.text.config(state=NORMAL)
    self.text.insert(END, msg)
    self.text.insert(END, "\n")
    self.update()
    self.text.config(state=DISABLED)
    self.text.see(END)
    self.entryVariable.set('')
    self.entry.focus_set()
    
  def quit(self):
    sys.exit(0)
