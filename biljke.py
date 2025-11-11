import tkinter as tk
from tkinter import messagebox, filedialog
from xml.etree import ElementTree as ET
from datetime import datetime, timedelta
import os



class Biljka:
    """Bazna klasa koja predstavlja biljku."""

    def __init__(self, ime, vrsta, datum_sadnje, interval_zalijevanja, datum_zadnjeg_zalijevanja=None):
        self.ime = ime
        self.vrsta = vrsta
        self.datum_sadnje = datum_sadnje
        self.interval_zalijevanja = int(interval_zalijevanja)
        self.datum_zadnjeg_zalijevanja = datum_zadnjeg_zalijevanja or datetime.now().strftime("%Y-%m-%d")

    def treba_zaliti(self):
        """Provjerava treba li biljku zaliti."""
        try:
            zadnje = datetime.strptime(self.datum_zadnjeg_zalijevanja, "%Y-%m-%d")
            return datetime.now().date() >= (zadnje + timedelta(days=self.interval_zalijevanja)).date()
        except Exception:
            return False

    def zalij(self):
        """Ažurira datum zadnjeg zalijevanja."""
        self.datum_zadnjeg_zalijevanja = datetime.now().strftime("%Y-%m-%d")


class SobnaBiljka(Biljka):
    def __init__(self, ime, vrsta, datum_sadnje, interval_zalijevanja, potreba_svjetla, datum_zadnjeg_zalijevanja=None):
        super().__init__(ime, vrsta, datum_sadnje, interval_zalijevanja, datum_zadnjeg_zalijevanja)
        self.potreba_svjetla = potreba_svjetla

    def __str__(self):
        return f"Sobna: {self.ime} ({self.vrsta}) – Svjetlo: {self.potreba_svjetla}"


class VanjskaBiljka(Biljka):
    def __init__(self, ime, vrsta, datum_sadnje, interval_zalijevanja, otpornost_hladnoca, datum_zadnjeg_zalijevanja=None):
        super().__init__(ime, vrsta, datum_sadnje, interval_zalijevanja, datum_zadnjeg_zalijevanja)
        self.otpornost_hladnoca = otpornost_hladnoca

    def __str__(self):
        return f"Vanjska: {self.ime} ({self.vrsta}) – Otpornost: {self.otpornost_hladnoca}"




class PlantKeeperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🌿 PlantKeeper 1.0")
        self.root.geometry("650x700")
        self.root.config(bg="#a5d6a7")

        self.biljke = []

        self._dodaj_logo()
        self._napravi_meni()
        self._napravi_formu()
        self._napravi_listu()

        self.status_var = tk.StringVar(value="Dobrodošli u PlantKeeper 🌿")
        self.status = tk.Label(root, textvariable=self.status_var, bg="#757575", fg="white", anchor="w")
        self.status.pack(fill="x", side="bottom")

   

    def _dodaj_logo(self):
        header = tk.Frame(self.root, bg="#2e7d32")
        header.pack(fill="x")

        
        logo_label = tk.Label(header, text="🌱", font=("Arial", 50), bg="#2e7d32", fg="white")
        logo_label.pack(side="left", padx=10, pady=5)

        tk.Label(header, text="PlantKeeper – Osobni asistent za tvoje biljke",
                 bg="#2e7d32", fg="white", font=("Arial", 16, "bold")).pack(side="left")

    def _napravi_meni(self):
        meni = tk.Menu(self.root)

        meni_dat = tk.Menu(meni, tearoff=0)
        meni_dat.add_command(label="Spremi kolekciju", command=self.spremi_xml)
        meni_dat.add_command(label="Učitaj kolekciju", command=self.ucitaj_xml)
        meni_dat.add_separator()
        meni_dat.add_command(label="Izlaz", command=self.root.destroy)

        meni_info = tk.Menu(meni, tearoff=0)
        meni_info.add_command(label="O aplikaciji", command=self.o_aplikaciji)

        meni.add_cascade(label="Datoteka", menu=meni_dat)
        meni.add_cascade(label="Pomoć", menu=meni_info)
        self.root.config(menu=meni)

    def _napravi_formu(self):
        frame = tk.LabelFrame(self.root, text="Unos nove biljke", bg="#a5d6a7", padx=10, pady=10)
        frame.pack(padx=10, pady=10, fill="x")

        self.tip_var = tk.StringVar(value="Sobna")
        tk.Label(frame, text="Tip biljke:", bg="#a5d6a7").grid(row=0, column=0, sticky="e")
        tk.OptionMenu(frame, self.tip_var, "Sobna", "Vanjska").grid(row=0, column=1, sticky="w")

        self.ime_entry = self._unos(frame, "Ime biljke:", 1)
        self.vrsta_entry = self._unos(frame, "Vrsta:", 2)
        self.datum_entry = self._unos(frame, "Datum sadnje (YYYY-MM-DD):", 3, default=datetime.now().strftime("%Y-%m-%d"))
        self.interval_entry = self._unos(frame, "Interval zalijevanja (dani):", 4)
        self.dodatno_entry = self._unos(frame, "Dodatno (svjetlo/otpornost):", 5)

        tk.Button(frame, text="➕ Dodaj biljku", bg="#2e7d32", fg="white",
                  command=self.dodaj_biljku).grid(row=6, column=0, columnspan=2, pady=5)

    def _napravi_listu(self):
        frame_lista = tk.LabelFrame(self.root, text="Popis biljaka", bg="#a5d6a7")
        frame_lista.pack(padx=10, pady=10, fill="both", expand=True)

        self.lista = tk.Listbox(frame_lista, width=70, height=15, font=("Arial", 10))
        self.lista.pack(padx=10, pady=10)

        tk.Button(self.root, text="💧 Osvježi zalijevanje", bg="#43a047", fg="white",
                  command=self.zalij_odabranu).pack(pady=5)

    def _unos(self, frame, label, row, default=""):
        tk.Label(frame, text=label, bg="#a5d6a7").grid(row=row, column=0, sticky="e")
        entry = tk.Entry(frame, width=35)
        entry.grid(row=row, column=1)
        if default:
            entry.insert(0, default)
        return entry

    

    def dodaj_biljku(self):
        try:
            tip = self.tip_var.get()
            ime = self.ime_entry.get().strip()
            vrsta = self.vrsta_entry.get().strip()
            datum = self.datum_entry.get().strip()
            interval = int(self.interval_entry.get().strip())
            dodatno = self.dodatno_entry.get().strip()

            if not (ime and vrsta and dodatno and datum):
                raise ValueError("Sva polja moraju biti popunjena!")

            biljka = SobnaBiljka(ime, vrsta, datum, interval, dodatno) if tip == "Sobna" else \
                     VanjskaBiljka(ime, vrsta, datum, interval, dodatno)

            self.biljke.append(biljka)
            self.osvjezi_listu()
            self.status_var.set(f"Dodana nova biljka: {ime}")
        except ValueError as e:
            messagebox.showerror("Greška", str(e))
        except Exception:
            messagebox.showerror("Greška", "Provjerite unos podataka.")

    def osvjezi_listu(self):
        self.lista.delete(0, tk.END)
        for b in self.biljke:
            prikaz = f"{b} | Zadnje zalijevanje: {b.datum_zadnjeg_zalijevanja}"
            self.lista.insert(tk.END, prikaz)
            if b.treba_zaliti():
                self.lista.itemconfig(tk.END, {'fg': 'red'})
            else:
                self.lista.itemconfig(tk.END, {'fg': 'green'})

    def zalij_odabranu(self):
        try:
            index = self.lista.curselection()
            if not index:
                raise ValueError("Odaberite biljku!")
            self.biljke[index[0]].zalij()
            self.osvjezi_listu()
            self.status_var.set("Biljka zalivena.")
        except ValueError as e:
            messagebox.showwarning("Upozorenje", str(e))

  

    def spremi_xml(self):
        try:
            korijen = ET.Element("KolekcijaBiljaka")
            for b in self.biljke:
                tip = "Sobna" if isinstance(b, SobnaBiljka) else "Vanjska"
                e_biljka = ET.SubElement(korijen, "Biljka", {"tip": tip})
                for k, v in b.__dict__.items():
                    ET.SubElement(e_biljka, k).text = str(v)

            ET.ElementTree(korijen).write("biljke.xml", encoding="utf-8", xml_declaration=True)
            self.status_var.set("Kolekcija spremljena u 'biljke.xml'")
        except Exception as e:
            messagebox.showerror("Greška", f"Neuspješno spremanje: {e}")

    def ucitaj_xml(self):
        try:
            if not os.path.exists("biljke.xml"):
                raise FileNotFoundError("Datoteka 'biljke.xml' nije pronađena!")
            stablo = ET.parse("biljke.xml")
            korijen = stablo.getroot()
            self.biljke.clear()
            for e in korijen:
                d = {p.tag: p.text for p in e}
                if e.attrib["tip"] == "Sobna":
                    self.biljke.append(SobnaBiljka(**d))
                else:
                    self.biljke.append(VanjskaBiljka(**d))
            self.osvjezi_listu()
            self.status_var.set("Kolekcija uspješno učitana.")
        except FileNotFoundError as e:
            messagebox.showerror("Greška", str(e))
        except Exception as e:
            messagebox.showerror("Greška", f"Greška pri učitavanju: {e}")

    

    def o_aplikaciji(self):
        win = tk.Toplevel(self.root)
        win.title("O aplikaciji")
        win.geometry("350x300")
        win.config(bg="#a5d6a7")

        tk.Label(win, text="🌿 PlantKeeper 1.0", font=("Arial", 16, "bold"), bg="#a5d6a7", fg="#2e7d32").pack(pady=10)
        tk.Label(win, text="Autor: Zara Sofia Krajcar, 4.a", bg="#a5d6a7").pack()
        tk.Label(win, text="Verzija: 1.0", bg="#a5d6a7").pack()
        tk.Label(win, text="Godina: 2025.", bg="#a5d6a7").pack()
        tk.Label(win, text="\nAplikacija za evidenciju i njegu sobnih i vanjskih biljaka.", wraplength=300, bg="#a5d6a7").pack()
        tk.Button(win, text="Zatvori", command=win.destroy, bg="#2e7d32", fg="white").pack(pady=10)



if __name__ == "__main__":
    root = tk.Tk()
    app = PlantKeeperApp(root)
    root.mainloop()
