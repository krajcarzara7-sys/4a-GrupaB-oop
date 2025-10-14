import tkinter as tk
from tkinter import messagebox, filedialog
import json

class ucenik:
    def __init__(self, ime_ucenika, prezime_ucenika, razred_ucenika):
        self.ime = ime_ucenika
        self.prezime = prezime_ucenika
        self.razred = razred_ucenika

    def __str__(self):
        return f'{self.prezime} {self.ime} ({self.razred})'

    def to_dict(self):
        return {"ime": self.ime, "prezime": self.prezime, "razred": self.razred}

    @staticmethod
    def from_dict(d):
        return ucenik(d["ime"], d["prezime"], d["razred"])


class EvidencijaApp:
    def __init__(self, root):
        self.root = root
        self.ucenici = []
        self.odabrani_ucenik_index = None

        self.root.title("Evidencija učenika")
        self.root.geometry("640x420")

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)

        unos_frame = tk.Frame(self.root, padx=10, pady=10)
        unos_frame.grid(row=0, column=0, sticky="EW")
        unos_frame.columnconfigure(1, weight=1)

        tk.Label(unos_frame, text="Ime:").grid(row=0, column=0, padx=5, pady=5, sticky="W")
        self.ime_entry = tk.Entry(unos_frame)
        self.ime_entry.grid(row=0, column=1, padx=5, pady=5, sticky="EW")

        tk.Label(unos_frame, text="Prezime:").grid(row=1, column=0, padx=5, pady=5, sticky="W")
        self.prezime_entry = tk.Entry(unos_frame)
        self.prezime_entry.grid(row=1, column=1, padx=5, pady=5, sticky="EW")

        tk.Label(unos_frame, text="Razred:").grid(row=2, column=0, padx=5, pady=5, sticky="W")
        self.razred_entry = tk.Entry(unos_frame)
        self.razred_entry.grid(row=2, column=1, padx=5, pady=5, sticky="EW")

        gumbi_frame = tk.Frame(unos_frame)
        gumbi_frame.grid(row=3, column=0, columnspan=2, sticky="W", pady=(8, 0))

        self.dodaj_gumb = tk.Button(gumbi_frame, text="Dodaj učenika", command=self.dodaj_ucenika)
        self.dodaj_gumb.grid(row=0, column=0, padx=5, pady=5)

        self.spremi_gumb = tk.Button(gumbi_frame, text="Spremi izmjene", command=self.spremi_izmjene)
        self.spremi_gumb.grid(row=0, column=1, padx=5, pady=5)

        self.obrisi_gumb = tk.Button(gumbi_frame, text="Obriši učenika", command=self.obrisi_ucenika)
        self.obrisi_gumb.grid(row=0, column=2, padx=5, pady=5)

        file_frame = tk.Frame(unos_frame)
        file_frame.grid(row=4, column=0, columnspan=2, sticky="W", pady=(8, 0))

        self.ucitaj_gumb = tk.Button(file_frame, text="Učitaj...", command=self.ucitaj_iz_datoteke)
        self.ucitaj_gumb.grid(row=0, column=0, padx=5, pady=5)

        self.spremi_dat_gumb = tk.Button(file_frame, text="Spremi...", command=self.spremi_u_datoteku)
        self.spremi_dat_gumb.grid(row=0, column=1, padx=5, pady=5)

        prikaz_frame = tk.Frame(self.root, padx=10, pady=10)
        prikaz_frame.grid(row=1, column=0, sticky="NSEW")
        prikaz_frame.columnconfigure(0, weight=1)
        prikaz_frame.rowconfigure(0, weight=1)

        self.listbox = tk.Listbox(prikaz_frame)
        self.listbox.grid(row=0, column=0, sticky="NSEW")
        self.listbox.bind('<<ListboxSelect>>', self.odaberi_ucenika)

        scrollbar = tk.Scrollbar(prikaz_frame, orient="vertical", command=self.listbox.yview)
        scrollbar.grid(row=0, column=1, sticky="NS")
        self.listbox.config(yscrollcommand=scrollbar.set)


    def dodaj_ucenika(self):
        ime = self.ime_entry.get().strip()
        prezime = self.prezime_entry.get().strip()
        razred = self.razred_entry.get().strip()
        if not (ime and prezime and razred):
            messagebox.showwarning("Upozorenje", "Ispuni sva polja (Ime, Prezime, Razred).")
            return
        self.ucenici.append(ucenik(ime, prezime, razred))
        self.osvjezi_prikaz()
        self.ocisti_polja()

    def osvjezi_prikaz(self):
        self.listbox.delete(0, tk.END)
        for u in self.ucenici:
            self.listbox.insert(tk.END, str(u))

    def odaberi_ucenika(self, event):
        odabrani_indeksi = self.listbox.curselection()
        if not odabrani_indeksi:
            return
        self.odabrani_ucenik_index = odabrani_indeksi[0]
        odabrani = self.ucenici[self.odabrani_ucenik_index]
        self.ime_entry.delete(0, tk.END);     self.ime_entry.insert(0, odabrani.ime)
        self.prezime_entry.delete(0, tk.END); self.prezime_entry.insert(0, odabrani.prezime)
        self.razred_entry.delete(0, tk.END);  self.razred_entry.insert(0, odabrani.razred)

    def spremi_izmjene(self):
        if self.odabrani_ucenik_index is None:
            messagebox.showinfo("Info", "Nije odabran nijedan učenik.")
            return
        ime = self.ime_entry.get().strip()
        prezime = self.prezime_entry.get().strip()
        razred = self.razred_entry.get().strip()
        if not (ime and prezime and razred):
            messagebox.showwarning("Upozorenje", "Ispuni sva polja prije spremanja izmjena.")
            return
        u = self.ucenici[self.odabrani_ucenik_index]
        u.ime, u.prezime, u.razred = ime, prezime, razred
        self.osvjezi_prikaz()
        self.ocisti_polja()
        self.odabrani_ucenik_index = None

    def obrisi_ucenika(self):
        odabrani_indeksi = self.listbox.curselection()
        if not odabrani_indeksi:
            messagebox.showinfo("Info", "Najprije odaberi učenika iz liste.")
            return
        idx = odabrani_indeksi[0]
        potvrda = messagebox.askyesno("Potvrda brisanja", "Želiš li obrisati odabranog učenika?")
        if potvrda:
            del self.ucenici[idx]
            self.osvjezi_prikaz()
            self.ocisti_polja()
            self.odabrani_ucenik_index = None

    def spremi_u_datoteku(self):
        if not self.ucenici:
            if not messagebox.askyesno("Prazna lista", "Lista je prazna. Svejedno spremiti?"):
                return
        path = filedialog.asksaveasfilename(
            title="Spremi kao",
            defaultextension=".json",
            filetypes=[("JSON datoteke", "*.json"), ("Sve datoteke", "*.*")]
        )
        if not path:
            return
        try:
            data = [u.to_dict() for u in self.ucenici]
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            messagebox.showinfo("Uspjeh", f"Podaci su spremljeni u:\n{path}")
        except Exception as e:
            messagebox.showerror("Greška pri spremanju", str(e))

    def ucitaj_iz_datoteke(self):
        path = filedialog.askopenfilename(
            title="Učitaj datoteku",
            filetypes=[("JSON datoteke", "*.json"), ("Sve datoteke", "*.*")]
        )
        if not path:
            return
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.ucenici = [ucenik.from_dict(d) for d in data]
            self.osvjezi_prikaz()
            self.ocisti_polja()
            self.odabrani_ucenik_index = None
            messagebox.showinfo("Uspjeh", f"Učitano iz:\n{path}")
        except Exception as e:
            messagebox.showerror("Greška pri učitavanju", str(e))

    def ocisti_polja(self):
        self.ime_entry.delete(0, tk.END)
        self.prezime_entry.delete(0, tk.END)
        self.razred_entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = EvidencijaApp(root)
    root.mainloop()
