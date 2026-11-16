"""fpdf2: payslip of a fictional employer with core Helvetica. Edit target: 2,618.40 -> 5,618.40 (twice)."""
import sys
from datetime import datetime, timezone
from fpdf import FPDF

pdf = FPDF(format="A4")
pdf.set_creator("Oakfield Payroll")
pdf.set_author("Oakfield Logistics")
pdf.set_title("Payslip October 2026")
pdf.set_creation_date(datetime(2026, 10, 31, 9, 0, tzinfo=timezone.utc))
pdf.set_margins(18, 18, 18)
pdf.add_page()

pdf.set_font("Helvetica", "B", 15); pdf.cell(0, 8, "Oakfield Logistics", new_x="LMARGIN", new_y="NEXT")
pdf.set_font("Helvetica", "", 8); pdf.cell(0, 5, "3 Depot Lane, Millbrook - fictional employer - SAMPLE", new_x="LMARGIN", new_y="NEXT")
pdf.ln(6)
pdf.set_font("Helvetica", "B", 11); pdf.cell(0, 6, "Payslip - October 2026", new_x="LMARGIN", new_y="NEXT")
pdf.set_font("Helvetica", "", 9)
pdf.cell(0, 5, "Employee: Sam Example    Employee no.: 00731    Pay date: 31.10.2026", new_x="LMARGIN", new_y="NEXT")
pdf.ln(5)

def row(label, amount, bold=False, fill=False):
    pdf.set_font("Helvetica", "B" if bold else "", 9.5)
    pdf.cell(130, 7, label, border="B", fill=fill)
    pdf.cell(44, 7, amount, border="B", align="R", fill=fill, new_x="LMARGIN", new_y="NEXT")

pdf.set_fill_color(236, 239, 243)
row("Earnings", "USD", bold=True, fill=True)
row("Base salary", "3,200.00")
row("Overtime 6 h", "184.50")
row("Gross pay", "3,384.50", bold=True)
pdf.ln(3)
row("Deductions", "USD", bold=True, fill=True)
row("Income tax", "-541.52")
row("Social security", "-209.84")
row("Health plan", "-14.74")
pdf.ln(3)
row("Net pay", "2,618.40", bold=True)
pdf.ln(8)
pdf.set_font("Helvetica", "", 9)
pdf.cell(0, 5, "Transferred to account ****5521: 2,618.40", new_x="LMARGIN", new_y="NEXT")
pdf.ln(6)
pdf.set_font("Helvetica", "", 7)
pdf.multi_cell(0, 4, "Synthetic document generated for research (SAMPLE). Oakfield Logistics does not exist.")
pdf.output(sys.argv[1])
