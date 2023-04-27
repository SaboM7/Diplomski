    add_predefined_labels(new_window,words)
    add_label_to_window(list_to_check,new_window,48.0)
    add_label_to_window(list_of_finds,new_window,400.0)
    add_label_to_window(list_of_marks,new_window,550.0)
    add_label_to_window(list_of_Cyrilic,new_window,700.0)

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
        text='Linkovi:',
        bd=0,
        anchor="w",
        font=("Inter Light", 20 * -1),
        bg='#454642',
        fg='#447ED5',
        activebackground='#454642',
        activeforeground='white'
    )
    l1.place(
        x=70.0,
        y=70.0,
    )
    l1 = Label(
        new_window,
        text='Nadjeni tekst:',
        bd=0,
        anchor="w",
        font=("Inter Light", 20 * -1),
        bg='#454642',
        fg='#447ED5',
        activebackground='#454642',
        activeforeground='white'
    )
    l1.place(
        x=400.0,
        y=70.0,
    )
    l1 = Label(
        new_window,
        text='Označen tekst:',
        bd=0,
        anchor="w",
        font=("Inter Light", 20 * -1),
        bg='#454642',
        fg='#447ED5',
        activebackground='#454642',
        activeforeground='white'
    )
    l1.place(
        x=550.0,
        y=70.0,
    )
    l1 = Label(
        new_window,
        text='Stranica ima ćirilicu:',
        bd=0,
        anchor="w",
        font=("Inter Light", 20 * -1),
        bg='#454642',
        fg='#447ED5',
        activebackground='#454642',
        activeforeground='white'
    )
    l1.place(
        x=700.0,
        y=70.0,
    )

def add_label_to_window(list_to_check:list,new_window,x_value:float):
    for index,link in enumerate(list_to_check,0):
        if type(link) == bool:
            if link:
                text= "Da"
            else:
                text = "Ne"
        else:
            text = str(index + 1) + ". " + str(link)
        l1 = Label(
            new_window,
            text=text,
            bd=0,
            anchor="w",
            font=("Inter Light", 20 * -1),
            bg='#454642',
            fg='white',
            activebackground='#454642',
            activeforeground='white'
        )
        l1.place(
            x=x_value,
            y=100.0+ float(index)*30,
        )