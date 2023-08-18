from functions import *


# making base window
window = Tk()
window.title("Pretraži stranice")
window.geometry("1058x511")
window.configure(bg="#444642")

# adding canvas
canvas = Canvas(
    window,
    bg="#444642",
    height=511,
    width=1058,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)

canvas.place(x=0, y=0)
canvas.create_text(
    300.0,
    31.0,
    anchor="nw",
    text="Pretraživanje Web stranica",
    fill="#FFFFFF",
    font=("Inter Black", 32 * -1)
)

# adding image for text box for searched word
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
    font=("Inter Light", 20 * -1)
)
entry_1.place(
    x=73.0,
    y=126.0,
    width=284.0,
    height=32.0
)
# adding label
canvas.create_text(
    70.0,
    180.0,
    anchor="nw",
    text="Izaberite dnevni list (Opciono):",
    fill="#FFFFFF",
    font=("Inter Black", 16 * -1)
)


link_dict = {"Blic": "https://www.blic.rs/", "Alo": "https://www.alo.rs/", "Danas": "https://www.danas.rs/",     # dict of default links with titles
             "Nova": "https://nova.rs/", "N1": "https://n1info.rs/", "Politika": "https://www.politika.rs/scc"}
selected = {}                                                                                                   # dict to save checkbox values
making_checkboxes(link_dict, selected)                           # making checkboxes of default links


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

# TextField
entry_image_2 = PhotoImage(
    file=relative_to_assets("entry_2.png"))
entry_bg_2 = canvas.create_image(
    774.0,
    289.0,
    image=entry_image_2
)
entry_2 = Text(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0,
    font=("Inter Light", 18 * -1)
)

load_links(entry_2)                         # loading links into text field

entry_2.place(
    x=556.0,
    y=174.0,
    width=436.0,
    height=228.0
)


# Pretraži
# button for search
button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: search_sites(link_dict, selected, entry_2, entry_1, window),
    relief="flat"
)
button_1.place(
    x=556.0,
    y=92.0,
    width=137.0,
    height=42.0
)

# Učitaj linkove
# button for loading links
button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: load_links(entry_2),    # dugme za linkove
    relief="flat"
)
button_2.place(
    x=556.0,
    y=424.0,
    width=115.0,
    height=32.0
)

window.protocol("WM_DELETE_WINDOW", lambda: on_closing(window, entry_2))      # setting function when closing window
window.resizable(False, False)
window.mainloop()
