# Based on https://stackoverflow.com/a/63686095

from typing import List, Tuple
from printer import HighlightFormatter, Highlight

import fitz  # install with 'pip install pymupdf'

def parse_text_from_annotation(annot: fitz.Annot, wordlist: List[Tuple[float, float, float, float, str, int, int, int]]) -> str:
    points = annot.vertices
    quad_count = int(len(points) / 4)
    sentences = []
    for i in range(quad_count):
        # where the highlighted part is
        r = fitz.Quad(points[i * 4 : i * 4 + 4]).rect

        words = [w for w in wordlist if fitz.Rect(w[:4]).intersects(r)]
        sentences.append(" ".join(w[4] for w in words))
    sentence = " ".join(sentences)
    return sentence

def parse_highlight_from_page(page):
    wordlist = page.get_text("words")  # list of words on page
    wordlist.sort(key=lambda w: (w[3], w[0]))  # ascending y, then x
    highlights: List[Highlight] = []

    annot = page.first_annot
    while annot:
        if annot.type[1] == 'Highlight':
            annot_text = parse_text_from_annotation(annot, wordlist)
            rgb_percentages = annot.colors['stroke']
            #print(annot_text, annot.colors, sep='\n')
            highlight = Highlight(rgb_percentages, annot_text)
            highlights.append(highlight)
        print(annot.type)
        annot = annot.next
    return highlights

def parse_highlight_from_pdf(filepath: str) -> List:
    pdf = fitz.open(filepath)
    highlights = []

    for page in pdf:
        highlights += parse_highlight_from_page(page)

    return highlights


if __name__ == "__main__":
    #parse_highlight_from_pdf("Clean Code - A Handbook of Agile Software Craftsmanship.pdf")
    print(parse_highlight_from_pdf("Clean Code - A Handbook of Agile Software Craftsmanship.pdf"))
    #print('\n\n'.join(parse_highlight_from_pdf("Clean Code - A Handbook of Agile Software Craftsmanship.pdf")))
