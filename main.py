import os
import tkinter as tk
from tkinter import filedialog
from datetime import datetime

from functions.attributeAnalysis import attribute_analysis
from functions.basicDataAnalysis import basic_data_analysis
from functions.kMC import kMC
from list_of_attributes import list_of_attributes

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

    # Create a folder to store the results, named by result with the current timestamp till the milliseconds
    current_time = datetime.now().strftime("%Y-%m-%d-%H-%M-%S-%f")
    result_folder = file_path+'/result_'+current_time
    os.mkdir(result_folder)
    attribute_analysis(result_folder, csv_file_path)
    basic_data_analysis(result_folder, csv_file_path)

    # Perform Clustering for every attribute in the list_of_attributes
    for attribute in list_of_attributes:
        kMC(result_folder, csv_file_path, attribute)


if __name__ == "__main__":
    main()
