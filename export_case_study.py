"""
Exports case-study-onboarding-emailer.md to a clean PDF.
Output: case-study-onboarding-emailer.pdf (same directory)
"""

from fpdf import FPDF
import re, os

SRC  = os.path.join(os.path.dirname(__file__), "case-study-onboarding-emailer.md")
DEST = os.path.join(os.path.dirname(__file__), "case-study-onboarding-emailer.pdf")

def sanitize(text):
    """Replace Unicode chars outside latin-1 range with ASCII equivalents."""
    return (text
        .replace("—", " - ")   # em dash
        .replace("–", " - ")   # en dash
        .replace("‘", "'")     # left single quote
        .replace("’", "'")     # right single quote
        .replace("“", '"')     # left double quote
        .replace("”", '"')     # right double quote
        .replace("…", "...")   # ellipsis
        .replace(" ", " ")     # non-breaking space
    )

with open(SRC, encoding="utf-8") as f:
    lines = [sanitize(l) for l in f.readlines()]


class PDF(FPDF):
    def header(self):
        pass

    def footer(self):
        self.set_y(-12)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

    def write_line(self, text, indent=0):
        """Write a line, handling **bold** inline markers."""
        self.set_x(self.l_margin + indent)
        parts = re.split(r"(\*\*[^*]+\*\*)", text)
        for part in parts:
            if part.startswith("**") and part.endswith("**"):
                self.set_font("Helvetica", "B", self.font_size_pt)
                self.write(6, part[2:-2])
            else:
                self.set_font("Helvetica", "", self.font_size_pt)
                self.write(6, part)
        self.ln()


pdf = PDF()
pdf.set_margins(22, 20, 22)
pdf.add_page()
pdf.set_auto_page_break(auto=True, margin=20)

i = 0
while i < len(lines):
    raw = lines[i].rstrip("\n")
    stripped = raw.strip()

    # ── H1
    if stripped.startswith("# ") and not stripped.startswith("## "):
        pdf.set_font("Helvetica", "B", 20)
        pdf.set_text_color(20, 20, 20)
        pdf.ln(2)
        pdf.multi_cell(0, 9, stripped[2:])
        pdf.ln(4)

    # ── H2
    elif stripped.startswith("## "):
        pdf.ln(5)
        pdf.set_font("Helvetica", "B", 13)
        pdf.set_text_color(40, 40, 40)
        pdf.multi_cell(0, 7, stripped[3:])
        # underline via thin line
        pdf.set_draw_color(200, 200, 200)
        y = pdf.get_y()
        pdf.line(pdf.l_margin, y, pdf.w - pdf.r_margin, y)
        pdf.ln(4)

    # ── HR
    elif stripped == "---":
        pdf.ln(2)
        pdf.set_draw_color(220, 220, 220)
        y = pdf.get_y()
        pdf.line(pdf.l_margin, y, pdf.w - pdf.r_margin, y)
        pdf.ln(4)

    # ── Table header row (| --- |)
    elif re.match(r"^\|[-| :]+\|$", stripped):
        pass  # skip separator row

    # ── Table row
    elif stripped.startswith("|") and stripped.endswith("|"):
        cells = [c.strip() for c in stripped.strip("|").split("|")]
        # detect if header (previous line was also a table row — handled below)
        col_w = (pdf.w - pdf.l_margin - pdf.r_margin) / len(cells)
        # check if next line is a separator → this is the header row
        next_stripped = lines[i + 1].strip() if i + 1 < len(lines) else ""
        is_header = bool(re.match(r"^\|[-| :]+\|$", next_stripped))
        pdf.set_font("Helvetica", "B" if is_header else "", 9)
        pdf.set_text_color(20, 20, 20)
        if is_header:
            pdf.set_fill_color(240, 240, 240)
        else:
            pdf.set_fill_color(255, 255, 255)
        for cell in cells:
            pdf.cell(col_w, 7, cell, border=1, fill=True)
        pdf.ln()

    # ── Blockquote
    elif stripped.startswith(">"):
        content = stripped.lstrip("> ").strip()
        if content:
            pdf.set_font("Helvetica", "I", 9.5)
            pdf.set_text_color(80, 80, 80)
            pdf.set_x(pdf.l_margin + 6)
            # left bar
            x = pdf.l_margin + 2
            y0 = pdf.get_y()
            pdf.multi_cell(pdf.w - pdf.l_margin - pdf.r_margin - 6, 5.5, content)
            y1 = pdf.get_y()
            pdf.set_draw_color(180, 180, 180)
            pdf.line(x, y0, x, y1)

    # ── Bullet point
    elif stripped.startswith("- "):
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(20, 20, 20)
        content = stripped[2:]
        pdf.set_x(pdf.l_margin + 4)
        pdf.write(6, "-  ")
        pdf.write_line(content, indent=4)
        pdf.ln(1)

    # ── Italic line (e.g. *Results based on...*)
    elif stripped.startswith("*") and stripped.endswith("*") and not stripped.startswith("**"):
        pdf.set_font("Helvetica", "I", 9)
        pdf.set_text_color(100, 100, 100)
        pdf.multi_cell(0, 5, stripped.strip("*"))
        pdf.ln(1)

    # ── Bold+link footer line
    elif stripped.startswith("*Built by"):
        pdf.ln(4)
        pdf.set_font("Helvetica", "I", 9)
        pdf.set_text_color(100, 100, 100)
        clean = re.sub(r"\*", "", stripped)
        pdf.multi_cell(0, 5, clean)

    # ── Empty line
    elif stripped == "":
        pdf.ln(2)

    # ── Normal paragraph text
    else:
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(20, 20, 20)
        pdf.write_line(stripped)
        pdf.ln(2)

    i += 1

pdf.output(DEST)
print(f"PDF saved: {DEST}")
