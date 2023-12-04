import customtkinter as ctk
from analysis_page import AnalysisPage
from data_page import DataPage
from home_page import HomePage

ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("dark-blue")

class View(ctk.CTkFrame):
    def __init__(self, *args, **kwargs):
        ctk.CTkFrame.__init__(self, *args, **kwargs)
        home = HomePage(self)
        analysis = AnalysisPage(self)
        data = DataPage(self)

        buttonframe = ctk.CTkFrame(self)
        container = ctk.CTkFrame(self)
        buttonframe.pack(side="top", fill="x", expand=False)
        container.pack(side="top", fill="both", expand=True)

        home.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        analysis.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        data.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        home_button = ctk.CTkButton(buttonframe, text="Home Page", command=home.show)
        analysis_button = ctk.CTkButton(buttonframe, text="Analysis", command=analysis.show)
        data_button = ctk.CTkButton(buttonframe, text="Data Management", command=data.show)
            
        home_button.pack(side="left")
        analysis_button.pack(side="left")
        data_button.pack(side="left")
        
        home.show()

if __name__ == "__main__":
    root = ctk.CTk()
    main = View(root)
    main.pack(side="top", fill="both", expand=True)
    root.wm_geometry("1280x720")
    root.title("Movie Trends Analyzer")
    root.mainloop()
