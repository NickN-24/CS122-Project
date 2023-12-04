import customtkinter as ctk
import tkinter as tk
import os
import pickle
import webbrowser
from page import Page

class AnalysisPage(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)
        
        selected_option = ctk.StringVar()

        def on_option_select(root):
            selected = selected_option.get()
            result_label = ctk.CTkLabel(root, text="")
            result_label.configure(text=f"Selected Option: {selected}")
            result_label.grid(row=2, column=0, padx=20, pady=20)
            
        self.tabview = ctk.CTkTabview(self, width=250)
        self.tabview.grid(row=0, column=1, rowspan=3, padx=(20, 0), pady=20, sticky="nsew")
        self.tabview.add("Genre")
        self.tabview.add("Score")
        self.tabview.add("Rating")
        self.tabview.tab("Genre").grid_columnconfigure(0, weight=1)
        self.tabview.tab("Score").grid_columnconfigure(0, weight=1)
        self.tabview.tab("Rating").grid_columnconfigure(0, weight=1)
        
        self.label_genre = ctk.CTkLabel(self.tabview.tab("Genre"), text="Select a year from the dropdown\n" + "menu on the right to proceed.")
        self.label_genre.grid(row=0, column=0, padx=20, pady=20)
        self.button_genre = ctk.CTkButton(self.tabview.tab("Genre"), text="Display graphs for Genre Trends", command=lambda: on_option_select(self.tabview.tab("Genre")))
        self.button_genre.grid(row=1, column=0, padx=20, pady=20)
        
        self.label_score = ctk.CTkLabel(self.tabview.tab("Score"), text="Select a year from the dropdown\n" + "menu on the right to proceed.")
        self.label_score.grid(row=0, column=0, padx=20, pady=20)
        self.button_score = ctk.CTkButton(self.tabview.tab("Score"), text="Display graphs for Score Trends", command=lambda: on_option_select(self.tabview.tab("Score")))
        self.button_score.grid(row=1, column=0, padx=20, pady=20)
        
        self.label_rating = ctk.CTkLabel(self.tabview.tab("Rating"), text="Select a year from the dropdown\n" + "menu on the right to proceed.")
        self.label_rating.grid(row=0, column=0, padx=20, pady=20)
        self.button_rating = ctk.CTkButton(self.tabview.tab("Rating"), text="Display graphs for Rating Trends", command=lambda: on_option_select(self.tabview.tab("Rating")))
        self.button_rating.grid(row=1, column=0, padx=20, pady=20)
        
        self.filter = ctk.CTkLabel(self, text="Select Time Range:", anchor="center")
        self.filter.grid(row=0, column=2, padx=20, pady=(10, 0))
        options=["2010-2011", "2011-2012", "2012-2013", "2013-2014", "2014-2015", 
                 "2015-2016", "2016-2017", "2017-2018", "2018-2019", "2019-2020",
                 "2020-2021", "2021-2022", "2022-2023"]
        
        # ctk.CTkOption was giving me trouble here so its going to be a tkinter option menu for now
        self.filter_optionemenu = tk.OptionMenu(self.filter, selected_option, *options)
        self.filter_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))

        self.data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),"data")
        self.scrollable_frame = None
        self.scrollable_frame_switches = None
            
        self.sort = ctk.CTkFrame(self, width=250)
        self.sort.grid(row=2, column=2, padx=20, pady=(0, 20), sticky="nsew")
        self.label_cb = ctk.CTkLabel(master=self.sort, text="Sort by:", anchor='center')
        self.label_cb.grid(row=0, column=0)
        self.checkbox_1 = ctk.CTkCheckBox(master=self.sort, text="Title")
        self.checkbox_1.grid(row=1, column=0, pady=(10, 0), padx=20, sticky="n")
        self.checkbox_2 = ctk.CTkCheckBox(master=self.sort, text="Rating")
        self.checkbox_2.grid(row=2, column=0, pady=(10, 0), padx=20, sticky="n")
        self.checkbox_3 = ctk.CTkCheckBox(master=self.sort, text="Date")
        self.checkbox_3.grid(row=3, column=0, pady=(10, 0), padx=20, sticky="n")

        # TODO : replace hardcoded years with actual values
        self.load_movies(2016, 2016)

    def load_movies(self, year_from, year_to) :
        if self.scrollable_frame != None :
            self.scrollable_frame.destroy()
        self.scrollable_frame = ctk.CTkScrollableFrame(self, width=250, label_text="Movies")
        self.scrollable_frame.grid(row=1, column=2, padx=20, pady=5, sticky="nsew")
        self.scrollable_frame.grid_columnconfigure(0, weight=1)
        if self.scrollable_frame_switches != None :
            for check, label in self.scrollable_frame_switches :
                check.destroy()
                label.destroy()
        self.scrollable_frame_switches = []
        count=0
        for i in range(year_from, year_to+1) :
            with open(os.path.join(self.data_dir, f"{i}_movies.pickle"),'rb') as f:
                data = pickle.load(f)
                for item in data :
                    m_frame = ctk.CTkFrame(master=self.scrollable_frame)
                    m_frame.grid(row=count, column=0, pady=5, sticky="new")
                    m_image = ctk.CTkLabel(master=m_frame, text="", image=item[3], anchor="nw")
                    m_image.image = item[3]
                    m_image.grid(row=0, column=0, rowspan=2, pady=1, sticky="nsew")
                    m_title = ctk.CTkLabel(master=m_frame, text=f"{count+1}. {item[1]}", anchor="w", cursor="hand2")
                    m_title.grid(row=0, column=1, padx=(5,1), pady=1, sticky="nsw")
                    # Change to proper link later
                    m_title.bind("<Button-1>", lambda e:webbrowser.open_new_tab("https://github.com/NickN-24/CS122-Project"))
                    m_details = ctk.CTkLabel(master=m_frame, text=f"{item[0]} | {item[4]}min | ☆ {item[2]:.1f} | {item[5]}", anchor="w")
                    m_details.grid(row=1, column=1, padx=(5,1), sticky="nsw")
                    m_genres = ctk.CTkLabel(master=m_frame, text=f"{', '.join(item[6])}", anchor="w")
                    m_genres.grid(row=2, column=1, padx=(5,1), sticky="nsw")
                    count+=1
