# In a file called shirtificate.py, implement a program that prompts the user for their name and outputs, using fpdf2, a CS50 shirtificate in a
# file called shirtificate.pdf similar to this one for John Harvard, with these specifications:
    # The orientation of the PDF should be Portrait.
    # The format of the PDF should be A4, which is 210mm wide by 297mm tall.
    # The top of the PDF should say “CS50 Shirtificate” as text, centered horizontally.
    # The shirt’s image should be centered horizontally.
    # The user’s name should be on top of the shirt, in white text.
# All other details we leave to you. You’re even welcome to add borders, colors, and lines. Your shirtificate needn’t match John Harvard’s precisely.
# And no need to wrap long names across multiple lines.

from fpdf import FPDF
name = ""

class PDF(FPDF):
    def header(self):
        self.set_font("Helvetica", "", 40)
        self.cell(text="CS50 Shirtificate", align="C", center=True)
        self.ln(30)
        self.image("shirtificate.png", w=pdf.epw*.9, x="C")


def user_name():
    return input("Name: ")


if __name__=="__main__":
    name = user_name()
    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Helvetica", size=25)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, -230, text=f"{name} took CS50", align="C", center=True)
    pdf.output("shirtificate.pdf")

