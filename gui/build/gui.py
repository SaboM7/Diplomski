
# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer

from functions import *
# from pathlib import Path
#
# # from tkinter import *
# # Explicit imports to satisfy Flake8
# import tksheet
# from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, Checkbutton, IntVar, Toplevel, Label


# OUTPUT_PATH = Path(__file__).parent
# ASSETS_PATH = OUTPUT_PATH / Path(r"D:\Skola\Diplomski\gui\build\assets\frame0")



window = Tk()
window.title("Pretraži stranice")
window.geometry("1058x511")
window.configure(bg = "#444642")

canvas = Canvas(
    window,
    bg = "#444642",
    height = 511,
    width = 1058,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
canvas.create_text(
    300.0,
    31.0,
    anchor="nw",
    text="Pretraživanje Web stranica",
    fill="#FFFFFF",
    font=("Inter Black", 32 * -1)
)

entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    215.0,
    143.0,
    image=entry_image_1
)
# Textbox
entry_1 = Entry(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0,
    font = ("Inter Light", 20 * -1)
)
entry_1.place(
    x=73.0,
    y=126.0,
    width=284.0,
    height=32.0
)
canvas.create_text(
    70.0,
    180.0,
    anchor="nw",
    text="Izaberite dnevni list (Opciono):",
    fill="#FFFFFF",
    font=("Inter Black", 16 * -1)
)


def making_checkboxes(link_dict : dict,selected : dict):
    for index, paper in enumerate(link_dict.keys()):
        selected[paper] = IntVar()
        l = Checkbutton(
            text=paper,
            variable=selected[paper],
            bd=0,
            anchor="w",
            font=("Inter Light", 20 * -1),
            bg='#454642',
            fg='white',
            activebackground='#454642',
            activeforeground='white',
            selectcolor="#454642")
        l.place(
            x=70.0,
            y=210.0 + index * 30.0,
            width=100.0,
            height=30.0)


link_dict = {"Blic":"https://www.blic.rs/","Alo": "https://www.alo.rs/", "Danas": "https://www.danas.rs/" ,
             "Nova": "https://nova.rs/", "N1":"https://n1info.rs/","Politika":"https://www.politika.rs/scc"}
selected = {}
making_checkboxes(link_dict,selected)


def check_if_selected_chbox(link_dict:dict,selected : dict):
    list_to_search = []
    for paper in link_dict.keys():
        if selected[paper].get() :
            list_to_search.append(link_dict[paper])
    return list_to_search

def load_links(entry):
    link_list_for_textarea = []
    open_file_update_list(link_list_for_textarea)
    for index, link in enumerate(link_list_for_textarea, 1):
        entry.insert(str(index) + ".0", link)

canvas.create_text(
    73.0,
    92.0,
    anchor="nw",
    text="Unesite tekst za pretragu :",
    fill="#FFFFFF",
    font=("Inter Light", 20 * -1)
)

canvas.create_text(
    556.0,
    147.0,
    anchor="nw",
    text="Unesite linkove za pretragu :",
    fill="#FFFFFF",
    font=("Inter Light", 20 * -1)
)

canvas.create_text(
    775.0,
    404.0,
    anchor="nw",
    text="*linkovi moraju biti jedan ispod drugog",
    fill="#FFFFFF",
    font=("Inter Light", 13 * -1)
)

entry_image_2 = PhotoImage(
    file=relative_to_assets("entry_2.png"))
entry_bg_2 = canvas.create_image(
    774.0,
    289.0,
    image=entry_image_2
)
# TextField
entry_2 = Text(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0,
    font = ("Inter Light", 18 * -1)
)

load_links(entry_2)                         # loading links into text field

entry_2.place(
    x=556.0,
    y=174.0,
    width=436.0,
    height=228.0
)

def get_links_from_textfield(entry,list_of_links:list):
    for link in entry.get("1.0", "end").splitlines():
        if link != ""  and link not in list_of_links:
            list_of_links.append(link)

def search_sites():
    list_to_check= check_if_selected_chbox(link_dict,selected)
    get_links_from_textfield(entry_2,list_to_check)
    # for link in entry_2.get("1.0", "end").splitlines():
    #     if link != ""  and link not in list_to_check:
    #         list_to_check.append(link)
    words = entry_1.get()
    if words != "" and len(list_to_check)>0 :
        checking_links_making_window(list_to_check,words)


def checking_links_making_window(list_to_check:list,words:str):
    list_of_paths = []
    list_of_finds = []
    list_of_marks = []
    list_of_Cyrilic = []
    list_of_lists = [list_to_check, list_of_finds, list_of_marks, list_of_Cyrilic]
    for i, link in enumerate(list_to_check, 0):
        found, marked, isCyrilic = check_page(link, words, i, list_of_paths)
        list_of_finds.append(bool_to_text(found))
        list_of_marks.append(bool_to_text(marked))
        list_of_Cyrilic.append(bool_to_text(isCyrilic))
    new_window = Toplevel(
        window,
        bg="#444642",
        height=511,
        width=1058,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )
    new_window.title("Rezultat")
    sheet = tksheet.Sheet(new_window, width=580)
    sheet.set_sheet_data([[item[index] for item in list_of_lists] for index in range(len(list_to_check))])
    sheet.column_width(column=0, width=200)
    sheet.column_width(column=1, width=100)
    sheet.column_width(column=2, width=100)
    sheet.column_width(column=3, width=130)
    sheet.headers(["Linkovi", "Postoji tekst", "Označen tekst", "Stranica ima ćirilicu"])
    sheet.enable_bindings(
        (
            "single_select",
            "row_select",
            "column_width_resize",
            "arrowkeys",
            "right_click_popup_menu",
            "rc_select",
            "copy",
            "cut",
            "paste"
        )
    )
    sheet.highlight_columns(1, "yellow", "red")
    sheet.place(
        x=48.0,
        y=100.0,
        height=45 + len(list_to_check) * 24.0,
        width=580.0
    )
    add_predefined_labels(new_window, words)
    add_buttons_to_window(list_of_paths, new_window, 640.0)
    add_buttons_to_window(list_to_check, new_window, 820.0)


def add_buttons_to_window(list_to_make_buttons: list,master_window,x_position: float):
    for index, link in enumerate(list_to_make_buttons,0):
        button_temp = Button(
            text="Otvori",
            master=master_window,
            borderwidth=0,
            highlightthickness=0,
            command=lambda link=link: webbrowser.open(link),
            relief="flat"
        )
        button_temp.place(
            x=x_position,
            y=125.0 + index * 23.0,
            width=100.0,
            height=20.0
        )

def add_predefined_labels(new_window,words):
    l1 = Label(
        new_window,
        text='Traženi tekst: ' + words,
        bd=0,
        anchor="w",
        font=("Inter Light", 25 * -1),
        bg='#454642',
        fg='yellow',
        activebackground='#454642',
        activeforeground='white'
    )
    l1.place(
        x=70.0,
        y=30.0,
    )
    l1 = Label(
        new_window,
        text='Otvori skinutu stranicu: ',
        bd=0,
        anchor="w",
        font=("Inter Light", 15 * -1),
        bg='#454642',
        fg='orange',
        activebackground='#454642',
        activeforeground='white'
    )
    l1.place(
        x=640.0,
        y=70.0,
    )
    l1 = Label(
        new_window,
        text='Otvori stranicu sa interneta: ',
        bd=0,
        anchor="w",
        font=("Inter Light", 15 * -1),
        bg='#454642',
        fg='green',
        activebackground='#454642',
        activeforeground='white'
    )
    l1.place(
        x=820.0,
        y=70.0,
    )


# Pretraži
button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=search_sites,                       # dodati moju funkciju za check_page
    relief="flat"
)
button_1.place(
    x=556.0,
    y=92.0,
    width=137.0,
    height=42.0
)
# Učitaj linkove
button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command= lambda : load_links(entry_2),    # dugme za linkove
    relief="flat"
)
button_2.place(
    x=556.0,
    y=424.0,
    width=115.0,
    height=32.0
)
def on_closing(window):
    if messagebox.askokcancel("Izlaz", "Da li želite da izadjete?"):
        list_to_save = []
        get_links_from_textfield(entry_2,list_to_save)
        save_links(list_to_save)
        window.destroy()

window.protocol("WM_DELETE_WINDOW", lambda : on_closing(window))
window.resizable(False, False)
window.mainloop()
