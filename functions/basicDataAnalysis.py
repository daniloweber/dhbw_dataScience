import os
import pandas as pd
from pdf import PDF

def summary_statistics (csv_file_path):

    # Load the dataset
    data = pd.read_csv(csv_file_path)
    # set male and female to 0 and 1
    data['Gender'] = data['Gender'].map({'Male': 0, 'Female': 1})
    #shape of the data
    shape = data.shape
    #Summary statistics
    summary = data.describe()

    return shape, summary


def basic_data_analysis(directory, csv_file_path):

    shape, summary = summary_statistics(csv_file_path)

    pdf = PDF(title='Basic Data Analysis Report')
    pdf.add_page()

    # Add shape chapter
    pdf.chapter_title("Datensatzform")
    pdf.chapter_body(f'{shape[1]} Spalten, {shape[0]} Zeilen')

    # Add summary chapter
    pdf.chapter_title("Beschreibende Statistik")
    pdf.add_table(summary)

    # Save the PDF to the given file path
    pdf.output(os.path.join(directory, 'basic_data_analysis_report.pdf'))

