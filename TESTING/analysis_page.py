import customtkinter as ctk
import tkinter as tk
import os
import re
import pickle
import webbrowser
from page import Page

class AnalysisPage(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)
        
        self.selected_starting_year = ctk.StringVar()
        self.selected_ending_year = ctk.StringVar()
        
        self.tabview = ctk.CTkTabview(self, width=250)
        self.tabview.grid(row=0, column=1, rowspan=3, padx=(20, 0), pady=20, sticky="nsew")
        self.tabview.grid(row=0, column=1, rowspan=3, padx=(20, 0), pady=20, sticky="nsew")
        self.tabview.add("Genre")
        self.tabview.add("Score")
        self.tabview.add("Ratings")
        self.tabview.tab("Genre").grid_columnconfigure(0, weight=1)
        self.tabview.tab("Score").grid_columnconfigure(0, weight=1)
        self.tabview.tab("Ratings").grid_columnconfigure(0, weight=1)
        
        # selecting year range for three graphs
        self.graph_button(self.tabview.tab("Genre"))
        self.graph_button(self.tabview.tab("Score"))
        self.graph_button(self.tabview.tab("Ratings"))
        
        self.data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),"data")
        self.years = ctk.CTkFrame(self)
        self.years.grid(row=0, column=2, padx=20, pady=(10, 0))
        years = self.get_years()

        self.filter = ctk.CTkLabel(self.years, text="Select Starting Year:", anchor="center")
        self.filter.grid(row=0, column=0, padx=20, pady=(10, 0))
        self.filter2 = ctk.CTkLabel(self.years, text="Select Ending Year:", anchor="center")
        self.filter2.grid(row=0, column=1, padx=20, pady=(10, 0))
    
        self.filter_startoptionemenu = tk.OptionMenu(self.years, self.selected_starting_year, *years)
        self.filter_startoptionemenu.grid(row=1, column=0, padx=20, pady=(10, 10))
        self.filter_endoptionemenu = tk.OptionMenu(self.years, self.selected_ending_year, *years)
        self.filter_endoptionemenu.grid(row=1, column=1, padx=20, pady=(10, 10))

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

    def graph_button(self, master) :
        self.label_rating = ctk.CTkLabel(master, text="Select a starting and ending year from the dropdown\n" + "menu on the right to proceed.")
        self.label_rating.grid(row=0, column=0, padx=20, pady=20)
        self.button_rating = ctk.CTkButton(master, text="Proceed", command=lambda: self.on_option_select(master))
        self.button_rating.grid(row=1, column=0, padx=20, pady=20)

    def on_option_select(self, root):
        selected_start = self.selected_starting_year.get()
        selected_end = self.selected_ending_year.get()
        result_label = ctk.CTkLabel(root, text="")
        result_label.configure(text=f"Displaying graph for movies from {selected_start} to {selected_end}")  
        result_label.grid(row=2, column=0, padx=20, pady=20)    

    def load_movies(self, year_from, year_to) :
        if self.scrollable_frame != None :
            self.scrollable_frame.destroy()
        self.scrollable_frame = ctk.CTkScrollableFrame(self, width=250, label_text="Movies")
        self.scrollable_frame.grid(row=1, column=2, padx=20, pady=5, sticky="nsew")
        self.scrollable_frame.grid_columnconfigure(0, weight=1)
        if self.scrollable_frame_switches != None :
            for frame, image, title, details, genres in self.scrollable_frame_switches :
                genres.destroy()
                details.destroy()
                title.destroy()
                image.destory()
                frame.destroy()
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
                    m_title.bind("<Button-1>", lambda e, url=item[7]:webbrowser.open_new_tab(url))
                    m_title.grid(row=0, column=1, padx=(5,1), pady=1, sticky="nsw")
                    m_details = ctk.CTkLabel(master=m_frame, text=f"{item[0]} | {item[4]}min | ☆ {item[2]:.1f} | {item[5]}", anchor="w")
                    m_details.grid(row=1, column=1, padx=(5,1), sticky="nsw")
                    m_genres = ctk.CTkLabel(master=m_frame, text=f"{', '.join(item[6])}", anchor="w")
                    m_genres.grid(row=2, column=1, padx=(5,1), sticky="nsw")

                    self.scrollable_frame_switches.append((m_frame, m_image, m_title, m_details, m_genres))
                    count+=1

    def get_years(self):
        years = []
        for f in os.listdir(self.data_dir):
            if (re.compile(r'\d{4}_movies\.pickle$')).match(f) :
                years.append(int(f[:4]))
        return years
