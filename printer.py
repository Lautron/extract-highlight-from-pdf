from config import Config
from typing import Tuple
import fitz  # install with 'pip install pymupdf'

class HexStringFromPercentage:
    def __init__(self, percentage: float):
        self.percentage: float = percentage
        self._set_formatted_hex_code()

    def _set_formatted_hex_code(self) -> None:
        self._calculate_hex_code_from_percentage(self.percentage)
        self._remove_prefix_from_hex_num()
        self._add_leading_zero_if_necessary()

    def _calculate_hex_code_from_percentage(self, percentage: float) -> None:
        self.hex_code: str = hex(round(percentage * 255))

    def _remove_prefix_from_hex_num(self) -> None:
        self.hex_code: str = self.hex_code.replace('0x', '')

    def _add_leading_zero_if_necessary(self) -> None:
        self.hex_code: str = self.hex_code if len(self.hex_code) == 2 else '0' + self.hex_code

    def __str__(self):
        return self.hex_code

class Word:
    def __init__(self, word:Tuple[float, float, float, float, str, int, int, int]):
        self.rect = fitz.Rect(word[:4])
        self.text = word[4]

    def __str__(self):
        return self.text

class HighlightLine:
    MIN_INTERSECTION_HEIGHT = 1.5

    def __init__(self, vertices):
        self.vertices = vertices
        self.rect = fitz.Quad(vertices).rect # TODO check

    def __contains__(self, item):
        return self.is_word_in_line(item.rect)

    def is_word_in_line(self, rect): 
        return self.rect.intersects(rect) and self.is_valid_intersection_height(rect)

    def is_valid_intersection_height(self, rect): 
        return abs(self.rect.y1 - rect.y0) > self.MIN_INTERSECTION_HEIGHT

class Highlight:
    def __init__(self, color: tuple[float, float, float], text: str):
        self.text: str = text
        self._set_hex_color_from_rgb(color)

    def _set_hex_color_from_rgb(self, color: tuple[float, float, float]) -> None:
        rgb_hex_values: list = [str(HexStringFromPercentage(percentage)) for percentage in color]
        self.color: str = '#' + "".join(rgb_hex_values)

    def __repr__(self):
        return f"Highlight(color='{self.color}', text='{self.text}')"

class HighlightFormatter:
    template_by_color: dict[str, str] = Config.string_template_by_color

    def __init__(self, highlight: Highlight):
        self.color: str = highlight.color
        self.text: str = highlight.text

    def format(self) -> str:
        template = self.template_by_color.get(self.color, '{}')
        return template.format(self.text)

    def __str__(self):
        return self.format()

