import customtkinter as ctk
import os
import re
import webreader
import pickle
from page import Page

class DataPage(Page) :
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        self.menu_frame = ctk.CTkFrame(self, corner_radius=0)
        self.menu_frame.grid(row=0, column=0, rowspan=4, padx=20, pady=20, sticky="nsew")
        self.menu_frame.grid_columnconfigure(0, weight=1)

        self.delete_data = ctk.CTkButton(self.menu_frame, text="Delete Data", command=self.delete_selected)
        self.delete_data.grid(row=0, column=0, padx=20, pady=(20,10), sticky="nsew")
        self.delete_text = ctk.CTkLabel(master=self.menu_frame, text="Delete the selected years")
        self.delete_text.grid(row=1, column=0, padx=20, sticky="ew")

        self.retrieve_data = ctk.CTkButton(self.menu_frame, text="Retrieve Data", command=lambda:self.fetch_data(self.retrieve_text.get("0.0","end-1c")))
        self.retrieve_data.grid(row=2, column=0, padx=10, pady=10)
        self.data_text = ctk.CTkLabel(master=self.menu_frame, text="Input the years to grab.\nie. 1980-1984,1987,2014-2012,2022")
        self.data_text.grid(row=3, column=0, padx=10, pady=5, sticky="ew")
        self.retrieve_text = ctk.CTkTextbox(self.menu_frame, height=80)
        self.retrieve_text.insert("0.0", "1980-1984,1987,2014-2012,2022")
        self.retrieve_text.grid(row=4, column=0, padx=10, pady=5, sticky="ew")

        self.current_text = ctk.CTkLabel(master=self.menu_frame, text="Input : N/A")
        self.current_text.grid(row=5, column=0, padx=10, pady=5, sticky="ew")
        self.progress_text = ctk.CTkLabel(master=self.menu_frame, text="Progress : 0/0")
        self.progress_text.grid(row=6, column=0, padx=10, pady=5, sticky="ew")

        self.data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),"data")
        self.scrollable_frame = None
        self.scrollable_frame_switches = None
        self.update_movie_list()

    def delete_selected(self):
        self.scrollable_frame = ctk.CTkScrollableFrame(self, label_text="Data Years")
        self.scrollable_frame.grid(row=0, column=1, padx=10, pady=10, width=180, sticky="nse")
        self.scrollable_frame.grid_columnconfigure(0, weight=1)

        for check, label in self.scrollable_frame_switches:
            filepath = os.path.join(self.data_dir, label._text[5:])
            if check.get() and os.path.exists(filepath):
                os.remove(filepath)
        self.update_movie_list()
    
    def fetch_data(self, input):
        os.makedirs(self.data_dir, exist_ok=True)
        years = self.get_years_from_input(input)
        self.current_text.configure(text=f"Input : {years}")
        self.current_text.update()
        count = 0
        self.progress_text.configure(text=f"Progress : 0/{len(years)}")
        self.progress_text.update()
        for year in years :
            data = webreader.scrape_top50(year, 50)
            with open(os.path.join(self.data_dir, f"{year}_movies.pickle"), "wb") as f:
                pickle.dump(data, f)
            count += 1
            self.progress_text.configure(text=f"Progress : {count}/{len(years)}")
            self.progress_text.update()
        self.update_movie_list()

    def get_years_from_input(self, input):
        year_ranges = re.findall(r'(\d{4})\s*-\s*(\d{4})|\b(\d{4})\b', input)

        years = []
        for range_tuple in year_ranges:
            if range_tuple[0]:  # If it's a range
                start_year, end_year = map(int, range_tuple[:2])
                if start_year <= end_year:
                    years.extend(range(start_year, end_year + 1))
                else:
                    years.extend(range(start_year, end_year - 1, -1))
            elif range_tuple[2]:  # If it's a single year
                years.append(int(range_tuple[2]))

        return years
    
    def update_movie_list(self):
        if self.scrollable_frame != None :
            self.scrollable_frame.destroy()
        self.scrollable_frame = ctk.CTkScrollableFrame(self, label_text="Data Years")
        self.scrollable_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nse")
        self.scrollable_frame.grid_columnconfigure(0, weight=1)
        if self.scrollable_frame_switches != None :
            for check, label in self.scrollable_frame_switches :
                check.destroy()
                label.destroy()
        self.scrollable_frame_switches = []
        count=0
        for f in os.listdir(self.data_dir):
            if (re.compile(r'^\d{4}_movies\.pickle$')).match(f) :
                label = ctk.CTkLabel(master=self.scrollable_frame, text=f"{f}")
                label.grid(row=count, column=1, padx=10, pady=(0, 20), sticky="ew")
                select = ctk.CTkCheckBox(master=self.scrollable_frame, text="")
                select.grid(row=count, column=0, padx=10, pady=(0, 20), sticky="w")
                self.scrollable_frame_switches.append((select, label))
                count+=1