import sys
import json
import os
import traceback


class JSONHandler:

    __slots__ = ['_text', '_tag_length', 'is_json']

    def __init__(self, json_text):
        self._text = json_text
        self._tag_length = dict()
        self.is_json = self._correct_form

    @property
    def _correct_form(self):
        if type(self._text) != list or len(self._text) == 0:
            return False

        is_dicts = all(map(lambda subpackage: isinstance(subpackage, dict), self._text))
        if not is_dicts:
            return False

        title = self._text[0]
        print(f"Title -> {title}")
        tags = tuple(title.keys())
        print((f"Tag -> {tags}"))

        for contain in self._text:
            for key in tags:
                print(f"Key -> {key}")
                print(f"Contain -> {contain[key]}")
                print(f"Type -> {type(contain[key])}")

                cur_len = len(str(contain[key]))

                try:
                    if cur_len > self._tag_length[key]:
                        self._tag_length[key] = cur_len
                except KeyError:
                    self._tag_length.update({key: len(key)})

        print("CONTAIN")
        print(self._tag_length)

        return True

    def pretty_print(self):
        if not self.is_json:
            return

        separator = '|'
        separator_len = sum(self._tag_length.values()) + len(self._tag_length.values()) * 5 + 1
        print('-' * separator_len)

        tags = tuple(self._tag_length.keys())
        for current_tag in tags:
            print(separator + current_tag.center(self._tag_length[current_tag] + 4), end='')
        print(separator)

        for subtext in self._text:
            for column in tags:
             #if isinstance(subtext[column], float) or isinstance(subtext[column], int):
                print(separator, end='')
                print(' ' * (2 + self._tag_length[column] - len(str(subtext[column]))) + str(subtext[column]), end='')
                print(' ' * 2, end='')
             #else:
             #   print(separator + ' ' * 2 + str(subtext[column]) + ' ' * (self._tag_length[column] - len(str(subtext[column])) + 2), end='')
            print(separator)
        print('-' * separator_len)


class TSVHandler:

    __slots__ = ["_text", "_tag_length", "is_tsv"]

    def __init__(self, tsv_text):
        self._text = tsv_text
        self._tag_length = dict()
        self.is_tsv = self._correct_form

    @property
    def _correct_form(self):
        if type(self._text) != list or len(self._text) == 0:
            return False

        is_lists = all(map(lambda subpackage: isinstance(subpackage, list), self._text))
        if not is_lists:
            return False

        tags = tuple(self._text[0])
        print((f"Tag -> {tags}"))

        for index in range(1, len(self._text)):
            for internal in range(len(self._text[index])):
                cur_len = len(str(self._text[index][internal]))

                try:
                    if cur_len > self._tag_length[tags[internal]]:
                        self._tag_length[tags[internal]] = cur_len
                except KeyError:
                    self._tag_length.update({tags[internal]: len(tags[internal])})

        print("CONTAIN")
        print(self._tag_length)

        return True

    def pretty_print(self):
        if not self.is_tsv:
            return

        separator = '|'
        separator_len = sum(self._tag_length.values()) + len(self._tag_length.values()) * 5 + 1
        print('-' * separator_len)

        tags = tuple(self._tag_length.keys())
        for current_tag in tags:
            print(separator + current_tag.center(self._tag_length[current_tag] + 4), end='')
        print(separator)

        for index in range(1, len(self._text)):
            for internal in range(len(self._text[index])):
             #if isinstance(subtext[column], float) or isinstance(subtext[column], int):
                print(separator, end='')
                print(' ' * (2 + self._tag_length[tags[internal]] - len(str(self._text[index][internal]))) + str(self._text[index][internal]), end='')
                print(' ' * 2, end='')
             #else:
             #   print(separator + ' ' * 2 + str(subtext[column]) + ' ' * (self._tag_length[column] - len(str(subtext[column])) + 2), end='')
            print(separator)
        print('-' * separator_len)

if __name__ == '__main__':
    filename = sys.argv[1]

    encoding_list = ['utf-8', 'utf-16', 'cp1251']

    try:
        with open(filename, 'rb') as file:
            flow_bytes = file.read()
    except FileNotFoundError:
        print(traceback.format_exc())
        #TODO

    for encode in encoding_list:
        try:
            flow_symbol = flow_bytes.decode(encode)
            break
        except UnicodeDecodeError:
            continue


    try:
        packet = json.loads(flow_symbol)
        handler = JSONHandler(packet)
        handler.pretty_print()
    except json.decoder.JSONDecodeError:
        packet = [line.strip().split('\t') for line in flow_symbol.split('\n') if line]
        #print(packet)
        handler = TSVHandler(packet)
        handler.pretty_print()
    except Exception:
        print(traceback.format_exc())
