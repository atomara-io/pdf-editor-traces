# PDF Editor Traces

What a PDF editor leaves in a file after one number is changed.

Seven synthetic documents, the same kind of edit in each of 18 tools (17 online editors and desktop Word), 109 edited files, and a per-file record of what changed besides the number. Collected by hand between 11 and 16 November 2026.

**Write-up:** [What 18 PDF editors leave in a file after one edited number](https://atomara.io/blog/pdf-editor-traces) (atomara.io)

Every document here is invented and marked SAMPLE. The banks, companies and people in them do not exist.

## What is in the repository

```
originals/              the 7 documents as generated
originals/generators/   the code that generated them
edited/<editor>/<original>.pdf   the same document after an edit in that editor
results/traces.csv      one row per edited file
tools/editor_traces.py  prints what an editor left in one file
tools/build_dataset.py  the script that built this dataset (shown for transparency; it reads our working folder)
SHA256SUMS
```

| Original | Made with |
|---|---|
| `statement` | ReportLab (bank statement) |
| `receipt` | headless Chrome from HTML (payment receipt) |
| `invoice` | Apple Numbers, Export to PDF |
| `tcpdf` | TCPDF 6.11, PHP (bank statement) |
| `mpdf` | mPDF 8.3, PHP (invoice) |
| `weasy` | WeasyPrint 70, Python (receipt) |
| `fpdf2` | fpdf2 2.9, Python (payslip) |

## Method

In each editor one amount was changed (the closing balance, the total due, the net pay), usually together with the figure that feeds it, using the editor's edit-text function where it had one. The result was downloaded and left untouched. The new figures differ between editors, so compare each edited file with its original, not with another editor's file.

`results/traces.csv` records for each file: the PDF header, the number of revisions, whether the original amount is still readable in the first revision or in the text layer, the Producer, whether Producer, CreationDate and ModDate equal the original's, editor marks found in page content and resources (`/IceniCID`, `/TouchUp_TextEdit`, `EmbeddedPdfPage`, `/APDE_`), fonts the editor added, and the file's SHA-256.

## Results by editor

Counts are files out of that editor's files. "Kept" means equal to the original's value, including a field that is absent in both (the `fpdf2` original has no Producer and no ModDate; the `weasy` original has no dates).

| Editor | Files | Revisions > 1 | Producer kept | CreationDate kept | ModDate kept | Old amount in revision 1 | Old amount in text layer | Marks | PDF header |
|---|---|---|---|---|---|---|---|---|---|
| acrobat-online | 7 | 7/7 | 7/7 | 7/7 | 0/7 | 7/7 | 0/7 | `/TouchUp_TextEdit` 4/7 | 1.3, 1.4, 1.7 |
| canva | 7 | 0/7 | 0/7 | 0/7 | 0/7 | 0/7 | 0/7 | — | 1.4, 1.7 |
| docfly | 6 | 0/6 | 0/6 | 2/6 | 0/6 | 0/6 | 6/6 | — | 1.5, 1.7 |
| dochub | 5 | 0/5 | 0/5 | 0/5 | 0/5 | 0/5 | 0/5 | — | 1.7 |
| hipdf | 1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 0/1 | — | 1.3 |
| ilovepdf | 7 | 0/7 | 7/7 | 7/7 | 7/7 | 0/7 | 0/7 | `/IceniCID` 7/7 | 1.7 |
| lightpdf | 5 | 0/5 | 5/5 | 5/5 | 5/5 | 0/5 | 0/5 | `/APDE_` 5/5 | 1.3, 1.4, 1.7 |
| lumin | 1 | 0/1 | 1/1 | 1/1 | 1/1 | 0/1 | 0/1 | `/IceniCID` 1/1 | 1.7 |
| pdf-candy | 7 | 0/7 | 0/7 | 0/7 | 0/7 | 0/7 | 0/7 | — | 1.7 |
| pdf2go | 7 | 0/7 | 0/7 | 6/7 | 0/7 | 0/7 | 7/7 | `EmbeddedPdfPage` 7/7 | 1.7 |
| pdfbear | 7 | 0/7 | 7/7 | 7/7 | 7/7 | 0/7 | 0/7 | — | 1.3, 1.4, 1.7 |
| pdfescape | 7 | 0/7 | 7/7 | 7/7 | 7/7 | 0/7 | 0/7 | — | 2.0 |
| pdffiller | 7 | 0/7 | 0/7 | 0/7 | 0/7 | 0/7 | 0/7 | — | 1.7 |
| sejda | 7 | 0/7 | 0/7 | 7/7 | 0/7 | 0/7 | 0/7 | — | 1.5, 1.7 |
| smallpdf | 7 | 0/7 | 7/7 | 7/7 | 7/7 | 0/7 | 0/7 | `/IceniCID` 7/7 | 1.7 |
| tinywow | 7 | 0/7 | 0/7 | 0/7 | 0/7 | 0/7 | 2/7 | — | 1.7 |
| word | 7 | 7/7 | 0/7 | 0/7 | 0/7 | 0/7 | 0/7 | — | 1.7 |
| xodo | 7 | 0/7 | 7/7 | 7/7 | 7/7 | 0/7 | 0/7 | `/IceniCID` 7/7 | 1.7 |

Notes:

- Word's files end with two `%%EOF` markers, but the first part holds the same text as the whole file: it is how Word writes a PDF, not an earlier version of the document.
- "Old amount in text layer" means the original figure can still be extracted from the page although the page shows the new one (the editor drew over it).
- HiPDF and Lumin have one file each.
- In the files with `/IceniCID`, the general Iceni tagging (`/IceniObject`) wraps the whole page (29 to 84 objects per file) and shows only that the file went through the editor. The `/IceniCID <</CI 1>>` runs sit only where figures were edited, two to four per file.
- More than one `%%EOF` does not by itself mean an edit; check that the earlier part holds different content.

## Run it

```bash
pip install pikepdf pymupdf
python tools/editor_traces.py edited/smallpdf/statement.pdf originals/statement.pdf
python tools/editor_traces.py edited/pdf2go/statement.pdf originals/statement.pdf
shasum -a 256 -c SHA256SUMS
```

## What is not published

- **Two real invoices.** The same edits were also made on two genuine invoices. They carry personal data, so the files are not here. Their measurements are in `traces.csv` as rows with `published = no` (original `real-stripe` and `real-apple`), without free-text values.
- **An unedited pass through each editor.** There is no "open and download without editing" control for the online editors, so this dataset cannot separate what an edit leaves from what any pass through the tool leaves.

## Personal data in the files

Two editors write the account that made the edit into the file. Canva puts the account holder's name in `/Author` and XMP `dc:creator`, with design identifiers in `/Keywords`. pdfFiller adds `/Owner` with the account e-mail, a `/DocumentID` and a `/reupload` value. DocHub adds a `dochub.document.id`. Those values are published as the editors wrote them, by the dataset owner's decision, because removing them would itself be an edit.

## Limits

One week, free tiers, a browser on macOS, edits made by hand. Online editors change their back ends without notice; this is how they behaved in November 2026. Version 1 covers online editors and Word. Desktop editors, mobile apps and AI editors are planned as later versions.

## License

- The original documents, `results/traces.csv` and this README: [CC BY 4.0](LICENSE). Credit "Atomara" and link to https://atomara.io/blog/pdf-editor-traces.
- The scripts in `tools/` and `originals/generators/`: [MIT](LICENSE-CODE).
- The files in `edited/` are the output of third-party services applied to our documents. They are provided as is, for research; we claim no rights in what those services added (embedded fonts, watermarks, metadata).

## How to cite

> Haiduchyk, B. (Atomara) (2026). *PDF Editor Traces: one edited figure, 18 PDF editors* (version 1.0.0) [Data set]. https://atomara.io/blog/pdf-editor-traces

See also [`CITATION.cff`](CITATION.cff).
