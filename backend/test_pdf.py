import pdfplumber
import sys

pdf_path = sys.argv[1] if len(sys.argv) > 1 else "test.pdf"

with pdfplumber.open(pdf_path) as pdf:
    for page_num, page in enumerate(pdf.pages, 1):
        print(f"\n=== Page {page_num} ===")
        tables = page.extract_tables()
        print(f"Found {len(tables)} tables")
        
        for idx, table in enumerate(tables):
            print(f"\n--- Table {idx} ---")
            print(f"Rows: {len(table)}")
            if table:
                print("First 3 rows:")
                for row in table[:3]:
                    print(row)
