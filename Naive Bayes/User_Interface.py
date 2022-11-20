import tkinter
from Model import Model,Reader
from tkinter import font, filedialog, INSERT


class UserInterface(tkinter.Tk):
    def __init__(self, title="Naïve Bayes_model"):
        super().__init__()
        self.model = None
        self.title(title)
        self.geometry("800x220")
        self.welcome_frame= tkinter.Frame(master=self)
        self.input_frame = tkinter.Frame(master=self)
        self.welcome_label=tkinter.Label(master=self.welcome_frame, text="welcome to the best data analyzer\nplease browse the file to create the model", font=font.Font(size=20))
        self.text_box=tkinter.Text(master=self.welcome_frame,name="please",height=1)
        self.browse_button=tkinter.Button(master=self.welcome_frame,text="Browse",command=lambda: self.browseFiles())
        self.model_status_label=tkinter.Label(master=self.welcome_frame, text="The model built successfully", fg ="green",font=font.Font(size=12))
        self.selection_box_label = tkinter.Label(master=self.input_frame, text="select from the list your input type")
        self.selection_box=tkinter.Listbox(master=self.input_frame, height=1, listvariable=tkinter.Variable(value=("list", "file")))
        self.selection_box.bind('<<ListboxSelect>>', self.get_selected)
        self.browse_button_input = tkinter.Button(master=self.input_frame, text="Browse_newfile",command=lambda: self.browseFiles2())
        self.data_list_as_text = tkinter.Text(master=self.input_frame, name="data with comma", height=1)
        self.commit_text = tkinter.Button(master=self.input_frame, text="commit", command=lambda: self.retrieve_input())
        self.output_label = tkinter.Label(master=self.input_frame, text="out put",font=font.Font(size=15))
        self.welcome_label.grid(row=1,column=1)
        self.text_box.grid(row=2,column=1,pady=5,padx=5,)
        self.browse_button.grid(row=2,column=2)
        self.welcome_frame.pack()
        self.input_frame.pack()
        self.mainloop()

    def create_frame(self):
        return tkinter.Frame(master=self)

    def pak_frame(self,frame):
        frame.pack()


    def browseFiles(self):
        filename = filedialog.askopenfilename(initialdir=".",
                                              title="Select your CSV File",
                                              filetypes=(("CSV files",
                                                          "*.csv"),
                                                         ("all files",
                                                          "*.*")))
        self.text_box.insert(INSERT, filename)
        csv_data_reader = Reader(filename)
        dat_list = csv_data_reader.get_data_as_list()
        columns_count = csv_data_reader.get_number_of_columns()
        self.model =Model(dat_list, columns_count)
        self.model_status_label.grid(row=3,column=1)
        self.selection_box_label.grid(row=4,column=1,pady=10)
        self.selection_box.grid(row=4,column=2)


    def get_selected(self,event):
        selected=self.selection_box.curselection()
        if selected[0] == 0:
            print("list")
            self.browse_button_input.grid_remove()
            self.output_label.grid_remove()
            self.data_list_as_text.grid(row=5,column=1)
            self.commit_text.grid(row=5,column=2)
        else:
            print("file")
            self.data_list_as_text.grid_remove()
            self.commit_text.grid_remove()
            self.output_label.grid_remove()
            self.browse_button_input.grid(row=4,column=3)


    def browseFiles2(self):
        filename1 = filedialog.askopenfilename(initialdir=".",
                                              title="Select your CSV File",
                                              filetypes=(("CSV files",
                                                          "*.csv"),
                                                         ("all files",
                                                          "*.*")))
        #self.text_box.insert(INSERT, filename1)
        text1=f"The accuracy percentage of the model : {self.model.get_correctness(filename1)}"
        self.output_label.config(text=text1)
        self.output_label.grid(row=6, column=1)

    def retrieve_input(self):
        inputValue=self.data_list_as_text.get("1.0","end-1c")
        text1=f"The expected value is : {self.model.get_expected_answer(inputValue.split(','))}"
        self.output_label.config(text=text1)
        self.output_label.grid(row=6, column=1)


a= UserInterface()
