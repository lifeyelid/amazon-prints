from pypdf import PdfReader, PdfWriter, PageObject
import os
import sys
from datetime import date
import time

A4_WIDTH = 595.28
A4_HEIGHT = 841.89
SCALE = 0.48
MARGIN = 20

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def progress_bar(current, total, bar_length=40):
    """Draw a text progress bar."""
    fraction = current / total
    filled = int(fraction * bar_length)
    bar = "#" * filled + "-" * (bar_length - filled)
    percent = int(fraction * 100)
    print(f"\r[{bar}] {percent}%", end="")


def process_two_page_pdf(input_path, scale=SCALE, margin=MARGIN):
    reader = PdfReader(input_path)
    if len(reader.pages) < 2:
        print(f"\n⚠️ Skipped (not 2 pages): {os.path.basename(input_path)}")
        return None

    new_page = PageObject.create_blank_page(width=A4_WIDTH, height=A4_HEIGHT)

    # Page 1
    page1 = reader.pages[0]
    page1.scale_by(scale)
    w1, h1 = float(page1.mediabox.width), float(page1.mediabox.height)
    new_page.merge_translated_page(page1, margin, A4_HEIGHT - h1 - margin)

    # Page 2
    page2 = reader.pages[1]
    page2.scale_by(scale)
    w2, h2 = float(page2.mediabox.width), float(page2.mediabox.height)
    new_page.merge_translated_page(page2, A4_WIDTH - w2 - margin, margin)

    return new_page


def process_dragged_pdfs(pdf_paths):
    writer = PdfWriter()
    total = len(pdf_paths)

    print(f"Processing {total} PDF(s):")

    for i, path in enumerate(pdf_paths, 1):
        merged_page = process_two_page_pdf(path)
        if merged_page:
            writer.add_page(merged_page)

        # Update progress bar
        progress_bar(i, total)
        time.sleep(0.05)  # smooth visual update

    print()  # newline after progress bar

    today_str = date.today().isoformat()
    output_file = f"{today_str} amazon prints.pdf"
    output_path = os.path.join(SCRIPT_DIR, output_file)

    with open(output_path, "wb") as f:
        writer.write(f)

    print(f"✅ Done! Saved as: {output_path}")


if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print("⚠️ No PDFs dragged onto run.bat")
        input("Press Enter to exit...")
        sys.exit()

    dragged_pdfs = [x for x in sys.argv[1:] if x.lower().endswith(".pdf")]

    if not dragged_pdfs:
        print("⚠️ No PDF files detected!")
        input("Press Enter to exit...")
        sys.exit()

    process_dragged_pdfs(dragged_pdfs)
