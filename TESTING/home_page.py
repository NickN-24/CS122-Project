import customtkinter as ctk
import tkinter as tk
from tkinter import font
from page import Page
import webbrowser

class HomePage(Page):
   def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        
        #Define a callback function
        def callback(url):
            webbrowser.open_new_tab(url)
            
        title_label = tk.Label(self, text="MOVIE TRENDS ANALYZER", 
                               font=("Tw Cen MT Condensed Extra Bold", 60), 
                               fg='#3a7ebf', bg='#d9d9d9')
        title_label.pack()
        
        description_label = tk.Label(self, text="Great for film enthusiasts, this application is designed for users to examine\n"
                                              + "trends among movies regarding popular genres and common scores or ratings. Users\n"
                                              + "will be able to explore the statistics of popular movies from the 1980s until today.", 
                                         font=("Tw Cen MT", 15), bg='#d9d9d9', anchor='center')
        description_label.pack(ipady=20)
        
        instruction_label = tk.Label(self, text="Instructions",
                                        font=("Tw Cen MT", 30), 
                                        fg='#3a7ebf', bg='#d9d9d9')
        instruction_label.pack(ipady=20)
        instruction_label2 = tk.Label(self, text="In the Analysis page, you will be able to select the years you would like to look\n"
                                                 + "at, then generate and view graphs with just a click of a button. The movies will be\n"
                                                 + "listed on the side in case any piques your interest.\n\n" 
                                                 + "The Data Management page will allow you to retrieve and delete any pickle files\n"
                                                 + "used in order to generate the graphs.\n\n",
                                        font=("Tw Cen MT", 15), bg='#d9d9d9')
        instruction_label2.pack()
        
        repo_label = tk.Label(self, text="Link to the Github repo.", 
                                  font=("Tw Cen MT", 15), bg='#d9d9d9',
                                  cursor="hand2")
        repo_label.pack(side='bottom', ipady=20)
        repo_label.bind("<Button-1>", lambda e:
            callback("https://github.com/NickN-24/CS122-Project"))
