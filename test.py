from tksheet import Sheet
import tkinter as tk


class demo(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.grid_columnconfigure(0, weight = 1)
        self.grid_rowconfigure(0, weight = 1)
        self.frame = tk.Frame(self)
        self.frame.grid_columnconfigure(0, weight = 1)
        self.frame.grid_rowconfigure(0, weight = 1)
        self.sheet = Sheet(self.frame,
                           data = [[f"Row {r}, Column {c}\nnewline1\nnewline2" for c in range(30)] for r in range(2000)], #to set sheet data at startup
                           headers = [f"Column {c}\nnewline1\nnewline2" for c in range(30)],
                            )
        self.sheet.enable_bindings(("single_select", #"single_select" or "toggle_select"
                                     "drag_select",   #enables shift click selection as well
                                    "rc_select",
                                    "row_select",
                                    "column_select",
                                     "arrowkeys",
                                     "row_height_resize",
                                     "double_click_row_resize",
                                     "copy",
                                     "cut",
                                     "paste",
                                     "delete",
                                     "undo",
                                     "edit_cell"))
        self.frame.grid(row = 0, column = 0, sticky = "nswe")
        self.sheet.grid(row = 0, column = 0, sticky = "nswe")
        self.del_rows_button = tk.Button(self,
                                         text = "Delete Rows",
                                         command = self.del_rows)
        self.del_rows_button.grid(row = 1, column = 0)
        self.new_rc_popup_menu = tk.Menu(self, tearoff = 0, background = "white")
        self.new_rc_popup_menu.add_command(label = "Delete Rows",
                                             font = ("Arial", 13, "normal"),
                                             foreground = "gray10",
                                             background = "white",
                                             activebackground = "gray90",
                                             activeforeground = "gray5",
                                             command = self.del_rows)
        #self.sheet.bind("<3>", self.rc) #use "<2>" if on Mac OS this is in case you need your own right click binding

    def rc(self, event):
        self.new_rc_popup_menu.tk_popup(event.x_root, event.y_root)

    def del_rows(self, event = None):
        selected_rows = self.sheet.get_selected_rows()
        if selected_rows:
            start = min(selected_rows)
            end = max(selected_rows) + 1
            self.sheet.MT.data_ref[start:end] = []
            index = self.sheet.row_index()
            if index:
                try:
                    index[start:end] = []
                    self.sheet.row_index(index)
                except:
                    pass
            self.sheet.deselect("all")
            self.sheet.refresh()


app = demo()
app.mainloop()