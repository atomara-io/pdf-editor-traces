"""What a PDF editor left in a file. Usage: python editor_traces.py file.pdf [original.pdf]

pip install pikepdf pymupdf
"""
import re
import sys
from collections import Counter

import pikepdf
import pymupdf

AMOUNT = re.compile(r"-?\$?\d[\d,]*\.\d\d\b")
EDITOR_MARKS = [b"/IceniCID", b"/TouchUp_TextEdit", b"EmbeddedPdfPage", b"/APDE_"]


def amounts(data: bytes) -> list[str]:
    doc = pymupdf.open(stream=data, filetype="pdf")
    return AMOUNT.findall(" ".join(page.get_text() for page in doc))


def page_bytes(pdf: pikepdf.Pdf) -> bytes:
    out = b""
    for page in pdf.pages:
        contents = page.obj.get("/Contents")
        streams = [contents] if isinstance(contents, pikepdf.Stream) else list(contents or [])
        out += b"".join(s.read_bytes() for s in streams)
        resources = page.obj.get("/Resources") or {}
        for kind in ("/Font", "/XObject"):
            out += b" ".join(str(k).encode() for k in (resources.get(kind) or {}).keys())
    return out


path = sys.argv[1]
raw = open(path, "rb").read()
pdf = pikepdf.open(path)
info = {k: str(v) for k, v in (pdf.docinfo or {}).items()}

print("header      ", raw[:8].decode("latin-1").strip())
print("producer    ", info.get("/Producer"), "| creator", info.get("/Creator"))
print("dates       ", info.get("/CreationDate"), "->", info.get("/ModDate"))

eofs = [m.end() for m in re.finditer(rb"%%EOF", raw)]
linearized = b"/Linearized" in raw[:2048]  # "fast web view" files end twice by design
print("revisions   ", len(eofs), "(linearized)" if linearized else "")
if len(eofs) > 1 and not linearized:  # an incremental save: the earlier file is still in the bytes
    first, last = amounts(raw[: eofs[0]]), amounts(raw)
    print("  revision 1 amounts:", first if first != last else "same as the final file")

body = page_bytes(pdf)
print("editor marks", [m.decode() for m in EDITOR_MARKS if m in body])
print("fonts       ", sorted({f[3] for page in pymupdf.open(path) for f in page.get_fonts()}))
print("amounts     ", amounts(raw))  # text under a white box is still text

if len(sys.argv) > 2:  # compare with the file as issued
    before, after = Counter(amounts(open(sys.argv[2], "rb").read())), Counter(amounts(raw))
    print("  gone:", list((before - after).elements()))
    print("  new: ", list((after - before).elements()))
