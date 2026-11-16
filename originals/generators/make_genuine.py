"""Synthetic one-page statement of a fictional credit union, SAMPLE watermark.

Target of every edit: the closing balance 4,812.37 -> 9,812.37 (same width),
printed twice (summary box and last table row), like a real statement.
"""
import sys
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

F = "/System/Library/Fonts/Supplemental/"
pdfmetrics.registerFont(TTFont("Arial", F + "Arial.ttf"))
pdfmetrics.registerFont(TTFont("Arial-Bold", F + "Arial Bold.ttf"))

out = sys.argv[1]
c = canvas.Canvas(out, pagesize=letter)
c.setAuthor("Northgate Credit Union")
c.setTitle("Account statement 2026-10")
c.setCreator("NCU eStatements 4.2")
c.setProducer("NCU eStatements 4.2")
W, H = letter

c.setFont("Arial-Bold", 16); c.drawString(54, H - 60, "Northgate Credit Union")
c.setFont("Arial", 9); c.drawString(54, H - 74, "100 Example Avenue, Springfield  ·  fictional institution")
c.setFont("Arial-Bold", 11); c.drawString(54, H - 110, "Account statement  ·  October 1 – October 31, 2026")
c.setFont("Arial", 10)
c.drawString(54, H - 128, "Member: Jordan Sample   Account: ****4417")

# summary box
c.rect(380, H - 150, 178, 56)
c.setFont("Arial", 9); c.drawString(390, H - 110, "Opening balance"); c.drawRightString(548, H - 110, "3,906.12")
c.drawString(390, H - 124, "Total deposits"); c.drawRightString(548, H - 124, "2,950.00")
c.setFont("Arial-Bold", 10); c.drawString(390, H - 142, "Closing balance"); c.drawRightString(548, H - 142, "4,812.37")

rows = [
    ("10/01", "Opening balance", "", "3,906.12"),
    ("10/03", "Payroll deposit ACME LOGISTICS", "1,475.00", "5,381.12"),
    ("10/07", "Rent payment ONLINE TRANSFER", "-1,350.00", "4,031.12"),
    ("10/12", "Grocery MARKET 214", "-86.40", "3,944.72"),
    ("10/17", "Payroll deposit ACME LOGISTICS", "1,475.00", "5,419.72"),
    ("10/21", "Utility ELECTRIC CO", "-122.35", "5,297.37"),
    ("10/28", "Card payment FUEL STOP", "-485.00", "4,812.37"),
]
y = H - 190
c.setFont("Arial-Bold", 9)
for x, t in ((54, "Date"), (100, "Description")): c.drawString(x, y, t)
c.drawRightString(470, y, "Amount"); c.drawRightString(558, y, "Balance")
c.line(54, y - 4, 558, y - 4)
c.setFont("Arial", 9)
for d, desc, amt, bal in rows:
    y -= 16
    c.drawString(54, y, d); c.drawString(100, y, desc)
    c.drawRightString(470, y, amt); c.drawRightString(558, y, bal)

c.saveState()
c.setFont("Arial-Bold", 72); c.setFillGray(0.85)
c.translate(W / 2, H / 2 - 120); c.rotate(30); c.drawCentredString(0, 0, "SAMPLE")
c.restoreState()
c.setFont("Arial", 7); c.drawString(54, 40, "SAMPLE - NOT A VALID DOCUMENT. Generated for a research experiment.")
c.showPage(); c.save()
