# PDF class
from fpdf import FPDF
from fpdf.enums import XPos, YPos
from PIL import Image

class PDF(FPDF):
    def __init__(self, title="kMC-Clustering"):
        super().__init__()
        self.title = title

    def header(self):
        self.set_font("Helvetica", "B", 20)
        self.cell(0, 10, self.title, 0, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
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
        col_width = self.w / (len(dataframe.columns) + 1)
        row_height = self.font_size * 1.5

        # Add column headers
        for col in dataframe.columns:
            self.cell(col_width, row_height, str(col), border=1)
        self.ln(row_height)

        # Add rows
        for row in dataframe.itertuples():
            for item in row[1:]:
                # Format numbers to fit within the cell
                if isinstance(item, (int, float)):
                    item = f"{item:.2f}"
                self.cell(col_width, row_height, str(item), border=1)
            self.ln(row_height)

    def chapter_image(self, image_path, width=180):
        self.add_page()  # Start a new page
        with Image.open(image_path) as img:
            aspect_ratio = img.height / img.width
            height = width * aspect_ratio

        current_y = self.get_y()
        self.image(image_path, x=10, y=current_y, w=width)
        self.ln(height + 10)