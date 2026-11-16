"""Build the public dataset (atomara-io/pdf-editor-traces) from the working folder.

Usage: build_dataset.py --src <experiment folder> --out <dataset clone> [--include-canva]

Copies the synthetic originals and the edited files under normalised names, writes
results/traces.csv and SHA256SUMS, then runs gate(): any real invoice or forbidden
string in the output is exit code 1, never a warning. The owner's real invoices are
measured (published=no rows) and never copied.

Forbidden strings live outside every repository, in <src>/forbidden.txt:
one regex per line; "allow <editor>: <regex>" exempts a match in that editor's files.
"""
import argparse
import collections
import csv
import glob
import hashlib
import os
import re
import shutil
import sys

import pikepdf
import pymupdf

TOOLS = os.path.dirname(os.path.abspath(__file__))
AMOUNT = re.compile(r"-?\$?\d[\d,]*\.\d\d\b")
MARKS = [b"/IceniCID", b"/TouchUp_TextEdit", b"EmbeddedPdfPage", b"/APDE_"]
SYNTHETIC = ["statement", "receipt", "invoice", "tcpdf", "mpdf", "weasy", "fpdf2"]
REAL = ["real-stripe", "real-apple"]
EDITORS = {
    "AcrobatOnline": "acrobat-online", "Canva": "canva", "DocFly": "docfly", "DocHub": "dochub",
    "HiPDF": "hipdf", "LightPDF": "lightpdf", "Lumin": "lumin", "PDF2Go": "pdf2go",
    "PDFBear": "pdfbear", "PDFCandy": "pdf-candy", "PDFescape": "pdfescape", "Sejda": "sejda",
    "Smallpdf": "smallpdf", "TinyWow": "tinywow", "Xodo": "xodo", "iLovePDF": "ilovepdf",
    "pdfFiller": "pdffiller", "Word": "word",
}
GENERATORS = ["make_genuine.py", "receipt.html", "invoice.applescript", "tcpdf_statement.php",
              "mpdf_invoice.php", "weasy_receipt.py", "fpdf_payslip.py"]
COLUMNS = ["editor", "original", "published", "file", "bytes", "pdf_header", "revisions",
           "old_amount_in_revision_1", "old_amount_in_text_layer", "producer", "producer_kept",
           "creation_date_kept", "mod_date_kept", "editor_marks", "fonts_added", "sha256"]


def amounts(data: bytes) -> collections.Counter:
    try:
        doc = pymupdf.open(stream=data, filetype="pdf")
        return collections.Counter(AMOUNT.findall(" ".join(p.get_text() for p in doc)))
    except Exception:
        return collections.Counter()


def info(pdf: pikepdf.Pdf) -> dict:
    return {k: str(v) for k, v in (pdf.docinfo or {}).items()}


def page_bytes(pdf: pikepdf.Pdf) -> bytes:
    out = b""
    for page in pdf.pages:
        contents = page.obj.get("/Contents")
        streams = [contents] if isinstance(contents, pikepdf.Stream) else list(contents or [])
        for s in streams:
            try:
                out += s.read_bytes()
            except Exception:
                pass
        res = page.obj.get("/Resources") or {}
        for kind in ("/Font", "/XObject"):
            out += b" ".join(str(k).encode() for k in (res.get(kind) or {}).keys())
    return out


def fonts(path: str) -> set:
    return {re.sub(r"^[A-Z]{6}\+", "", f[3]) for page in pymupdf.open(path) for f in page.get_fonts()}


def yes(flag: bool) -> str:
    return "yes" if flag else "no"


def measure(path: str, original: str) -> dict:
    raw, raw_o = open(path, "rb").read(), open(original, "rb").read()
    pdf, pdf_o = pikepdf.open(path), pikepdf.open(original)
    i, o = info(pdf), info(pdf_o)
    before, after = amounts(raw_o), amounts(raw)
    gone, new = before - after, after - before
    eofs = [m.end() for m in re.finditer(rb"%%EOF", raw)]
    linearized = b"/Linearized" in raw[:2048]
    first = amounts(raw[: eofs[0]]) if len(eofs) > 1 and not linearized else None
    old_in_rev1 = bool(first is not None and ((first - after) & before))
    # text under a painted box is still text: figures were added (or one digit drawn) and none left
    old_in_text = not gone and (bool(new) or raw != raw_o)
    body = page_bytes(pdf)
    return {
        "bytes": len(raw), "pdf_header": raw[:8].decode("latin-1").strip(),
        "revisions": 1 if linearized else len(eofs),
        "old_amount_in_revision_1": yes(old_in_rev1), "old_amount_in_text_layer": yes(old_in_text),
        "producer": (i.get("/Producer") or "").strip(),
        "producer_kept": yes(i.get("/Producer") == o.get("/Producer")),
        "creation_date_kept": yes(i.get("/CreationDate") == o.get("/CreationDate")),
        "mod_date_kept": yes(i.get("/ModDate") == o.get("/ModDate")),
        "editor_marks": " ".join(m.decode() for m in MARKS if m in body),
        "fonts_added": " ".join(sorted(fonts(path) - fonts(original))),
        "sha256": hashlib.sha256(raw).hexdigest(),
    }


def sources(src: str) -> list:
    """(editor slug, original, source path) for the canonical set, duplicates dropped."""
    found = {}
    dirs = sorted(glob.glob(os.path.join(src, "3-web-editors", "*"))) + [os.path.join(src, "4-desktop", "Word")]
    for d in dirs:
        key = os.path.basename(d).split(" ")[0]
        if key not in EDITORS:
            continue
        for f in sorted(glob.glob(os.path.join(glob.escape(d), "*.pdf"))):
            original = re.sub(r"^tinywow_", "", os.path.basename(f)).split("-00-")[0]
            if original not in SYNTHETIC + REAL:
                sys.exit(f"unknown original in {f}")
            found.setdefault((EDITORS[key], original), f)  # sorted: " (1)" wins over " (2)"
    return [(e, o, f) for (e, o), f in sorted(found.items())]


def searchable(path: str) -> str:
    """Everything a reader could find in the file: raw bytes, Info, XMP, annotations, page text."""
    raw = open(path, "rb").read()
    parts = [raw.decode("latin-1"), raw.decode("utf-16-be", "ignore")]
    try:
        pdf = pikepdf.open(path)
        parts += [f"{k}={v}" for k, v in info(pdf).items()]
        with pdf.open_metadata() as m:
            parts += [f"{k}={m[k]}" for k in m]
        for page in pdf.pages:
            for a in page.obj.get("/Annots") or []:
                parts += [str(a.get(k)) for k in ("/T", "/Contents") if a.get(k) is not None]
        parts.append(page_bytes(pdf).decode("latin-1"))
        parts += [p.get_text() for p in pymupdf.open(path)]
    except Exception as e:
        parts.append(f"<unreadable {e}>")
    return "\n".join(parts)


def gate(out: str, forbidden_file: str, expect_edited: int) -> list:
    problems = []
    if not os.path.exists(forbidden_file):
        return [f"missing {forbidden_file}: the gate cannot run without it"]
    forbid, allow = [], collections.defaultdict(list)
    for line in open(forbidden_file, encoding="utf-8"):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        m = re.match(r"allow\s+([\w-]+):\s*(.+)", line)
        if m:
            allow[m.group(1)].append(re.compile(m.group(2), re.I))
        else:
            forbid.append(re.compile(line, re.I))
    files = [f for f in glob.glob(os.path.join(out, "**", "*"), recursive=True)
             if os.path.isfile(f) and "/.venv/" not in f and "/.git/" not in f]
    for f in files:
        rel = os.path.relpath(f, out)
        if "real-" in rel:
            problems.append(f"real invoice in output: {rel}")
        text = searchable(f) if f.endswith(".pdf") else open(f, errors="ignore").read()
        editor = rel.split(os.sep)[1] if rel.startswith("edited" + os.sep) else ""
        for a in allow.get(editor, []):
            text = a.sub("", text)
        for pattern in forbid:
            if pattern.search(text):
                problems.append(f"forbidden /{pattern.pattern}/ in {rel}")
    n_orig = len(glob.glob(os.path.join(out, "originals", "*.pdf")))
    n_edit = len(glob.glob(os.path.join(out, "edited", "*", "*.pdf")))
    if n_orig != 7:
        problems.append(f"originals: {n_orig}, expected 7")
    if n_edit != expect_edited:
        problems.append(f"edited: {n_edit}, expected {expect_edited}")
    return problems


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--include-canva", action="store_true")
    ap.add_argument("--gate-only", action="store_true", help="check an existing output folder")
    args = ap.parse_args()
    expect = 109 if args.include_canva else 102
    forbidden = os.path.join(args.src, "forbidden.txt")

    if not args.gate_only:
        for sub in ("originals", "edited", "results", "tools"):
            path = os.path.join(args.out, sub)
            if os.path.isdir(path):
                shutil.rmtree(path)  # generated subfolders of the dataset clone only
            os.makedirs(path)
        os.makedirs(os.path.join(args.out, "originals", "generators"))
        for o in SYNTHETIC:
            shutil.copy(os.path.join(args.src, "1-originals", f"{o}-00-genuine.pdf"),
                        os.path.join(args.out, "originals", f"{o}.pdf"))
        for g in GENERATORS:
            shutil.copy(os.path.join(TOOLS, g), os.path.join(args.out, "originals", "generators", g))
        shutil.copy(os.path.join(TOOLS, "..", "..", "devto", "snippets", "editor_traces.py"),
                    os.path.join(args.out, "tools", "editor_traces.py"))
        shutil.copy(os.path.abspath(__file__), os.path.join(args.out, "tools", "build_dataset.py"))

        rows = []
        for editor, original, f in sources(args.src):
            row = {"editor": editor, "original": original}
            row.update(measure(f, os.path.join(args.src, "1-originals", f"{original}-00-genuine.pdf")))
            publish = original in SYNTHETIC and (editor != "canva" or args.include_canva)
            row["published"] = yes(publish)
            if publish:
                row["file"] = f"edited/{editor}/{original}.pdf"
                os.makedirs(os.path.join(args.out, "edited", editor), exist_ok=True)
                shutil.copy(f, os.path.join(args.out, row["file"]))
            else:  # nothing free-text from an unpublished file
                row.update({"file": "", "sha256": "", "producer": "", "fonts_added": ""})
            rows.append(row)
        with open(os.path.join(args.out, "results", "traces.csv"), "w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=COLUMNS)
            w.writeheader()
            w.writerows(rows)
        with open(os.path.join(args.out, "SHA256SUMS"), "w") as fh:
            for f in sorted(glob.glob(os.path.join(args.out, "originals", "*.pdf"))
                            + glob.glob(os.path.join(args.out, "edited", "*", "*.pdf"))):
                fh.write(f"{hashlib.sha256(open(f, 'rb').read()).hexdigest()}  {os.path.relpath(f, args.out)}\n")
        print(f"rows {len(rows)}, published {sum(r['published'] == 'yes' for r in rows)}")

    problems = gate(args.out, forbidden, expect)
    for p in problems:
        print("GATE:", p)
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
