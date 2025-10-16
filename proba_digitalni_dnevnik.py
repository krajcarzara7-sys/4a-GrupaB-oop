import tkinter as tk
from tkinter import messagebox, filedialog
import csv

class Kontakt:
    def __init__ (self, ime, email, telefon):
        self.ime=ime
        self.email=email
        self.telefon=telefon
    def __str__(self):
        return (f'{self.ime} {self.email} {self.telefon}')

class ImenikApp:
    def __init__(self,root):
        self.root=root
        self.kontakti=[]
        self.odabrani_kontakt_index = None
        

        self.root.title('Digitalni imenik')
        self.root.geometry('640x420')
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)

        unos_frame = tk.Frame(self.root, padx=10, pady=10)
        unos_frame.grid(row=0, column=0, sticky="EW")
        unos_frame.columnconfigure(1, weight=1)

        

        
        tk.Label(unos_frame, text='Ime:').grid(row=0, column=0, padx=5, pady=5, sticky='W')
        self.ime_entry=tk.Entry(unos_frame)
        self.ime_entry.grid(row=0, column=1, padx=5, pady=5, sticky='EW')

        tk.Label(unos_frame, text='Email:').grid(row=1, column=0, padx=5, pady=5, sticky='W')
        self.email_entry=tk.Entry(unos_frame)
        self.email_entry.grid(row=1, column=1, padx=5, pady=5, sticky='EW')

        tk.Label(unos_frame, text='Telefon:').grid(row=2, column=0, padx=5, pady=5, sticky='W')
        self.telefon_entry=tk.Entry(unos_frame)
        self.telefon_entry.grid(row=2, column=1, padx=5, pady=5, sticky='EW')

        gumbi_frame = tk.Frame(unos_frame)
        gumbi_frame.grid(row=3, column=0, columnspan=2, sticky="W", pady=(8, 0))

        self.dodaj_gumb = tk.Button(gumbi_frame, text="Učitaj kontakt", command=self.dodaj_kontakt)
        self.dodaj_gumb.grid(row=0, column=0, padx=5, pady=5)

        self.spremi_gumb = tk.Button(gumbi_frame, text="Spremi kontakte", command=self.spremi_izmjene)
        self.spremi_gumb.grid(row=0, column=1, padx=5, pady=5)

        self.obrisi_gumb = tk.Button(gumbi_frame, text="Obriši kontakt", command=self.obrisi_ucenika)
        self.obrisi_gumb.grid(row=0, column=2, padx=5, pady=5)

        file_frame = tk.Frame(unos_frame)
        file_frame.grid(row=4, column=0, columnspan=2, sticky="W", pady=(8, 0))

        prikaz_frame = tk.Frame(self.root, padx=10, pady=10)
        prikaz_frame.grid(row=1, column=0, sticky="NSEW")
        prikaz_frame.columnconfigure(0, weight=1)
        prikaz_frame.rowconfigure(0, weight=1)

        self.listbox = tk.Listbox(prikaz_frame)
        self.listbox.grid(row=0, column=0, sticky="NSEW")
        self.listbox.bind('<<ListboxSelect>>', self.odaberi_kontakt)

        scrollbar = tk.Scrollbar(prikaz_frame, orient="vertical", command=self.listbox.yview)
        scrollbar.grid(row=0, column=1, sticky="NS")
        self.listbox.config(yscrollcommand=scrollbar.set)

        self.ucitaj_iz_csv()

       
    def dodaj_kontakt(self):
        ime = self.ime_entry.get().strip()
        email = self.email_entry.get().strip()
        telefon = self.telefon_entry.get().strip()
        if not (ime and email and telefon):
            messagebox.showwarning("Upozorenje", "Ispuni sva polja (Ime, Email, telefon).")
            return
        self.kontakti.append(Kontakt(ime, email, telefon))
        self.osvjezi_prikaz()
        self.ocisti_polja()
        self.spremi_u_csv()

    def osvjezi_prikaz(self):
        self.listbox.delete(0, tk.END)
        for u in self.kontakti:
            self.listbox.insert(tk.END, str(u))

    def ocisti_polja(self):
        self.ime_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.telefon_entry.delete(0, tk.END)

    def odaberi_kontakt(self, event):
        odabrani_indeksi = self.listbox.curselection()
        if not odabrani_indeksi:
            return
        self.odabrani_kontakt_index = odabrani_indeksi[0]
        odabrani = self.kontakti[self.odabrani_kontakt_index]
        self.ime_entry.delete(0, tk.END);     self.ime_entry.insert(0, odabrani.ime)
        self.email_entry.delete(0, tk.END); self.email_entry.insert(0, odabrani.email)
        self.telefon_entry.delete(0, tk.END);  self.telefon_entry.insert(0, odabrani.telefon)
    def spremi_u_csv(self):
        with open('kontakti.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Ime', 'Email', 'Telefon'])
            for kontakt in self.kontakti:
                writer.writerow([kontakt.ime, kontakt.email, kontakt.telefon])

    def ucitaj_iz_csv(self):
        try:
            with open('kontakti.csv', mode='r') as file:
                reader = csv.reader(file)
                next(reader)
                for row in reader:
                    if len(row)==3:
                        ime, email, telefon = row
                        self.kontakti.append(Kontakt(ime,email,telefon))
                self.osvjezi_prikaz()
        except FileNotFoundError:
            messagebox.showinfo('Info', 'Datoteka kontakti.csv nije pronađena, počinjemo od praznog imenika.')
            


    def spremi_izmjene(self):
        if self.odabrani_kontakt_index is None:
            messagebox.showinfo("Info", "Nije odabran nijedan učenik.")
            return
        ime = self.ime_entry.get().strip()
        email = self.email_entry.get().strip()
        telefon = self.telefon_entry.get().strip()
        if not (ime and email and telefon):
            messagebox.showwarning("Upozorenje", "Ispuni sva polja prije spremanja izmjena.")
            return
        u = self.kontakti[self.odabrani_kontakt_index]
        u.ime, u.email, u.telefon = ime, email, telefon
        self.osvjezi_prikaz()
        self.ocisti_polja()
        self.odabrani_kontakt_index = None
        self.spremi_u_csv()

    def obrisi_ucenika(self):
        odabrani_indeksi = self.listbox.curselection()
        if not odabrani_indeksi:
            messagebox.showinfo("Info", "Najprije odaberi učenika iz liste.")
            return
        idx = odabrani_indeksi[0]
        potvrda = messagebox.askyesno("Potvrda brisanja", "Želiš li obrisati odabranog učenika?")
        if potvrda:
            del self.kontakti[idx]
            self.osvjezi_prikaz()
            self.ocisti_polja()
            self.odabrani_kontakt_index = None
            self.spremi_u_csv()




if __name__ == "__main__":
    root = tk.Tk()
    app = ImenikApp(root)
    root.mainloop()
