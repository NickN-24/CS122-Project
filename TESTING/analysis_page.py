import customtkinter as ctk
import os
import re
import pickle
from page import Page

class AnalysisPage(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)
        
        self.tabview = ctk.CTkTabview(self, width=250)
        self.tabview.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.tabview.add("Genre")
        self.tabview.add("Score")
        self.tabview.add("Rating")
        self.tabview.tab("Genre").grid_columnconfigure(0, weight=1)
        self.tabview.tab("Score").grid_columnconfigure(0, weight=1)
        self.tabview.tab("Rating").grid_columnconfigure(0, weight=1)
        
        self.label_genre = ctk.CTkLabel(self.tabview.tab("Genre"), text="Graph for genre")
        self.label_genre.grid(row=0, column=0, padx=20, pady=20)
        self.label_score = ctk.CTkLabel(self.tabview.tab("Score"), text="Graph for score")
        self.label_score.grid(row=0, column=0, padx=20, pady=20)
        self.label_rating = ctk.CTkLabel(self.tabview.tab("Rating"), text="Graph for rating")
        self.label_rating.grid(row=0, column=0, padx=20, pady=20)

        self.data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),"data")
        self.scrollable_frame = None
        self.scrollable_frame_switches = None

        self.filter = ctk.CTkFrame(self)
        self.filter.grid(row=0, column=2, padx=10, pady=20, sticky="nsew")
        self.label_cb = ctk.CTkLabel(master=self.filter, text="Select Years:")
        self.label_cb.grid(row=0, column=0)
        # TODO : Above
            
        self.sort = ctk.CTkFrame(self)
        self.sort.grid(row=1, column=2, padx=10, pady=20, sticky="nsew")
        self.label_cb = ctk.CTkLabel(master=self.sort, text="Sort by:")
        self.label_cb.grid(row=0, column=0)
        self.checkbox_1 = ctk.CTkCheckBox(master=self.sort, text="Title")
        self.checkbox_1.grid(row=1, column=0, pady=(20, 0), padx=20, sticky="n")
        self.checkbox_2 = ctk.CTkCheckBox(master=self.sort, text="Rating")
        self.checkbox_2.grid(row=2, column=0, pady=(20, 0), padx=20, sticky="n")
        self.checkbox_3 = ctk.CTkCheckBox(master=self.sort, text="Option 3")
        self.checkbox_3.grid(row=3, column=0, pady=20, padx=20, sticky="n")

        # TODO : replace hardcoded years with actual values
        self.load_movies(2010, 2011)

    def load_movies(self, year_from, year_to) :
        if self.scrollable_frame != None :
            self.scrollable_frame.destroy()
        self.scrollable_frame = ctk.CTkScrollableFrame(self, width=250, label_text="Movies")
        self.scrollable_frame.grid(row=1, column=1, padx=20, pady=20, sticky="nsew")
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
                    m_title = ctk.CTkLabel(master=self.scrollable_frame, text=item[1])
                    m_title.grid(row=count, column=1, padx=10, pady=(0, 20), sticky="ew")
                    count+=1


        # for f in os.listdir(self.data_dir):
        #     if (re.compile(r'^\d{4}_movies\.pickle$')).match(f) :
        #         label = ctk.CTkLabel(master=self.scrollable_frame, text=f"Year {f}")
        #         label.grid(row=count, column=1, padx=10, pady=(0, 20), sticky="ew")
        #         select = ctk.CTkCheckBox(master=self.scrollable_frame, text="")
        #         select.grid(row=count, column=0, padx=10, pady=(0, 20), sticky="w")
        #         self.scrollable_frame_switches.append((select, label))
        #         count+=1