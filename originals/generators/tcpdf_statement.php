<?php
// TCPDF: one-page bank statement of a fictional bank. Edit target: 6,284.19 -> 8,284.19 (twice).
require __DIR__ . '/vendor/autoload.php';

$pdf = new TCPDF('P', 'mm', 'A4', true, 'UTF-8', false);
$pdf->SetCreator('Riverside Online Banking');
$pdf->SetAuthor('Riverside Savings Bank');
$pdf->SetTitle('Statement of account 2026-10');
$pdf->setPrintHeader(false);
$pdf->setPrintFooter(false);
$pdf->SetMargins(18, 18, 18);
$pdf->AddPage();

$pdf->SetFont('dejavusans', 'B', 15);
$pdf->Cell(0, 8, 'Riverside Savings Bank', 0, 1);
$pdf->SetFont('dejavusans', '', 8);
$pdf->Cell(0, 5, '42 Harbour Road, Lakeside · fictional institution · SAMPLE', 0, 1);
$pdf->Ln(6);
$pdf->SetFont('dejavusans', 'B', 11);
$pdf->Cell(0, 6, 'Statement of account · 1–31 October 2026', 0, 1);
$pdf->SetFont('dejavusans', '', 9);
$pdf->Cell(0, 5, 'Customer: Alex Sample    Account: ****2093    Currency: USD', 0, 1);
$pdf->Ln(4);

// summary
$pdf->SetFont('dejavusans', '', 9);
$pdf->Cell(120, 6, 'Opening balance', 'LT'); $pdf->Cell(54, 6, '4,918.64', 'TR', 1, 'R');
$pdf->Cell(120, 6, 'Credits', 'L');        $pdf->Cell(54, 6, '3,210.00', 'R', 1, 'R');
$pdf->Cell(120, 6, 'Debits', 'L');         $pdf->Cell(54, 6, '-1,844.45', 'R', 1, 'R');
$pdf->SetFont('dejavusans', 'B', 10);
$pdf->Cell(120, 7, 'Closing balance', 'LB'); $pdf->Cell(54, 7, '6,284.19', 'BR', 1, 'R');
$pdf->Ln(6);

$rows = [
    ['01.10', 'Opening balance', '', '4,918.64'],
    ['02.10', 'Salary NORTHWIND TRADING', '2,850.00', '7,768.64'],
    ['05.10', 'Card payment GREENLEAF MARKET', '-86.30', '7,682.34'],
    ['09.10', 'Standing order RENT', '-1,250.00', '6,432.34'],
    ['14.10', 'Card payment CITY TRANSIT', '-42.00', '6,390.34'],
    ['18.10', 'Transfer from savings', '360.00', '6,750.34'],
    ['23.10', 'Direct debit POWERGRID UTILITIES', '-118.75', '6,631.59'],
    ['27.10', 'Card payment BOOKNOOK', '-347.40', '6,284.19'],
];
$pdf->SetFont('dejavusans', 'B', 8.5);
$pdf->SetFillColor(235, 238, 242);
foreach ([[18, 'Date'], [96, 'Description'], [30, 'Amount'], [30, 'Balance']] as $i => [$w, $t]) {
    $pdf->Cell($w, 6, $t, 'B', 0, $i >= 2 ? 'R' : 'L', true);
}
$pdf->Ln();
$pdf->SetFont('dejavusans', '', 8.5);
foreach ($rows as $r) {
    $pdf->Cell(18, 6, $r[0], 'B');
    $pdf->Cell(96, 6, $r[1], 'B');
    $pdf->Cell(30, 6, $r[2], 'B', 0, 'R');
    $pdf->Cell(30, 6, $r[3], 'B', 1, 'R');
}
$pdf->Ln(8);
$pdf->SetFont('dejavusans', '', 7);
$pdf->MultiCell(0, 4, 'This is a synthetic document generated for research (SAMPLE). Riverside Savings Bank does not exist.', 0, 'L');

$pdf->Output($argv[1], 'F');
