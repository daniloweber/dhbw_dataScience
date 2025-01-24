import os
import tkinter as tk
from tkinter import filedialog

from functions.attributeAnalysis import attribute_analysis
from functions.basicDataAnalysis import basic_data_analysis
from functions.kMC import kMC

# Get the directory of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the absolute path to the CSV file
csv_file_path = os.path.join(current_dir, 'kunden_einkaufszentrum.csv')

def select_folder():
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    folder_path = filedialog.askdirectory(title="Select Folder")
    return folder_path



def main():
    file_path = select_folder()
    if not file_path:
        print("No folder selected. Exiting.")
        return

    run_all = input("Do you want to run the whole code? (Yes/no): ").strip().lower()
    if run_all == "yes" or run_all == "":
        attribute_analysis(file_path, csv_file_path)
        basic_data_analysis(file_path, csv_file_path)
        kMC(file_path, csv_file_path)
    else:
        print("Exiting.")

if __name__ == "__main__":
    main()