
from printer import *

class FakeHighlight(Highlight):
    def __init__(self):
        pass
        
def test_hexString():
    assert str(HexStringFromPercentage(1.0)) == 'ff'
    assert str(HexStringFromPercentage(0.0)) == '00'
    assert str(HexStringFromPercentage(0.3333333432674408)) == '55'
    assert str(HexStringFromPercentage(0.6666666865348816)) == 'aa'

def _highlight(color, expected_hex):
    highlight = FakeHighlight()
    highlight.rgb_percentages = color
    highlight._set_hex_color_from_rgb()
    assert highlight.color == expected_hex

def test_Highlight():
    test_cases = [
      ((1.0, 0.6666666865348816, 1.0), '#ffaaff'),
      ((0.3333333432674408, 1.0, 1.0), '#55ffff'),
      ((0.0, 1.0, 0.0), '#00ff00'),
      ((0.3333333432674408, 0.6666666865348816, 1.0), '#55aaff'),
      ((1.0, 1.0, 0), '#ffff00'),
    ]
    for color, expected_hex in test_cases:
        _highlight(color, expected_hex)

def _printer(color, text, expected_result):
    highlight = FakeHighlight()
    highlight.rgb_percentages = color
    highlight._set_hex_color_from_rgb()
    highlight.text = text

    printer = HighlightFormatter(highlight)

    assert printer.format() == expected_result

def test_Printer():
    text = 'test'
    test_cases = [
      ((1.0, 0.6666666865348816, 1.0),                f'\n# {text}'),
      ((0.3333333432674408, 1.0, 1.0),                f'\n## {text}'),
      ((0.0, 1.0, 0.0),                               f'\n### {text}'),
      ((0.3333333432674408, 0.6666666865348816, 1.0), f'\n#### {text}'),
      ((1.0, 1.0, 0), f'{text}'),
    ]
    for color, expected_text in test_cases:
        _printer(color, text, expected_text)

