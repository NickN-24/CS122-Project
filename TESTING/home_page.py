import customtkinter as ctk
from page import Page

class HomePage(Page):
   def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        
        #Define a callback function
        def callback(url):
            webbrowser.open_new_tab(url)
            
        label = ctk.CTkLabel(self, text="Link to the Github repo.", cursor="hand2")
        label.pack(side="top", fill="both", expand=True)
        label.bind("<Button-1>", lambda e:
            callback("https://github.com/NickN-24/CS122-Project"))