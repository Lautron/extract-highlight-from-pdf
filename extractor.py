# Based on https://stackoverflow.com/a/63686095

from typing import List, Tuple
from printer import HighlightFormatter, Highlight, Word

import fitz  # install with 'pip install pymupdf'

def parse_text_from_annotation(highlight: Highlight, page_words: List[Word]) -> str:
    highlight_lines = highlight.get_highlight_lines()
    sentences = []

    for line in highlight_lines:
        line_words = []
        for word in page_words:
            if word in line:
                line_words.append(str(word))

        sentence = " ".join(line_words)
        sentences.append(sentence)

    text = " ".join(sentences)

    return text

def get_annots_from_page(page):
    annots = []
    annot = page.first_annot

    while annot:
        annots.append(annot)
        annot = annot.next

    return annots

def parse_highlight_from_page(page):
    wordlist = page.get_text("words")  # list of words on page
    wordlist.sort(key=lambda w: (w[3], w[0]))  # ascending y, then x
    words = [Word(word) for word in wordlist]
    highlights: List[Highlight] = []

    annots = get_annots_from_page(page)
    annots.sort(key=lambda w: (w.vertices[0][0], w.vertices[0][1]))

    for annot in annots:
        if annot.type[1] == 'Highlight':
            annot_text = parse_text_from_annotation(annot, wordlist)
            rgb_percentages = annot.colors['stroke']
            highlight = Highlight(rgb_percentages, annot_text)
            highlights.append(highlight)
    return highlights

def parse_highlight_from_pdf(filepath: str) -> List:
    pdf = fitz.open(filepath)
    highlights = []

    for page in pdf:
        highlights += parse_highlight_from_page(page)

    return highlights

def format_highlights(highlights: list[Highlight]) -> list[str]:
    return [str(HighlightFormatter(highlight)) for highlight in highlights]

def format_output_text(highlights: list[Highlight]) -> str:
    formatted_highlights = format_highlights(highlights)
    return "\n".join(formatted_highlights).strip('\n')

def main(filename):
    highlight = parse_highlight_from_pdf(filename)
    formatted_highlight = format_output_text(highlight)
    return formatted_highlight

if __name__ == "__main__":
    print(main("test_pdf.pdf"))
