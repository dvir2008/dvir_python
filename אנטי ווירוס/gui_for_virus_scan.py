import tkinter as tk
from tkinter import filedialog
import viros_scan

from colorama import Fore, Back, Style, init
init(autoreset=True)

def select_folder_and_scan():
    folder_path = filedialog.askdirectory()
    if folder_path:
        viros_scan.itratza_files(folder_path)
        print(Fore.GREEN+"scan complited")
    else:
        print(Fore.RED+"Folder selection cancelled.")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Virus Scan")
    root.geometry("300x100")
    scan_button = tk.Button(root, text="Select Folder and Scan", command=select_folder_and_scan)
    scan_button.pack(pady=30)
    root.mainloop()
