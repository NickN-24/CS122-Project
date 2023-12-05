import customtkinter as ctk
import tkinter as tk
import matplotlib.pyplot as plt
import numpy as np
import os
import re
import pickle
import webbrowser
from page import Page
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class AnalysisPage(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)
        
        self.selected_starting_year = ctk.StringVar()
        self.selected_ending_year = ctk.StringVar()
        self.selected_sort = ctk.StringVar()
        
        self.tabview = ctk.CTkTabview(self, width=250)
        self.tabview.grid(row=0, column=1, rowspan=4, padx=(20, 0), pady=20, sticky="nsew")
        self.tabview.grid(row=0, column=1, rowspan=4, padx=(20, 0), pady=20, sticky="nsew")
        self.tabview.add("Genre")
        self.tabview.add("Score")
        self.tabview.add("Ratings")
        self.tabview.tab("Genre").grid_columnconfigure(0, weight=1)
        self.tabview.tab("Score").grid_columnconfigure(0, weight=1)
        self.tabview.tab("Ratings").grid_columnconfigure(0, weight=1)
        
        # selecting year range for three graphs
        self.graph_button(self.tabview.tab("Genre"), "Genres")
        self.graph_button(self.tabview.tab("Score"), "Score")
        self.graph_button(self.tabview.tab("Ratings"), "Rating")
        
        self.data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),"data")
        self.years = ctk.CTkFrame(self)
        self.years.grid(row=0, column=2, padx=20, pady=(10, 0))
        years = self.get_years()
        self.selected_starting_year.set(years[0])
        self.selected_ending_year.set(years[0])
        sort_option_list = ["Title", "Score", "Time"]
        self.selected_sort.set(sort_option_list[1])

        self.filter = ctk.CTkLabel(self.years, text="Select Starting Year:", anchor="center")
        self.filter.grid(row=0, column=0, padx=20, pady=(10, 0))
        self.filter2 = ctk.CTkLabel(self.years, text="Select Ending Year:", anchor="center")
        self.filter2.grid(row=0, column=1, padx=20, pady=(10, 0))
    
        self.filter_startoptionemenu = tk.OptionMenu(self.years, self.selected_starting_year, *years)
        self.filter_startoptionemenu.grid(row=1, column=0, padx=20, pady=(10, 10))
        self.filter_endoptionemenu = tk.OptionMenu(self.years, self.selected_ending_year, *years)
        self.filter_endoptionemenu.grid(row=1, column=1, padx=20, pady=(10, 10))

        self.retrieve = ctk.CTkButton(master=self, text="Update List",
                                      command=lambda : self.load_movies(self.selected_starting_year.get(),
                                                                        self.selected_ending_year.get()))
        self.retrieve.grid(row=2, column=2, padx=20, sticky="nsew")
            
        self.sort = ctk.CTkFrame(self, width=250)
        self.sort.grid(row=3, column=2, padx=20, pady=(10, 20), sticky="nsew")
        self.label_cb = ctk.CTkLabel(master=self.sort, text="Sort by:", anchor='center')
        self.label_cb.grid(row=0, column=0, padx=20, pady=10, sticky="nsw")
        self.sort_option = tk.OptionMenu(self.sort, self.selected_sort, *sort_option_list)
        self.sort_option.grid(row=0, column=1, padx=20, pady=10, sticky="nsew")
        self.sort_direction = ctk.CTkCheckBox(master=self.sort, text="Ascending", command=self.load_movie_scroll)
        self.sort_direction.grid(row=0, column=2, pady=10, padx=20, sticky="nse")
        self.selected_sort.trace("w", self.load_movie_scroll)

        self.scrollable_frame = None
        self.scrollable_frame_switches = None
        self.data = None
        self.load_movies(years[0], years[0])

    def graph_button(self, master, section) :
        self.label_rating = ctk.CTkLabel(master, text="Select a starting and ending year from the dropdown\n" + "menu on the right to proceed.")
        self.label_rating.grid(row=0, column=0, padx=20, pady=20)
        self.button_rating = ctk.CTkButton(master, text="Proceed", command=lambda: self.on_option_select(master, section))
        self.button_rating.grid(row=1, column=0, padx=20, pady=20)

    def on_option_select(self, root, section):
        selected_start = self.selected_starting_year.get()
        selected_end = self.selected_ending_year.get()
        if selected_start > selected_end :
            selected_start, selected_end = selected_end, selected_start
        self.display_graph(root, (int(selected_start), int(selected_end)), section)

    def display_graph(self, root, years, column_name) :
        self.graph = None
        if years[1]==years[0] :
            self.graph = self.single_graph(years[0], column_name)
        else :
            self.graph = self.multi_graph(years[0], years[1], column_name)
        self.canvas = FigureCanvasTkAgg(self.graph, master = root)   
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")

    def single_graph(self, year, column_name) :
        fig = plt.figure()
        flat = self.data[column_name]
        if column_name == "Genres" :
            flat = np.concatenate(flat)
        unique_e, counts = np.unique(flat, return_counts=True)
        plt.style.use('seaborn-darkgrid')
        plt.bar(unique_e, counts, width=0.8/len(unique_e) if column_name=="Score" else 0.8, color='skyblue', edgecolor='black', alpha=0.8)
        plt.xlabel(column_name)
        plt.ylabel("Count")
        plt.title(f"{column_name} Counts for {year}")
        plt.xticks(rotation=45, ha="right")
        plt.grid(linestyle="--", linewidth=0.5, alpha=0.5)
        plt.gca().spines['top'].set_visible(False)
        plt.gca().spines['right'].set_visible(False)
        plt.tight_layout()
        plt.close()
        return fig


    def multi_graph(self, year_from, year_to, column_name) :
        if year_from > year_to :
            year_from, year_to = year_to, year_from
        year_to += 1
        line_styles = ["-", ":", "--", "-."]

        fig = plt.figure()
        plt.style.use('seaborn-darkgrid')

        info = dict()
        
        years = np.unique(self.data["Year"])
        years.sort()
        flat = self.data[column_name]
        for i in np.unique(np.concatenate(flat) if column_name=="Genres" else flat) :
            info[i] = [0]*len(years)
        count=0
        for year in years :
            flat = (self.data[self.data["Year"]==year])[column_name]
            for i in np.concatenate(flat) if column_name=="Genres" else flat :
                info[i][count]+=1
            count+=1
        count=0
        for key in info :
            plt.plot(years, info[key],
                     label=key, linestyle=line_styles[count//10])
            count+=1

        plt.xlabel("Year")
        plt.ylabel("Count")
        plt.title(f"{column_name} Counts from {year_from} through {year_to-1}")
        plt.legend(loc="center left", bbox_to_anchor = (1.0, 0.5))
        plt.xticks(rotation=45, ha="right")
        plt.grid(linestyle="--", linewidth=0.5, alpha=0.5)
        plt.gca().spines['top'].set_visible(False)
        plt.gca().spines['right'].set_visible(False)
        plt.tight_layout()
        plt.close()
        return fig
    
    def sort_movies(self) :
        self.data = (self.data[np.argsort(self.data, order=self.selected_sort.get())])[::1 if self.sort_direction.get() else -1]
    
    def load_movies(self, year_from, year_to) :
        if year_from > year_to :
            year_from, year_to = year_to, year_from
        self.data = np.concatenate([
            pickle.load(open(os.path.join(self.data_dir, f"{i}_movies.pickle"), 'rb'))
            for i in range(int(year_from), int(year_to) + 1)
            if os.path.exists(os.path.join(self.data_dir, f"{i}_movies.pickle"))
        ])
        self.load_movie_scroll()

    def load_movie_scroll(self, *args) :
        self.sort_movies()
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
                image.destroy()
                frame.destroy()
        self.scrollable_frame_switches = []
        count = 0
        for item in self.data[:100] :
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
    
