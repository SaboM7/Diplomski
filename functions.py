from urllib.request import urlopen
from urllib.request import Request
import cyrtranslit
import regex
from datetime import datetime
import webbrowser
import os
from pathlib import Path
import tksheet
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, Checkbutton, IntVar, Toplevel, Label, messagebox

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"D:\Skola\Diplomski\gui\build\assets\frame0")


def bool_to_text(value: bool):
    """
    Turning boolean values into text for display.
    :param value: Value to display
    :return: Text to display
    """
    if value:
        text = "Da"
    else:
        text = "Ne"
    return text


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


def check_page(url: str, words: str, temp_number: int, path_list: list):
    """
    Checks page if it contains string, then it tries to mark string in html and saves it to temp.
    :param url: URL that you want to search on
    :param words: string that you search
    :param temp_number: number of temp file
    :param path_list: list of paths to save path on
    :return: Result if string is found and if the page has marked words and if page has Cyrillic characters
    """
    match = True
    # link_list.append(url)                                               #??
    req = Request(url, headers={'User-Agent': "Magic Browser"})
    html_contents = urlopen(req).read()
    string_byte_decoded = html_contents.decode("UTF-8")                 # decoding html page

    if regex.search(r'\p{IsCyrillic}', words) is not None:
        temp_words = cyrtranslit.to_latin(words)                            # convert words to latin if cyr
    else:
        temp_words = cyrtranslit.to_cyrillic(words)                         # convert words to cyr if latin
    cyr_flag = regex.search(r'\p{IsCyrillic}', string_byte_decoded) is not None

    if string_byte_decoded.lower().find(" "+words.lower()) >= 0:     # checking if words exist in text
        marked = encoding_saving_marking(string_byte_decoded, words, path_list, temp_number)
        return match, marked, cyr_flag
    elif string_byte_decoded.lower().find(" "+temp_words.lower()) >= 0:
        marked = encoding_saving_marking(string_byte_decoded, temp_words, path_list, temp_number)
        return match, marked, cyr_flag
    else:
        match = False
        marked = False
        path_list.append(save_to_temp(html_contents, temp_number))
        return match, marked, cyr_flag


def encoding_saving_marking(string_to_encode_: str, words: str, path_list: list, temp_number: int):
    """
    Reduces code repetition in my functions.
    :param string_to_encode_: String to encode
    :param words: String to mark
    :param path_list: List of paths to temp pages
    :param temp_number: Number of temp page
    :return: True if words are marked, false if not
    """
    marked = True
    string_to_encode = mark_string(string_to_encode_, words)
    if string_to_encode == string_to_encode_:
        marked = False                                          # checking if it is really marked and saving value
    html_contents = string_to_encode.encode()
    path_list.append(save_to_temp(html_contents, temp_number))  # saving html page to temp and saving path
    return marked


def open_file_update_list(list_of_links: list):
    """
    Updates list of links to search from.
    :param list_of_links: List to update.
    :return: Nothing.
    """
    path = Path(__file__).parent / "links.txt"
    try:
        open(path, "x")                                     # creating file if it doesnt exist
    except FileExistsError:
        pass
    finally:
        f = open(path, "r+")
        for link in f:
            list_of_links.append(link)
        f.close()


def save_links(list_of_links):
    """
    Saves links to txt file.
    :param list_of_links: List that gets saved to file.
    :return: Nothing.
    """
    path = Path(__file__).parent / "links.txt"
    try:
        open(path, "x")                         # creating txt file to save links to
    except FileExistsError:
        pass
    finally:
        f = open(path, "w")
        for link in list_of_links:
            if not link.endswith("\n"):
                link = link + "\n"
            f.write(link)
        f.close()


def check_if_selected_chbox(link_dict: dict, selected: dict):
    """
    Checking which checkboxes are selected
    :param link_dict: Dictionary of links and their titles
    :param selected: Dictionary to check which button is selected
    :return: List of links to search from
    """
    list_to_search = []
    for paper in link_dict.keys():
        if selected[paper].get():                          # if checkbox is selected
            list_to_search.append(link_dict[paper])
    return list_to_search


def load_links(entry):
    """
    Loads links from text file into the textfield
    :param entry: Entry (textfield) to put links in
    :return: None
    """
    link_list_for_textarea = []
    open_file_update_list(link_list_for_textarea)                   # function to put links from file to list
    for index, link in enumerate(link_list_for_textarea, 1):        # putting links in textfield
        entry.insert(str(index) + ".0", link)


def get_links_from_textfield(entry, list_of_links: list):
    """
    Getting lines from textfield and putting them in list
    :param entry: Textfield to load lines from
    :param list_of_links: List to put the links in
    :return: None
    """
    for link in entry.get("1.0", "end").splitlines():               # getting whole text in textfield and then splitting it in lines
        if link != "" and link not in list_of_links:
            list_of_links.append(link)


def search_sites(link_dict: dict, selected: dict, textfield, textbox, main_window):
    """
    Function that searches the words from textbox in the links from textbox or selected checkboxes
    :return: None
    """
    list_to_check = check_if_selected_chbox(link_dict, selected)              # making a list of links to check from checkboxes
    get_links_from_textfield(textfield, list_to_check)                         # adding links from textfield to list to check
    words = textbox.get()                                                   # getting the words to search for
    if words != "" and len(list_to_check) > 0:                               # if there is a word/s and is a link start searching
        checking_links_making_window(list_to_check, words, main_window)


def checking_links_making_window(list_to_check: list, words: str, main_window):
    """
    Searches and marks words if found in the links provided in the list
    :param list_to_check: List of links from which to search for words
    :param words: Words to search for
    :param main_window: Main window to attach the new window with results
    :return: None
    """
    start_time = getting_time()
    # initializing lists to be used
    list_of_paths = []                                                # list to store paths from downloaded pages
    list_of_finds = []                                                # list to store if search is successful
    list_of_marks = []                                                # list to store if the searched word is marked in downloaded page
    list_of_Cyrilic = []                                              # list to store if the page has some Cyrillic characters
    list_of_lists = [list_to_check, list_of_finds, list_of_marks, list_of_Cyrilic]  # list of all lists that is used to make a sheet

    for i, link in enumerate(list_to_check, 0):
        found, marked, isCyrilic = check_page(link, words, i, list_of_paths)            # checking each page
        # adding values to lists
        list_of_finds.append(bool_to_text(found))
        list_of_marks.append(bool_to_text(marked))
        list_of_Cyrilic.append(bool_to_text(isCyrilic))

    # making new window to display results of search
    new_window = Toplevel(
        main_window,
        bg="#444642",
        height=511,
        width=1058,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )
    new_window.title("Rezultat")
    sheet = tksheet.Sheet(new_window, width=580)
    sheet.set_sheet_data([[item[index] for item in list_of_lists] for index in range(len(list_to_check))])  # putting values from lists into the sheet row by row
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
    sheet.highlight_columns(1, "yellow", "red")                     # highlighting the column with the result if words are found
    sheet.place(
        x=48.0,
        y=100.0,
        height=45 + len(list_to_check) * 24.0,
        width=580.0
    )
    add_predefined_labels(new_window, words, start_time)             # adding labels that are necessary to window
    add_buttons_to_window(list_of_paths, new_window, 640.0)         # adding buttons for opening downloaded pages
    add_buttons_to_window(list_to_check, new_window, 820.0)         # adding buttons for opening pages on web


def add_buttons_to_window(list_to_make_buttons: list, master_window, x_position: float):
    """
    Makes buttons and places them to window from a list of links
    :param list_to_make_buttons: List of links from which buttons are made
    :param master_window:
    :param x_position: X to place the buttons to
    :return: None
    """
    for index, link in enumerate(list_to_make_buttons, 0):
        button_temp = Button(
            text="Otvori",
            master=master_window,
            borderwidth=0,
            highlightthickness=0,
            command=lambda link=link: webbrowser.open(link),         # command is opening link in default web browser
            relief="flat"
        )
        button_temp.place(
            x=x_position,
            y=125.0 + index * 23.0,                                 # placing the button one below other
            width=100.0,
            height=20.0
        )


def add_predefined_labels(new_window, words: str, start_time: str):
    """
    Adds labels to window
    :param new_window:
    :param words:
    :param start_time: Time that searching started to put in label
    :return:
    """
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
    l1 = Label(
        new_window,
        text='Pretraženo ' + start_time,
        bd=0,
        anchor="w",
        font=("Inter Light", 15 * -1),
        bg='#454642',
        fg='white',
        activebackground='#454642',
        activeforeground='white'
    )
    l1.place(
        x=640.0,
        y=20.0,
    )


def making_checkboxes(link_dict: dict, selected: dict):
    """
    Makes checkboxes from dict of links and putting values in selected dict
    :param link_dict: Dictionary of links and their titles
    :param selected: Dictionary to put the selected values in
    :return: None
    """
    for index, paper in enumerate(link_dict.keys()):
        selected[paper] = IntVar()                      # making variable to store checkbutton value
        check = Checkbutton(
            text=paper,                                 # setting title of link to be display on checkbutton
            variable=selected[paper],                   # setting the variable to be value of title key
            bd=0,
            anchor="w",
            font=("Inter Light", 20 * -1),
            bg='#454642',
            fg='white',
            activebackground='#454642',
            activeforeground='white',
            selectcolor="#454642")
        check.place(
            x=70.0,
            y=210.0 + index * 30.0,
            width=100.0,
            height=30.0)


def getting_time():
    """
    Getting formatted string of time.
    :return: String containing time.
    """
    now = datetime.now()
    # dd/mm/YY H:M:S
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")               # formatting
    return dt_string


def save_to_temp(html_contents: bytes, temp_num):
    """
    Saving html page in bytes to temp file.
    :param html_contents: Html page in bytes.
    :param temp_num: Number of temp file.
    :return: Path to them file that page is saved to.
    """
    path = Path(__file__).parent
    try:
        os.mkdir(path/"tmp")                                     # making temp directory if it doesnt exist
    except FileExistsError:
        pass
    finally:
        os.chdir(path/"tmp")
        file_path = os.path.abspath(f"temp{temp_num}.html")      # creating path
        os.chdir("..")
        with open(file_path, 'wb') as f:                         # opening file
            f.write(html_contents)                          # saving page to file
        return file_path


def mark_string(string_for_marking: str, words: str):
    """
    Marking string in html page.
    :param string_for_marking:
    :param words: String to mark.
    :return: Marked string.
    """
    string_for_return = string_for_marking.replace(" " + words + " ", f" <mark>{words}</mark> ")  # marking words
    string_for_return = string_for_return.replace(" " + words.capitalize() + " ", f" <mark>{words.capitalize()}</mark> ")
    string_for_return = string_for_return.replace(" " + words.lower() + " ", f" <mark>{words.lower()}</mark> ")
    string_for_return = string_for_return.replace(" " + words.upper() + " ", f" <mark>{words.upper()}</mark> ")
    return string_for_return


def on_closing(window, textfield):
    """
    Function that is called on trying to close the main window
    :param window: Window to be closed
    :param textfield: Text field to take links from
    :return: None
    """
    if messagebox.askokcancel("Izlaz", "Da li želite da izadjete?"):  # asking are you sure to quit
        list_to_save = []
        get_links_from_textfield(textfield, list_to_save)                # loading links from text filed to save
        save_links(list_to_save)                                      # saving links to text file
        window.destroy()                                              # closing window
