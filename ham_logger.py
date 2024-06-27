import tkinter as tk
from tkinter import messagebox
from datetime import datetime

def band_name(Frequency):
    if Frequency < 14.350 and Frequency > 14.000:
        return "20M"
    else:
        return None



class HamRadioLogger:
    def __init__(self, master):
        self.master = master
        self.master.title("Ham Radio Logger")

        self.my_callsign_label = tk.Label(master, text="My callsign:")
        self.my_callsign_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.my_callsign_entry = tk.Entry(master)
        self.my_callsign_entry.grid(row=0, column=1, padx=5, pady=5)

        self.my_park_label = tk.Label(master, text="My Park:")
        self.my_park_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.my_park_entry = tk.Entry(master)
        self.my_park_entry.grid(row=1, column=1, padx=5, pady=5)

        self.mode_options = [
            "SSB",
            "CW",
        ]
        self.clicked = tk.StringVar()
        # initial menu text
        self.clicked.set("SSB")

        # Create Dropdown menu
        self.mode_entry = tk.OptionMenu(master, self.clicked, *self.mode_options)
        self.mode_entry.grid(row=2, column=1, padx=5, pady=5)


        self.frequency_label = tk.Label(master, text="Frequency:")
        self.frequency_label.grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.frequency_entry = tk.Entry(master)
        self.frequency_entry.grid(row=3, column=1, padx=5, pady=5)

        self.callsign_label = tk.Label(master, text="Callsign:")
        self.callsign_label.grid(row=4, column=0, padx=5, pady=5, sticky="e")
        self.callsign_entry = tk.Entry(master)
        self.callsign_entry.grid(row=4, column=1, padx=5, pady=5)

        self.qth_label = tk.Label(master, text="QTH:")
        self.qth_label.grid(row=5, column=0, padx=5, pady=5, sticky="e")
        self.qth_entry = tk.Entry(master)
        self.qth_entry.grid(row=5, column=1, padx=5, pady=5)

        self.park_label = tk.Label(master, text="Park:")
        self.park_label.grid(row=6, column=0, padx=5, pady=5, sticky="e")
        self.park_entry = tk.Entry(master)
        self.park_entry.grid(row=6, column=1, padx=5, pady=5)

        self.submit_button = tk.Button(master, text="Submit", command=self.submit_entry)
        self.submit_button.grid(row=7, columnspan=2, padx=5, pady=5)


        def sel():
            if self.time_option.get() == 1:
                "Show manual time box"
            else:
                "Hide manual time box and "

        self.time_option=tk.IntVar()
        self.R1 = tk.Radiobutton(master, text="Now", variable=self.time_option, value=0, command=sel)
        self.R1.grid(row=6, column=0, padx=5, pady=5, sticky="e")
        self.R2 = tk.Radiobutton(master, text="Manual time", variable=self.time_option, value=1, command=sel)
        self.R2.grid(row=6, column=2, padx=5, pady=5, sticky="e")



    def submit_entry(self):
        my_callsign = self.my_callsign_entry.get().strip()
        callsign = self.callsign_entry.get().strip()
        qth = self.qth_entry.get().strip()
        park = self.park_entry.get().strip()
        Frequency = self.frequency_entry.get().strip()
        my_park=self.my_park_entry.get().strip()
        mode=self.clicked.get().strip()

        print(Frequency)
        band=band_name(float(Frequency))

        if not callsign:
            messagebox.showerror("Error", "Please fill call sign at minimum")
            return

        if not band:
            messagebox.showerror("Error", "QSO out of band allocations")
            return


        datestamp = datetime.utcnow().strftime('%Y%m%d')
        timestamp = datetime.utcnow().strftime('%H%M')
        
        with open("log.adif", "a") as file:

            QSO_str=(f"<QSO_DATE:8{len(datestamp)}>{datestamp} <TIME_ON:4{len(timestamp)}>{timestamp} <STATION_CALL:{len(my_callsign)}>{my_callsign.upper()} <MODE:{len(mode)}>{mode} "
                     f"<OPERATOR:{len(my_callsign)}>{my_callsign.upper()} <MY_SIG:4>POTA <MY_SIG_INFO:{len(my_park)}>{my_park.upper()} <CALL:{len(callsign)}>{callsign.upper()}")


            print(len(park))
            print("Park is:" +str(park))
            if len(park)!=0:
                QSO_str += f" <SIG:4>POTA <SIG_INFO:{len(park)}>{park}"
            if len(qth)!=0:
                QSO_str += f" <STATE:{len(qth)}>{qth}"

            QSO_str += " <EOR>\n"
            file.write(QSO_str)
        
        messagebox.showinfo("Success", "Entry submitted successfully")

        self.callsign_entry.delete(0, tk.END)
        self.qth_entry.delete(0, tk.END)
        self.park_entry.delete(0, tk.END)

def main():
    root = tk.Tk()
    app = HamRadioLogger(root)
    root.mainloop()

if __name__ == "__main__":
    main()
