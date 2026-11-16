<?php
// mPDF: HTML invoice of a fictional studio. Edit target: 1,940.00 -> 7,940.00 (subtotal row + total due).
require __DIR__ . '/vendor/autoload.php';

$mpdf = new \Mpdf\Mpdf(['format' => 'A4', 'tempDir' => sys_get_temp_dir() . '/mpdf-research']);
$mpdf->SetCreator('Brightline Billing');
$mpdf->SetAuthor('Brightline Design Studio');
$mpdf->SetTitle('Invoice INV-2026-0417');

$html = <<<HTML
<style>
body { font-family: dejavusans; font-size: 9.5pt; color: #222; }
h1 { font-size: 18pt; margin: 0; }
.muted { color: #666; font-size: 8pt; }
table.items { width: 100%; border-collapse: collapse; margin-top: 14pt; }
table.items th { background: #eef1f4; text-align: left; padding: 5pt; font-size: 8.5pt; }
table.items td { border-bottom: 0.5pt solid #ccc; padding: 5pt; }
.r { text-align: right; }
.total td { font-weight: bold; font-size: 11pt; border-bottom: none; }
</style>
<table width="100%"><tr>
<td><h1>Brightline Design Studio</h1><div class="muted">7 Canal Street, Westbrook · fictional company · SAMPLE</div></td>
<td class="r"><b>INVOICE</b><br>INV-2026-0417<br>Issued 2026-10-28<br>Due 2026-11-27</td>
</tr></table>
<p><b>Bill to:</b> Example Retail Ltd, 15 Market Square, Eastfield</p>
<table class="items">
<tr><th>Description</th><th class="r">Qty</th><th class="r">Rate</th><th class="r">Amount</th></tr>
<tr><td>Brand identity refresh</td><td class="r">1</td><td class="r">1,200.00</td><td class="r">1,200.00</td></tr>
<tr><td>Landing page design</td><td class="r">1</td><td class="r">560.00</td><td class="r">560.00</td></tr>
<tr><td>Revision rounds</td><td class="r">3</td><td class="r">60.00</td><td class="r">180.00</td></tr>
<tr><td colspan="3" class="r">Subtotal</td><td class="r">1,940.00</td></tr>
<tr><td colspan="3" class="r">VAT (0%, reverse charge)</td><td class="r">0.00</td></tr>
<tr class="total"><td colspan="3" class="r">Total due (USD)</td><td class="r">1,940.00</td></tr>
</table>
<p class="muted" style="margin-top:24pt">Payment by bank transfer, reference INV-2026-0417. Synthetic document for research (SAMPLE).</p>
HTML;

$mpdf->WriteHTML($html);
$mpdf->Output($argv[1], \Mpdf\Output\Destination::FILE);
