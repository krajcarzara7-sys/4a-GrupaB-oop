# ============================================
# TOP 10 FILMOVA PO ŽANRU
# GUI aplikacija u Pythonu (Tkinter)
# ============================================

import tkinter as tk
from tkinter import ttk, messagebox


# ------------------------------------------------
# PODACI O FILMOVIMA
# ------------------------------------------------
filmovi = {

    "Akcija": [
        {"naziv": "The Dark Knight", "ocjena": 9.0, "godina": 2008},
        {"naziv": "Inception", "ocjena": 8.8, "godina": 2010},
        {"naziv": "Gladiator", "ocjena": 8.5, "godina": 2000},
        {"naziv": "The Matrix", "ocjena": 8.7, "godina": 1999},
        {"naziv": "John Wick", "ocjena": 7.4, "godina": 2014},
        {"naziv": "Mad Max: Fury Road", "ocjena": 8.1, "godina": 2015},
        {"naziv": "Die Hard", "ocjena": 8.2, "godina": 1988},
        {"naziv": "Casino Royale", "ocjena": 8.0, "godina": 2006},
        {"naziv": "Avengers: Endgame", "ocjena": 8.4, "godina": 2019},
        {"naziv": "Terminator 2", "ocjena": 8.6, "godina": 1991}
    ],

    "Komedija": [
        {"naziv": "The Hangover", "ocjena": 7.7, "godina": 2009},
        {"naziv": "Home Alone", "ocjena": 7.7, "godina": 1990},
        {"naziv": "Superbad", "ocjena": 7.6, "godina": 2007},
        {"naziv": "Deadpool", "ocjena": 8.0, "godina": 2016},
        {"naziv": "Rush Hour", "ocjena": 7.0, "godina": 1998},
        {"naziv": "Ted", "ocjena": 6.9, "godina": 2012},
        {"naziv": "The Mask", "ocjena": 6.9, "godina": 1994},
        {"naziv": "21 Jump Street", "ocjena": 7.2, "godina": 2012},
        {"naziv": "Dumb and Dumber", "ocjena": 7.3, "godina": 1994},
        {"naziv": "Step Brothers", "ocjena": 6.9, "godina": 2008}
    ],

    "Horor": [
        {"naziv": "The Conjuring", "ocjena": 7.5, "godina": 2013},
        {"naziv": "It", "ocjena": 7.3, "godina": 2017},
        {"naziv": "Hereditary", "ocjena": 7.3, "godina": 2018},
        {"naziv": "The Exorcist", "ocjena": 8.1, "godina": 1973},
        {"naziv": "Get Out", "ocjena": 7.8, "godina": 2017},
        {"naziv": "Saw", "ocjena": 7.6, "godina": 2004},
        {"naziv": "Halloween", "ocjena": 7.7, "godina": 1978},
        {"naziv": "Insidious", "ocjena": 6.8, "godina": 2010},
        {"naziv": "A Quiet Place", "ocjena": 7.5, "godina": 2018},
        {"naziv": "The Ring", "ocjena": 7.1, "godina": 2002}
    ],

    "Drama": [
        {"naziv": "The Shawshank Redemption", "ocjena": 9.3, "godina": 1994},
        {"naziv": "Forrest Gump", "ocjena": 8.8, "godina": 1994},
        {"naziv": "Fight Club", "ocjena": 8.8, "godina": 1999},
        {"naziv": "Interstellar", "ocjena": 8.7, "godina": 2014},
        {"naziv": "Whiplash", "ocjena": 8.5, "godina": 2014},
        {"naziv": "Parasite", "ocjena": 8.5, "godina": 2019},
        {"naziv": "The Green Mile", "ocjena": 8.6, "godina": 1999},
        {"naziv": "Joker", "ocjena": 8.4, "godina": 2019},
        {"naziv": "Titanic", "ocjena": 7.9, "godina": 1997},
        {"naziv": "The Pianist", "ocjena": 8.5, "godina": 2002}
    ]
}


# ------------------------------------------------
# PRIKAZ FILMOVA
# ------------------------------------------------
def prikazi_filmove(event=None):

    lista_filmova.delete(*lista_filmova.get_children())

    zanr = combo_zanr.get()

    if zanr in filmovi:

        sortirani = sorted(
            filmovi[zanr],
            key=lambda x: x["ocjena"],
            reverse=True
        )

        for film in sortirani:

            lista_filmova.insert(
                "",
                tk.END,
                values=(
                    film["naziv"],
                    film["ocjena"],
                    film["godina"]
                )
            )


# ------------------------------------------------
# PRETRAGA FILMA
# ------------------------------------------------
def pretrazi_film():

    trazeni = entry_pretraga.get().lower()

    lista_filmova.delete(*lista_filmova.get_children())

    for zanr in filmovi:
        for film in filmovi[zanr]:

            if trazeni in film["naziv"].lower():

                lista_filmova.insert(
                    "",
                    tk.END,
                    values=(
                        film["naziv"],
                        film["ocjena"],
                        film["godina"]
                    )
                )


# ------------------------------------------------
# DODAVANJE FILMA
# ------------------------------------------------
def dodaj_film():

    naziv = entry_naziv.get()
    ocjena = entry_ocjena.get()
    godina = entry_godina.get()
    zanr = combo_dodaj_zanr.get()

    if naziv == "" or ocjena == "" or godina == "":
        messagebox.showwarning(
            "Greška",
            "Popuni sva polja!"
        )
        return

    try:

        novi_film = {
            "naziv": naziv,
            "ocjena": float(ocjena),
            "godina": int(godina)
        }

        filmovi[zanr].append(novi_film)

        messagebox.showinfo(
            "Uspjeh",
            f"Film '{naziv}' dodan je u žanr '{zanr}'!"
        )

        # Brisanje unosa
        entry_naziv.delete(0, tk.END)
        entry_ocjena.delete(0, tk.END)
        entry_godina.delete(0, tk.END)

        prikazi_filmove()

    except:

        messagebox.showerror(
            "Greška",
            "Ocjena mora biti broj!"
        )


# ------------------------------------------------
# GLAVNI PROZOR
# ------------------------------------------------
root = tk.Tk()

root.title("Top Filmovi")
root.geometry("900x700")
root.configure(bg="#dff6ff")


# ------------------------------------------------
# NASLOV
# ------------------------------------------------
naslov = tk.Label(
    root,
    text="TOP 10 FILMOVA PO ŽANRU",
    font=("Arial", 24, "bold"),
    bg="#dff6ff",
    fg="#003049"
)

naslov.pack(pady=20)


# ------------------------------------------------
# ODABIR ŽANRA
# ------------------------------------------------
frame_zanr = tk.Frame(root, bg="#dff6ff")
frame_zanr.pack()

label_zanr = tk.Label(
    frame_zanr,
    text="Odaberi žanr:",
    font=("Arial", 12),
    bg="#dff6ff"
)

label_zanr.pack(side=tk.LEFT, padx=5)

combo_zanr = ttk.Combobox(
    frame_zanr,
    values=list(filmovi.keys()),
    state="readonly",
    width=25
)

combo_zanr.pack(side=tk.LEFT)
combo_zanr.bind("<<ComboboxSelected>>", prikazi_filmove)


# ------------------------------------------------
# PRETRAGA
# ------------------------------------------------
frame_pretraga = tk.Frame(root, bg="#dff6ff")
frame_pretraga.pack(pady=15)

entry_pretraga = tk.Entry(
    frame_pretraga,
    width=30,
    font=("Arial", 12)
)

entry_pretraga.pack(side=tk.LEFT, padx=5)

btn_pretraga = tk.Button(
    frame_pretraga,
    text="Pretraži",
    command=pretrazi_film,
    bg="#38b000",
    fg="white",
    font=("Arial", 10, "bold")
)

btn_pretraga.pack(side=tk.LEFT)


# ------------------------------------------------
# TABLICA FILMOVA
# ------------------------------------------------
kolone = ("Naziv", "Ocjena", "Godina")

lista_filmova = ttk.Treeview(
    root,
    columns=kolone,
    show="headings",
    height=15
)

for kolona in kolone:
    lista_filmova.heading(kolona, text=kolona)
    lista_filmova.column(kolona, width=250)

lista_filmova.pack(pady=20)


# ------------------------------------------------
# DODAVANJE FILMOVA
# ------------------------------------------------
frame_dodavanje = tk.LabelFrame(
    root,
    text="Dodaj novi film",
    padx=15,
    pady=15,
    bg="#caf0f8",
    font=("Arial", 12, "bold")
)

frame_dodavanje.pack(pady=20)


# Naziv
tk.Label(
    frame_dodavanje,
    text="Naziv:",
    bg="#caf0f8"
).grid(row=0, column=0, padx=5, pady=5)

entry_naziv = tk.Entry(frame_dodavanje, width=25)
entry_naziv.grid(row=0, column=1)


# Ocjena
tk.Label(
    frame_dodavanje,
    text="Ocjena:",
    bg="#caf0f8"
).grid(row=1, column=0, padx=5, pady=5)

entry_ocjena = tk.Entry(frame_dodavanje, width=25)
entry_ocjena.grid(row=1, column=1)


# Godina
tk.Label(
    frame_dodavanje,
    text="Godina:",
    bg="#caf0f8"
).grid(row=2, column=0, padx=5, pady=5)

entry_godina = tk.Entry(frame_dodavanje, width=25)
entry_godina.grid(row=2, column=1)


# Žanr
tk.Label(
    frame_dodavanje,
    text="Žanr:",
    bg="#caf0f8"
).grid(row=3, column=0, padx=5, pady=5)

combo_dodaj_zanr = ttk.Combobox(
    frame_dodavanje,
    values=list(filmovi.keys()),
    state="readonly",
    width=22
)

combo_dodaj_zanr.grid(row=3, column=1)
combo_dodaj_zanr.current(0)


# GUMB ZA DODAVANJE
btn_dodaj = tk.Button(
    frame_dodavanje,
    text="Dodaj film",
    command=dodaj_film,
    bg="#0077b6",
    fg="white",
    font=("Arial", 11, "bold"),
    width=20
)

btn_dodaj.grid(
    row=4,
    column=0,
    columnspan=2,
    pady=15
)


# ------------------------------------------------
# FOOTER
# ------------------------------------------------
footer = tk.Label(
    root,
    text="Maturantski projekt - Python GUI aplikacija",
    bg="#dff6ff",
    fg="gray"
)

footer.pack(side=tk.BOTTOM, pady=10)

# ------------------------------------------------
# BRISANJE FILMA
# ------------------------------------------------
def obrisi_film():

    odabrani_film = lista_filmova.focus()

    if odabrani_film == "":
        messagebox.showwarning(
            "Greška",
            "Odaberi film za brisanje!"
        )
        return

    podaci = lista_filmova.item(odabrani_film)

    naziv_filma = podaci["values"][0]

    # Traženje i brisanje filma iz liste
    for zanr in filmovi:

        for film in filmovi[zanr]:

            if film["naziv"] == naziv_filma:

                filmovi[zanr].remove(film)

                messagebox.showinfo(
                    "Uspjeh",
                    f"Film '{naziv_filma}' je obrisan!"
                )

                prikazi_filmove()
                return
            
# ------------------------------------------------
# GUMB ZA BRISANJE FILMA
# ------------------------------------------------
btn_obrisi = tk.Button(
    frame_dodavanje,
    text="Obriši označeni film",
    command=obrisi_film,
    bg="#d62828",
    fg="white",
    font=("Arial", 11, "bold"),
    width=20
)

btn_obrisi.grid(
    row=5,
    column=0,
    columnspan=2,
    pady=5
)

# ------------------------------------------------
# POKRETANJE PROGRAMA
# ------------------------------------------------
root.mainloop()