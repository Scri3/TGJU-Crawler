import customtkinter
import os
import mysql.connector

# from api import records

customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        
        self.title("Currency Rates")
        self.geometry(f"{1650}x{800}")

        # configure grid layout (4x4)
        # self.grid_columnconfigure(0, weight=1)
        # self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)


        # new frame
        self.crawl_frame = customtkinter.CTkFrame(self, width=250, corner_radius=0)
        self.crawl_frame.grid(row=0, column=1, padx=20, pady=10, rowspan=4, sticky="nsew")
        self.crawl_frame.grid_rowconfigure((2,3), weight=1)
        self.crawl_frame.grid_columnconfigure(0, weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, padx=20, pady=10, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(5, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Currency Crawler", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.AddButton = customtkinter.CTkButton(self.sidebar_frame,text="Add", command=self.add_button_event)
        self.AddButton.grid(row=1, column=0, padx=20, pady=10)
        self.SelectButton = customtkinter.CTkButton(self.sidebar_frame,text="Select", command=self.select_button_event,state="disabled")
        self.SelectButton.grid(row=2, column=0, padx=20, pady=10)
        self.EditButton = customtkinter.CTkButton(self.sidebar_frame,text="Edit", command=self.edit_button_event,state="disabled")
        self.EditButton.grid(row=3, column=0, padx=20, pady=10)
        self.DeleteButton = customtkinter.CTkButton(self.sidebar_frame,text="Delete", command=self.delete_button_event,state="disabled")
        self.DeleteButton.grid(row=4, column=0, padx=20, pady=10)
        # , state="disabled"
        # # self.sidebar_button_7 = customtkinter.CTkButton(self.sidebar_frame, command=self.sidebar_button_event)
        # # self.sidebar_button_7.grid(row=5, column=0, padx=20, pady=10)
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=6, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=7, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=8, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=9, column=0, padx=20, pady=(10, 20))

        # create main entry and button
        # # self.entry = customtkinter.CTkEntry(self, placeholder_text="CTkEntry")
        # # self.entry.grid(row=3, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")

        # # self.main_button_1 = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"))
        # # self.main_button_1.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")

        # create textbox
        self.textbox = customtkinter.CTkTextbox(self, width=375,height=2000, border_width=4, border_color="white",
        font=customtkinter.CTkFont(size=25, weight="bold"))
        self.textbox.grid(row=0, column=2, padx=(20,20), pady=(10,10), sticky="nsew")
        # create label
        # self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="CustomTkinter", font=customtkinter.CTkFont(size=20, weight="bold"))
        # self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.welcome_label=customtkinter.CTkLabel(self.crawl_frame,text="Welcome!",font=customtkinter.CTkFont(size=50, weight="bold"),width=1000)
        self.welcome_label.grid(row=0, column=0, padx=70, pady=10, sticky="nsew")
        # create crawl button
        self.CrawlButton=customtkinter.CTkButton(self.crawl_frame,text="Start Crawling",font=customtkinter.CTkFont(size=30, weight="bold"),width=1000, command = self.crawl_button_event)
        self.CrawlButton.grid(row=1, column=0, padx=70, pady=(10, 30), sticky="nsew")
        





        # # # # #  create tabview
        # # # # tab1="                Tab 1               "
        # # # # tab2="                Tab 2               "
        # # # # tab3="                Tab 3               "
        # # # # tab4="                Tab 4               "

        self.crawl_result = customtkinter.CTkFrame(self.crawl_frame, width=250,height=580, border_width=10, border_color="darkgreen")
        self.crawl_result.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        # # # # self.tabview.add(tab1)
        # # # # self.tabview.add(tab2)
        # # # # self.tabview.add(tab3)
        # # # # self.tabview.add(tab4)
        self.crawl_result.grid_columnconfigure((0,1,2,3), weight=1)
        self.crawl_result.grid_rowconfigure((0,1,2,3,4,5,6,7,8), weight=1)  # configure grid of individual tabs
        
        


        
        # Frame:

        # row 0
        self.ID0=customtkinter.CTkLabel(self.crawl_result,text="ID ",font=customtkinter.CTkFont(size=20, weight="bold"))
        self.ID0.grid(row=0, column=0, padx=8, pady=(15,20), sticky="nsew")

        self.Clabel0=customtkinter.CTkLabel(self.crawl_result,text= "Currency ", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.Clabel0.grid(row=0, column=1, padx=10, pady=(15,20), sticky="nsew")

        self.Rate0=customtkinter.CTkLabel(self.crawl_result,text= "Rate ", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.Rate0.grid(row=0, column=2, padx=20, pady=(15,20), sticky="nsew")

        self.Time0=customtkinter.CTkLabel(self.crawl_result,text= "Time ", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.Time0.grid(row=0, column=3, padx=20, pady=(15,20), sticky="nsew")

        

        rowpady=15
        # row 1

        self.ID1=customtkinter.CTkLabel(self.crawl_result,text="",font=customtkinter.CTkFont(size=20, weight="bold"))
        self.ID1.grid(row=1, column=0, padx=8, pady=rowpady, sticky="nsew")

        self.Clabel1=customtkinter.CTkLabel(self.crawl_result,text= "", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.Clabel1.grid(row=1, column=1, padx=10, pady=rowpady, sticky="nsew")

        self.Rate1=customtkinter.CTkLabel(self.crawl_result,text= "", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.Rate1.grid(row=1, column=2, padx=20, pady=rowpady, sticky="nsew")

        self.Time1=customtkinter.CTkLabel(self.crawl_result,text= "", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.Time1.grid(row=1, column=3, padx=20, pady=rowpady, sticky="nsew")

        

        # row 2

        self.ID2=customtkinter.CTkLabel(self.crawl_result,text="",font=customtkinter.CTkFont(size=20, weight="bold"))
        self.ID2.grid(row=2, column=0, padx=8, pady=rowpady, sticky="nsew")

        self.Clabel2=customtkinter.CTkLabel(self.crawl_result,text= "", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.Clabel2.grid(row=2, column=1, padx=10, pady=rowpady, sticky="nsew")

        self.Rate2=customtkinter.CTkLabel(self.crawl_result,text= "", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.Rate2.grid(row=2, column=2, padx=20, pady=rowpady, sticky="nsew")

        self.Time2=customtkinter.CTkLabel(self.crawl_result,text= "", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.Time2.grid(row=2, column=3, padx=20, pady=rowpady, sticky="nsew")

        

        # row 3

        self.ID3=customtkinter.CTkLabel(self.crawl_result,text="",font=customtkinter.CTkFont(size=20, weight="bold"))
        self.ID3.grid(row=3, column=0, padx=8, pady=rowpady, sticky="nsew")

        self.Clabel3=customtkinter.CTkLabel(self.crawl_result,text= "", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.Clabel3.grid(row=3, column=1, padx=10, pady=rowpady, sticky="nsew")

        self.Rate3=customtkinter.CTkLabel(self.crawl_result,text= "", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.Rate3.grid(row=3, column=2, padx=20, pady=rowpady, sticky="nsew")

        self.Time3=customtkinter.CTkLabel(self.crawl_result,text= "", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.Time3.grid(row=3, column=3, padx=20, pady=rowpady, sticky="nsew")

        

        # row 4

        self.ID4=customtkinter.CTkLabel(self.crawl_result,text="",font=customtkinter.CTkFont(size=20, weight="bold"))
        self.ID4.grid(row=4, column=0, padx=8, pady=rowpady, sticky="nsew")

        self.Clabel4=customtkinter.CTkLabel(self.crawl_result,text= "", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.Clabel4.grid(row=4, column=1, padx=10, pady=rowpady, sticky="nsew")

        self.Rate4=customtkinter.CTkLabel(self.crawl_result,text= "", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.Rate4.grid(row=4, column=2, padx=20, pady=rowpady, sticky="nsew")

        self.Time4=customtkinter.CTkLabel(self.crawl_result,text= "", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.Time4.grid(row=4, column=3, padx=20, pady=rowpady, sticky="nsew")

        

        # row 5

        self.ID5=customtkinter.CTkLabel(self.crawl_result,text="",font=customtkinter.CTkFont(size=20, weight="bold"))
        self.ID5.grid(row=5, column=0, padx=8, pady=rowpady, sticky="nsew")

        self.Clabel5=customtkinter.CTkLabel(self.crawl_result,text= "", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.Clabel5.grid(row=5, column=1, padx=10, pady=rowpady, sticky="nsew")

        self.Rate5=customtkinter.CTkLabel(self.crawl_result,text= "", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.Rate5.grid(row=5, column=2, padx=20, pady=rowpady, sticky="nsew")

        self.Time5=customtkinter.CTkLabel(self.crawl_result,text= "", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.Time5.grid(row=5, column=3, padx=20, pady=rowpady, sticky="nsew")

        

        # row 6

        self.ID6=customtkinter.CTkLabel(self.crawl_result,text="",font=customtkinter.CTkFont(size=20, weight="bold"))
        self.ID6.grid(row=6, column=0, padx=8, pady=rowpady, sticky="nsew")

        self.Clabel6=customtkinter.CTkLabel(self.crawl_result,text= "", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.Clabel6.grid(row=6, column=1, padx=10, pady=rowpady, sticky="nsew")

        self.Rate6=customtkinter.CTkLabel(self.crawl_result,text= "", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.Rate6.grid(row=6, column=2, padx=20, pady=rowpady, sticky="nsew")

        self.Time6=customtkinter.CTkLabel(self.crawl_result,text= "", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.Time6.grid(row=6, column=3, padx=20, pady=rowpady, sticky="nsew")

       

        # row 7

        self.ID7=customtkinter.CTkLabel(self.crawl_result,text="",font=customtkinter.CTkFont(size=20, weight="bold"))
        self.ID7.grid(row=7, column=0, padx=8, pady=rowpady, sticky="nsew")

        self.Clabel7=customtkinter.CTkLabel(self.crawl_result,text= "", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.Clabel7.grid(row=7, column=1, padx=10, pady=rowpady, sticky="nsew")

        self.Rate7=customtkinter.CTkLabel(self.crawl_result,text= "", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.Rate7.grid(row=7, column=2, padx=20, pady=rowpady, sticky="nsew")

        self.Time7=customtkinter.CTkLabel(self.crawl_result,text= "", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.Time7.grid(row=7, column=3, padx=20, pady=rowpady, sticky="nsew")


        # row 8

        self.ID8=customtkinter.CTkLabel(self.crawl_result,text="",font=customtkinter.CTkFont(size=20, weight="bold"))
        self.ID8.grid(row=8, column=0, padx=8, pady=rowpady, sticky="nsew")

        self.Clabel8=customtkinter.CTkLabel(self.crawl_result,text= "", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.Clabel8.grid(row=8, column=1, padx=10, pady=rowpady, sticky="nsew")

        self.Rate8=customtkinter.CTkLabel(self.crawl_result,text= "", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.Rate8.grid(row=8, column=2, padx=20, pady=rowpady, sticky="nsew")

        self.Time8=customtkinter.CTkLabel(self.crawl_result,text= "", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.Time8.grid(row=8, column=3, padx=20, pady=rowpady, sticky="nsew")

        

        

        

        self.appearance_mode_optionemenu.set("Dark")
        self.scaling_optionemenu.set("100%")
       
        


        self.textbox.insert("0.0", "Welcome! \n\n" + "Press Start Crawling button\n\n"+
        
        "Crawling from:\nhttps://tgju.org/\n\n"+"Use operators located\non left side of the window\nto edit the table\n\n"+
        "This is a university project\nmade by:\nDanial Goodarzi\nHossein Hosseini\n\nShamsipour Technical College")
        # # self.seg_button_1.configure(values=["CTkSegmentedButton", "Value 2", "Value 3"])
        # # self.seg_button_1.set("Value 2")
        self.textbox.configure(state="disabled")
        self.Crawled_label=customtkinter.CTkLabel(self.crawl_frame,text= "", font=customtkinter.CTkFont(size=40, weight="bold"))
        self.Crawled_label.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")
        


    # SQL
    conn=mysql.connector.connect(
                    host = 'localhost',
                    user = 'root',
                    passwd = 'LmN3LmN3!',
                    database = 'currency_rates')
    
    curr=conn.cursor()

    conn.close()




    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(text="Type in a number:", title="CTkInputDialog")
        print("CTkInputDialog:", dialog.get_input())

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)


    
        
        
        
        
        
        
    def api_add(self):

        TitleInput= customtkinter.CTkInputDialog(text= "Enter Currency Title: ", title="Add new currency")
        Title = TitleInput.get_input() 

        RateInput= customtkinter.CTkInputDialog(text= "Enter Currency Rate: ", title="Add new currency")
        Rate = RateInput.get_input()

        TimeInput= customtkinter.CTkInputDialog(text= "Enter Time: ", title="Add new currency")
        Time = TimeInput.get_input()

            
            
            
        self.curr.execute("""Insert into crawled_data_tb values ('{}','{}','{}','{}')""".format(self.ID,Title,Rate,Time))
        self.conn.commit()

        self.curr.execute("""SELECT * FROM crawled_data_tb where ID= '{}' """.format(self.ID))


    def add_button_event(self):
       
        self.conn._open_connection()
        

        if self.ID1._text=="" :
            
            self.ID="1"

            

            self.api_add()
            records=self.curr.fetchall()
                


            self.ID1.configure(text= records[0][0])
            self.Clabel1.configure(text=records[0][1])
            self.Rate1.configure(text=records[0][2])
            self.Time1.configure(text=records[0][3])
            

        elif self.ID2._text=="" :

            self.ID="2"


            self.api_add()
            records=self.curr.fetchall()
                


            self.ID2.configure(text=records[0][0])
            self.Clabel2.configure(text=records[0][1])
            self.Rate2.configure(text=records[0][2])
            self.Time2.configure(text=records[0][3])
        
        elif self.ID3._text=="" :

            self.ID="3"


            self.api_add()
            records=self.curr.fetchall()
                


            self.ID3.configure(text=records[0][0])
            self.Clabel3.configure(text=records[0][1])
            self.Rate3.configure(text=records[0][2])
            self.Time3.configure(text=records[0][3])
        
        elif self.ID4._text=="" :

            self.ID="4"


            self.api_add()
            records=self.curr.fetchall()
                


            self.ID4.configure(text=records[0][0])
            self.Clabel4.configure(text=records[0][1])
            self.Rate4.configure(text=records[0][2])
            self.Time4.configure(text=records[0][3])

        elif self.ID5._text=="" :

            self.ID="5"


            self.api_add()
            records=self.curr.fetchall()
                


            self.ID5.configure(text=records[0][0])
            self.Clabel5.configure(text=records[0][1])
            self.Rate5.configure(text=records[0][2])
            self.Time5.configure(text=records[0][3])

        elif self.ID6._text=="":

            self.ID="6"


            self.api_add()
            records=self.curr.fetchall()
                


            self.ID6.configure(text=records[0][0])
            self.Clabel6.configure(text=records[0][1])
            self.Rate6.configure(text=records[0][2])
            self.Time6.configure(text=records[0][3])

        elif self.ID7._text=="":

            self.ID="7"


            self.api_add()
            records=self.curr.fetchall()
                


            self.ID7.configure(text=records[0][0])
            self.Clabel7.configure(text=records[0][1])
            self.Rate7.configure(text=records[0][2])
            self.Time7.configure(text=records[0][3])

        elif self.ID8._text=="":

            self.ID="8"


            self.api_add()
            records=self.curr.fetchall()
                


            self.ID8.configure(text=records[0][0])
            self.Clabel8.configure(text=records[0][1])
            self.Rate8.configure(text=records[0][2])
            self.Time8.configure(text=records[0][3])

            self.AddButton.configure(state= "disabled")

        else:
            pass
            
        self.SelectButton.configure(state="enabled")
        
        
        self.conn.close()


    
    

    def select_button_event(self):
        # print("select_button click")


        
        AskID = customtkinter.CTkInputDialog(text= "Enter ID: ", title="Select row")

        self.ID= AskID.get_input()
        self.EditButton.configure(state="enabled")
        self.DeleteButton.configure(state="enabled")

        
        


        
    def edit_api(self):
        TitleInput= customtkinter.CTkInputDialog(text= "Enter Currency Title: ", title="Edit row")
        Title = TitleInput.get_input() 

        RateInput= customtkinter.CTkInputDialog(text= "Enter Currency Rate: ", title="Edit row")
        Rate = RateInput.get_input()
        
        DateInput= customtkinter.CTkInputDialog(text= "Enter Date: ", title="Edit row")
        Date= DateInput.get_input()

        TimeInput= customtkinter.CTkInputDialog(text= "Enter Time: ", title="Edit row")
        Time = TimeInput.get_input()

        self.curr.execute("""update crawled_data_tb 
            set Currency='{}', Current_Rate='{}', Time='{}'
            where ID='{}'
            """.format(
                Title,Rate,Time,self.ID
            ))
        self.conn.commit()
        self.curr.execute("""SELECT * FROM crawled_data_tb where ID='{}'""".format(self.ID))


    def edit_button_event(self):
        # print("edit_button click")

        self.conn._open_connection()

        if self.ID=="1":

            
            self.edit_api()

            records=self.curr.fetchall()
            self.ID1.configure(text=records[0][0])
            self.Clabel1.configure(text=records[0][1])
            self.Rate1.configure(text=records[0][2])
            self.Time1.configure(text=records[0][3])


            

            

        elif self.ID=="2":

            self.edit_api()

            records=self.curr.fetchall()
            self.ID2.configure(text=records[0][0])
            self.Clabel2.configure(text=records[0][1])
            self.Rate2.configure(text=records[0][2])
            self.Time2.configure(text=records[0][3])

        elif self.ID=="3":
            
            self.edit_api()

            records=self.curr.fetchall()
            self.ID3.configure(text=records[0][0])
            self.Clabel3.configure(text=records[0][1])
            self.Rate3.configure(text=records[0][2])
            self.Time3.configure(text=records[0][3])
            
        elif self.ID=="4":
            
            self.edit_api()

            records=self.curr.fetchall()
            self.ID4.configure(text=records[0][0])
            self.Clabel4.configure(text=records[0][1])
            self.Rate4.configure(text=records[0][2])
            self.Time4.configure(text=records[0][3])

        elif self.ID=="5":
            
            self.edit_api()

            records=self.curr.fetchall()
            self.ID5.configure(text=records[0][0])
            self.Clabel5.configure(text=records[0][1])
            self.Rate5.configure(text=records[0][2])
            self.Time5.configure(text=records[0][3])

        elif self.ID=="6":
            
            self.edit_api()

            records=self.curr.fetchall()
            self.ID6.configure(text=records[0][0])
            self.Clabel6.configure(text=records[0][1])
            self.Rate6.configure(text=records[0][2])
            self.Time6.configure(text=records[0][3])

        elif self.ID=="7":
            
            self.edit_api()

            records=self.curr.fetchall()
            self.ID7.configure(text=records[0][0])
            self.Clabel7.configure(text=records[0][1])
            self.Rate7.configure(text=records[0][2])
            self.Time7.configure(text=records[0][3])
        
        elif self.ID=="8":
            
            self.edit_api()

            records=self.curr.fetchall()
            self.ID8.configure(text=records[0][0])
            self.Clabel8.configure(text=records[0][1])
            self.Rate8.configure(text=records[0][2])
            self.Time8.configure(text=records[0][3])

        else:
            pass


        self.conn.close()
        self.EditButton.configure(state="disabled")
        self.DeleteButton.configure(state="disabled")

    def delete_api(self):
        self.curr.execute("""delete from crawled_data_tb where ID= '{}'""".format(self.ID))


    def delete_button_event(self):
        

        self.conn._open_connection()

        

        self.delete_api()


        if self.ID=="1":

            self.ID1.configure(text="")
            self.Clabel1.configure(text="")
            self.Rate1.configure(text="")
            self.Time1.configure(text="")
        
        elif self.ID=="2":

            self.ID2.configure(text="")
            self.Clabel2.configure(text="")
            self.Rate2.configure(text="")
            self.Time2.configure(text="")

        elif self.ID=="3":
            
            self.ID3.configure(text="")
            self.Clabel3.configure(text="")
            self.Rate3.configure(text="")
            self.Time3.configure(text="")
        
        elif self.ID=="4":

            self.ID4.configure(text="")
            self.Clabel4.configure(text="")
            self.Rate4.configure(text="")
            self.Time4.configure(text="")
        
        elif self.ID=="5":

            self.ID5.configure(text="")
            self.Clabel5.configure(text="")
            self.Rate5.configure(text="")
            self.Time5.configure(text="")
        
        elif self.ID=="6":

            self.ID6.configure(text="")
            self.Clabel6.configure(text="")
            self.Rate6.configure(text="")
            self.Time6.configure(text="")
        
        elif self.ID=="7":

            self.ID7.configure(text="")
            self.Clabel7.configure(text="")
            self.Rate7.configure(text="")
            self.Time7.configure(text="")
        
        elif self.ID=="8":

            self.ID8.configure(text="")
            self.Clabel8.configure(text="")
            self.Rate8.configure(text="")
            self.Time8.configure(text="")
        
        else:
            pass
        
        
        
        
        self.conn.commit()



        self.conn.close()
        self.AddButton.configure(state="enabled")
        self.EditButton.configure(state="disabled")
        self.DeleteButton.configure(state="disabled")

    def crawl_button_event(self):
        
        
        os.chdir("E:\\VS Code projects\\tgju.org Crawler 2\\CrawlENV")
        os.system("python Crawler.py")

        self.api()
        



        
        self.SelectButton.configure(state="enabled")
        
        
        
        
    
    def api(self):
        
        self.conn._open_connection()
        

        self.curr.execute("""SELECT * FROM currency_rates.crawled_data_tb""")

        # get all records 

        records= self.curr.fetchall()

        self.curr.execute("""DELETE FROM currency_rates.crawled_data_tb WHERE ID='100'""")

        print(records)
        self.conn.close()

        # Row 1
        self.ID1.configure(text=records[0][0])
        self.Clabel1.configure(text=records[0][1])
        self.Rate1.configure(text=records[0][2])
        self.Time1.configure(text=records[0][3])

        # Row 2
        self.ID2.configure(text=records[1][0])
        self.Clabel2.configure(text=records[1][1])
        self.Rate2.configure(text=records[1][2])
        self.Time2.configure(text=records[1][3])

        # Row 3
        self.ID3.configure(text=records[2][0])
        self.Clabel3.configure(text=records[2][1])
        self.Rate3.configure(text=records[2][2])
        self.Time3.configure(text=records[2][3])

        # Row 4
        self.ID4.configure(text=records[3][0])
        self.Clabel4.configure(text=records[3][1])
        self.Rate4.configure(text=records[3][2])
        self.Time4.configure(text=records[3][3])

        # Row 5
        self.ID5.configure(text=records[4][0])
        self.Clabel5.configure(text=records[4][1])
        self.Rate5.configure(text=records[4][2])
        self.Time5.configure(text=records[4][3])

        # Row 6
        self.ID6.configure(text=records[5][0])
        self.Clabel6.configure(text=records[5][1])
        self.Rate6.configure(text=records[5][2])
        self.Time6.configure(text=records[5][3])

        self.Crawled_label.configure(text="Successfully Crawled at: "+ records[6][3])

        

        

        


if __name__ == "__main__":
    app = App()
    app.mainloop()

    
    