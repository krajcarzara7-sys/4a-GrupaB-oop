import tkinter as tk

class ucenik:
    def __init__ (self, ime_ucenika, prezime_ucenika, razred_ucenika):
        self.ime=ime_ucenika
        self.prezime=prezime_ucenika
        self.razred=razred_ucenika
    def __str__(self):
        print(f'{self.prezime} {self.ime} {self.razred}')

#print(ucenik('Nina', 'Smolica', '4.a'))
    
ucenik1=ucenik('Nina', 'Smolica', '4.a')
ucenik1.__str__()


class EvidencijaApp:
    def __init__(self, root):
        
        self.root=root
        self.ucenici=[]
        self.odabrani_ucenik_index=None
        
        self.root.title("Evidencija učenika")
        self.root.geometry("500x400")
       
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)

        
        unos_frame = tk.Frame(self.root, padx=10, pady=10)
        unos_frame.grid(row=0, column=0, sticky="EW") 

       
        prikaz_frame = tk.Frame(self.root, padx=10, pady=10)
        prikaz_frame.grid(row=1, column=0, sticky="NSEW") 

        
        prikaz_frame.columnconfigure(0, weight=1)
        prikaz_frame.rowconfigure(0, weight=1)
        
        tk.Label(unos_frame, text="Ime:").grid(row=0, column=0, padx=5, pady=5, sticky="W")
        self.ime_entry = tk.Entry(unos_frame)
        self.ime_entry.grid(row=0, column=1, padx=5, pady=5, sticky="EW")
        
        tk.Label(unos_frame, text="Prezime:").grid(row=1, column=0, padx=5, pady=5, sticky="W")
        self.prezime_entry = tk.Entry(unos_frame)
        self.prezime_entry.grid(row=1, column=1, padx=5, pady=5, sticky="EW")
        
        tk.Label(unos_frame, text="Razred:").grid(row=2, column=0, padx=5, pady=5, sticky="W")
        self.razred_entry = tk.Entry(unos_frame)
        self.razred_entry.grid(row=2, column=1, padx=5, pady=5, sticky="EW")
        
        self.dodaj_gumb = tk.Button(unos_frame, text="Dodaj učenika")
        self.dodaj_gumb.grid(row=3, column=0, padx=5, pady=10)
        self.spremi_gumb = tk.Button(unos_frame, text="Spremi izmjene")
        self.spremi_gumb.grid(row=3, column=1, padx=5, pady=10, sticky="W")
        
        self.listbox = tk.Listbox(prikaz_frame)
        self.listbox.grid(row=0, column=0, sticky="NSEW")
        
        scrollbar = tk.Scrollbar(prikaz_frame, orient="vertical", command=self.listbox.yview)
        scrollbar.grid(row=0, column=1, sticky="NS")
        self.listbox.config(yscrollcommand=scrollbar.set)


        def dodaj_ucenika(self):
            ime = self.entry_ime.get().strip()
            prezime= self.entry_prezime.get().strip()
            razred = self.entry_razred.get().strip()
            if ime or prezime or razred:
                ucenik_novi=ucenik(ime, prezime, razred)
                self.ucenici.append(ucenik_novi)

def osvjezi_prikaz(self):
    self.listbox.delete(0, tk.END)
    for ucenik in self.ucenici:
        self.listbox.insert(tk.END, ucenik)

def odaberi_ucenika(self):
    odabrani_indeksi=self.listbox.curselection()
    if not odabrani_indeksi:
        return
    self.odabrani_ucenik_index=odabrani_indeksi[0]
    odabrani_ucenik=self.ucenici[odabrani_ucenik]

def spremi_izmjene(self):
    


        
