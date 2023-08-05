from io import BytesIO

from reportlab.lib.pagesizes import inch, A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import PageBreak
from reportlab.platypus import Paragraph
from reportlab.platypus import SimpleDocTemplate


class BuildPDF:

    def __init__(self):
        self.pdf_buffer = BytesIO()
        self._doc_file = SimpleDocTemplate(
            self.pdf_buffer,
            pagesize=A4,
            topMargin=1 * inch,
            leftMargin=1 * inch,
            rightMargin=1 * inch,
            bottomMargin=1 * inch
        )
        self.sample_style_sheet = getSampleStyleSheet()
        self.flowables = list()

    def create_from_json(self, json_data: list):
        for jd in json_data:
            if jd["data"] == "":
                self.flowables.append(PageBreak())
            else:
                paragraph = Paragraph(jd["data"], self.sample_style_sheet[jd["style"]])
                self.flowables.append(paragraph)

    def build(self):
        self._doc_file.build(self.flowables)

    def get_buffer(self):
        return self.pdf_buffer
