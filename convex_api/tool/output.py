"""


    Starfish Tool Output

"""
import json
from typing import Union


class Output:
    def __init__(self):
        self._line_list: list[str] = []
        self._values: dict[str, Union[str, int]] = {}
        self._error_list: list[str] = []

    def add_error(self, line: str):
        self._error_list.append(line)

    def add_line(self, line: str):
        self._line_list.append(line)

    def add_line_values(self, values: dict[str, Union[str, int]]):
        for name, value in values.items():
            self.add_line(f'{name}: {value}')

    def set_value(self, key: str, value: Union[str, int]):
        self._values[key] = value

    def set_values(self, values: dict[str, Union[str, int]]):
        for name, value in values.items():
            self.set_value(name, value)

    def printout(self, is_json: bool):
        if self.has_errors:
            error_lines = '\nError: '. join(self.errors)
            print(f'Error: {error_lines}')
            return

        if is_json:
            if self.has_values:
                print(json.dumps(self.values, sort_keys=True, indent=2))
        else:
            if self.has_lines:
                print('\n'.join(self.lines))

    @property
    def errors(self):
        return self._error_list

    @property
    def has_errors(self):
        return len(self._error_list) > 0

    @property
    def lines(self):
        return self._line_list

    @property
    def has_lines(self):
        return len(self._line_list) > 0

    @property
    def values(self):
        return self._values

    @property
    def has_values(self):
        return len(self._values.keys()) > 0
