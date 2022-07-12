
class Highlight:
    def __init__(self, color, text):
        self.text = text
        self._set_hex_color_from_rgb_tuple(color)

    def _set_hex_color_from_rgb_tuple(self, color):
        rgb_hex_values: list = [HexStringFromPercentage(percentage) for percentage in color]
        self.color = '#' + "".join([str(hex_code) for hex_code in rgb_hex_values])

class HexStringFromPercentage:
    def __init__(self, percentage):
        self.percentage = percentage
        self._set_formatted_hex_code()

    def _set_formatted_hex_code(self):
        self._get_hex_code_from_percentage(self.percentage)
        self._remove_prefix_from_hex_num()
        self._add_leading_zero_if_necessary()

    def _get_hex_code_from_percentage(self, num):
        self.hex_code = hex(round(num * 255))

    def _remove_prefix_from_hex_num(self):
        self.hex_code = self.hex_code.replace('0x', '')

    def _add_leading_zero_if_necessary(self):
        self.hex_code = self.hex_code if len(self.hex_code) == 2 else '0' + self.hex_code

    def __str__(self):
        return self.hex_code

class Printer:
    template_by_color = {
            '#55aaff': "# {}",
            '#ffff01': "## {}",
            '#ffff02': "### {}",
    }
    def __init__(self, highlight):
        self.color = highlight.color
        self.text = highlight.text

    def get_formatted_text(self):
        template = self.template_by_color.get(self.color, '{}')
        return template.format(self.text)


