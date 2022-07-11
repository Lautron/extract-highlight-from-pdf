
from printer import *

def test_hexString():
    assert str(HexStringFromPercentage(1.0)) == 'ff'
    assert str(HexStringFromPercentage(0.0)) == '00'
    assert str(HexStringFromPercentage(0.3333333432674408)) == '55'
    assert str(HexStringFromPercentage(0.6666666865348816)) == 'aa'

def _highlight(color, expected_hex):
    highlight = Highlight(color, 'test')
    assert highlight.color == expected_hex

def test_Highlight():
    test_cases = [
      ((1.0, 1.0, 0), '#ffff00'),
      ((0.3333333432674408, 0.6666666865348816, 1.0), '#55aaff')
    ]
    for color, expected_hex in test_cases:
        _highlight(color, expected_hex)

def _printer(color, text, expected_result):
    highlight = Highlight(color, text)
    printer = Printer(highlight)
    assert printer.get_formatted_text() == expected_result

def test_Printer():
    text = 'test'
    test_cases = [
      ((1.0, 1.0, 0), f'{text}'),
      ((0.3333333432674408, 0.6666666865348816, 1.0), f'# {text}')
    ]
    for color, expected_text in test_cases:
        _printer(color, text, expected_text)

