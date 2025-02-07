import os
import pandas as pd
from fpdf import FPDF
from sklearn.linear_model import LinearRegression
from fpdf.enums import XPos, YPos

class PDF(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 20)
        self.cell(0, 10, "Datensatzvoranalyse", 0, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
        self.ln(10)

    def chapter_title(self, title):
        self.set_font("Helvetica", "B", 12)
        self.cell(0, 10, title, 0, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='L')
        self.ln(10)

    def chapter_body(self, body):
        self.set_font("Helvetica", size=10)
        self.multi_cell(0, 10, body)
        self.ln()

    def add_table(self, dataframe):
        self.set_font("Helvetica", size=10)
        col_width = self.w / (len(dataframe.columns) + 2)  # Adjust column width dynamically
        row_height = self.font_size * 1.5

        # Add column headers
        self.cell(col_width, row_height, "", border=1)  # Empty cell for the index column
        for col in dataframe.columns:
            self.cell(col_width, row_height, str(col), border=1)
        self.ln(row_height)

        # Add rows
        for idx, row in dataframe.iterrows():
            self.cell(col_width, row_height, str(idx), border=1)  # Index column
            for item in row:
                # Format numbers to fit within the cell
                if isinstance(item, (int, float)):
                    item = f"{item:.2f}"
                self.cell(col_width, row_height, str(item), border=1)
            self.ln(row_height)

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


def basic_data_analysis(file_path, csv_file_path):

    shape, summary = summary_statistics(csv_file_path)


    pdf = PDF()
    pdf.add_page()

    # Add shape chapter
    pdf.chapter_title("Datensatzform")
    pdf.chapter_body(f'{shape[1]} Spalten, {shape[0]} Zeilen')

    # Add summary chapter
    pdf.chapter_title("Beschreibende Statistik")
    pdf.add_table(summary)

    # Save the PDF to the given file path
    pdf.output(os.path.join(file_path, 'basic_data_analysis_report.pdf'))

