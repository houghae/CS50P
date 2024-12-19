from fpdf import FPDF


class PDF(FPDF):
    def header(self):
        self.set_font("Helvetica", "", 40)
        self.cell(text="CS50 Shirtificate", align="C", center=True)
        self.ln(30)
        self.image("shirtificate.png", w=pdf.epw*.9, x="C")



pdf = PDF()
pdf.add_page()
pdf.set_font("Helvetica", size=25)
pdf.set_text_color(255, 255, 255)
pdf.cell(0, -230, text="Name took CS50", align="C", center=True)
pdf.output("new-tuto2.pdf")
