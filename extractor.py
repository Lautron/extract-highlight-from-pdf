# Based on https://stackoverflow.com/a/63686095

from typing import List, Tuple
from printer import HighlightFormatter, Highlight

import fitz  # install with 'pip install pymupdf'

def parse_text_from_annotation(annot: fitz.Annot, wordlist: List[Tuple[float, float, float, float, str, int, int, int]]) -> str:
    points = annot.vertices
    quad_count = int(len(points) / 4)
    MIN_INTERSECTION_HEIGHT = 1.5
    words = []
    sentences = []
    valid_intersection_height = lambda r1, r2: (abs(r1.y1 - r2.y0) > MIN_INTERSECTION_HEIGHT)
    is_word_highlighted = lambda r1, r2: r1.intersects(r2) and valid_intersection_height(r1, r2)
    for i in range(quad_count):
        # where the highlighted part is
        r = fitz.Quad(points[i * 4 : i * 4 + 4]).rect

        words = [w for w in wordlist if is_word_highlighted(r, fitz.Rect(w[:4]))]

        sentences.append(" ".join(w[4] for w in words))
    sentence = " ".join(sentences)
    return sentence

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
    return "\n".join(formatted_highlights)

if __name__ == "__main__":
    #format_output_text(parse_highlight_from_pdf("test_pdf.pdf"))
    print(format_output_text(parse_highlight_from_pdf("test_pdf.pdf")))
    #print('\n\n'.join(parse_highlight_from_pdf("Clean Code - A Handbook of Agile Software Craftsmanship.pdf")))
