"""WeasyPrint: HTML/CSS payment receipt of a fictional service. Edit target: $3,150.00 -> $8,150.00 (twice)."""
import sys
from weasyprint import HTML

html = """<!doctype html><html><head><meta charset="utf-8">
<title>Payment receipt R-88213</title>
<meta name="author" content="Parcelway Payments">
<meta name="generator" content="Parcelway Receipts">
<style>
@page { size: A4; margin: 22mm 20mm; }
body { font-family: Helvetica, Arial, sans-serif; font-size: 10pt; color: #1d1d1f; }
.brand { font-size: 17pt; font-weight: 700; }
.muted { color: #6e6e73; font-size: 8pt; }
.amount { font-size: 26pt; font-weight: 700; margin: 18pt 0 4pt; }
table { width: 100%; border-collapse: collapse; margin-top: 16pt; }
td { padding: 6pt 0; border-bottom: 0.5pt solid #d2d2d7; }
td.r { text-align: right; }
.badge { display: inline-block; background: #e3f5ea; color: #116b3a; padding: 2pt 6pt; border-radius: 4pt; font-size: 8pt; }
</style></head><body>
<div class="brand">Parcelway</div>
<div class="muted">Parcelway Payments · fictional company · SAMPLE</div>
<div class="amount">$3,150.00</div>
<span class="badge">Paid</span> <span class="muted">October 30, 2026 at 14:12</span>
<table>
<tr><td>Receipt number</td><td class="r">R-88213</td></tr>
<tr><td>Paid to</td><td class="r">Harbor Freight Partners</td></tr>
<tr><td>Payment method</td><td class="r">Visa •••• 0042</td></tr>
<tr><td>Description</td><td class="r">Container booking, October</td></tr>
<tr><td><b>Amount</b></td><td class="r"><b>$3,150.00</b></td></tr>
</table>
<p class="muted" style="margin-top:28pt">Questions? support@parcelway.example · Synthetic document for research (SAMPLE).</p>
</body></html>"""

HTML(string=html).write_pdf(sys.argv[1])
