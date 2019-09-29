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
        tags = tuple(title.keys())

        for contain in self._text:
            for key in tags:

                cur_len = len(str(contain[key]))

                try:
                    if cur_len > self._tag_length[key]:
                        self._tag_length[key] = cur_len
                except KeyError:
                    self._tag_length.update({key: len(key)})

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

        for subtext in self._text:
            print(separator)
            for column in tags:

                escape_num = self._tag_length[column] - len(str(subtext[column]))

                if isinstance(subtext[column], float) or isinstance(subtext[column], int):
                    print(separator + ' ' * (2 + escape_num) + str(subtext[column]) + ' ' * 2, end='')
                else:
                    print(separator + ' ' * 2 + str(subtext[column]) + ' ' * (escape_num + 2), end='')

        print(separator)
        print('-' * separator_len)
