import customtkinter as ctk
from analysis_page import AnalysisPage
from data_page import DataPage
from home_page import HomePage

class View(ctk.CTkFrame):
    def __init__(self, *args, **kwargs):
        ctk.CTkFrame.__init__(self, *args, **kwargs)
        p1 = HomePage(self)
        p2 = AnalysisPage(self)
        p3 = DataPage(self)

        buttonframe = ctk.CTkFrame(self)
        container = ctk.CTkFrame(self)
        buttonframe.pack(side="top", fill="x", expand=False)
        container.pack(side="top", fill="both", expand=True)

        p1.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p2.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p3.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        b1 = ctk.CTkButton(buttonframe, text="Home Page", command=p1.show)
        b2 = ctk.CTkButton(buttonframe, text="Analysis", command=p2.show)
        b3 = ctk.CTkButton(buttonframe, text="Data Management", command=p3.show)

        b1.pack(side="left")
        b2.pack(side="left")
        b3.pack(side="left")

        p1.show()

if __name__ == "__main__":
    root = ctk.CTk()
    main = View(root)
    main.pack(side="top", fill="both", expand=True)
    root.wm_geometry("1280x720")
    root.title("Movie Trends Analyzer")
    root.mainloop()
