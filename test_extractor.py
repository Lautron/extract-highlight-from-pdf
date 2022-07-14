from extractor import main

def test_main():
    filename = "test_pdf.pdf"
    md_file = "test_pdf.md"
    with open(md_file, 'r') as md:
        md_lines = md.readlines()
        extracted_lines = main(filename).split('\n')
        for md_line, extracted_line in zip(md_lines, extracted_lines):
            assert md_line.strip() == extracted_line.strip()
