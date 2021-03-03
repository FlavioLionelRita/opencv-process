from .base import *
import tkinter as tk
from tkinter import ttk
from os import path,listdir


class UiHelper():

    @staticmethod
    def center(win):
        # Center the root screen
        win.update_idletasks()
        width = win.winfo_width()
        frm_width = win.winfo_rootx() - win.winfo_x()
        win_width = width + 2 * frm_width
        height = win.winfo_height()
        titlebar_height = win.winfo_rooty() - win.winfo_y()
        win_height = height + titlebar_height + frm_width
        x = win.winfo_screenwidth() // 2 - win_width // 2
        y = win.winfo_screenheight() // 2 - win_height // 2
        win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        win.deiconify() 

class ToolTip():
    def __init__(self, widget):
        self.widget = widget
        self.tipWindow = None
        self.id = None
        self.x = self.y = 0
    
    def showtip(self, text):
        self.text = text
        if self.tipWindow or not self.text:
            return
        x, y, cx, cy = self.widget.bbox('insert')
        x = x + self.widget.winfo_rootx() + 0
        y = y + cy + self.widget.winfo_rooty() + 40
        self.tipWindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry('+%d+%d' % (x, y))
        
        label = tk.Label(tw, text=self.text, justify=tk.LEFT,
                         background='#000000', foreground='yellow', relief=tk.SOLID, borderwidth=1)
        label.pack(ipadx=1)
     
    def hidetip(self):
        tw = self.tipWindow
        self.tipWindow = None
        if tw:
            tw.destroy()
    
class IconProvider():
    def __init__(self,iconsPath=None): 
        self.icons = {}
        if iconsPath is not None:
           self.loadIcons(iconsPath)

    def loadIcons(self,iconsPath):
        for item in listdir(iconsPath):
            name=path.splitext(path.basename(item))[0]
            self.icons[name] = tk.PhotoImage(file=path.join(iconsPath,item))  

    def getIcon(self,key):
        key = key.replace('.','')
        if key not in self.icons: key = '_blank'
        return self.icons[key.replace('.','')]   

class ToolbarPanel(ttk.Frame):
    def __init__(self, master,mgr):
        super(ToolbarPanel,self).__init__(master)
        self.mgr=mgr
        self.buttons = {}
        self.onCommand=Event()

    def load(self,dic):
        for key in dic:
            item=Helper.nvl(dic[key],{})
            item['command'] = key
            self.add(**item)

    def add(self,command,img=None,tootip=None):
        icon = self.mgr.getIcon(Helper.nvl(img,command))
        btn = ttk.Button(self, image=icon, command=  lambda: self.raiseCommand(command) )
        btn.image = icon
        btn.pack(side=tk.LEFT)
        self.createToolTip(btn,Helper.nvl(tootip,command))
        self.buttons[command] =btn

    def createToolTip(self, widget, text):
        toolTip = ToolTip(widget)
        def enter(event):
            toolTip.showtip(text)
        def leave(event):
            toolTip.hidetip()
        widget.bind('<Enter>', enter)
        widget.bind('<Leave>', leave) 

    def raiseCommand(self, command=None):
        self.onCommand(command)      

    def subscribe(self,method): 
        self.onCommand += method 
          
    def unsubscribe(self,method): 
        self.onCommand -= method      
       
  