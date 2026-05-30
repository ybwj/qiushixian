from pathlib import Path
import fitz  # PyMuPDF


def extract_text_from_pdf(pdf_path: Path) -> str:
    """
    Extract raw text from a PDF file page by page.
    """
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")

    text_pages = []

    with fitz.open(pdf_path) as doc:
        for page_index, page in enumerate(doc, start=1):
            page_text = page.get_text("text")
            text_pages.append(f"\n\n===== Page {page_index} =====\n\n{page_text}")

    return "\n".join(text_pages)


def main():
    base_dir = Path(__file__).resolve().parent

    pdf_path = base_dir / "data" / "case_report.pdf"
    output_dir = base_dir / "results"
    output_dir.mkdir(exist_ok=True)

    output_path = output_dir / "case_report_text.txt"

    extracted_text = extract_text_from_pdf(pdf_path)

    output_path.write_text(extracted_text, encoding="utf-8")

    print(f"PDF text extracted successfully.")
    print(f"Output file: {output_path}")
    print("\nPreview of extracted text:")
    print(extracted_text[:1000])


if __name__ == "__main__":
    main()