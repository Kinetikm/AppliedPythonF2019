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

        for index in range(1, len(self._text)):
            for internal in range(len(self._text[index])):
                cur_len = len(str(self._text[index][internal]))

                try:
                    if cur_len > self._tag_length[tags[internal]]:
                        self._tag_length[tags[internal]] = cur_len
                except KeyError:
                    self._tag_length.update({tags[internal]: len(tags[internal])})

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
                print(separator, end='')
                print(' ' * (2 + self._tag_length[tags[internal]] - len(str(self._text[index][internal]))), end='')
                print(str(self._text[index][internal]), end='')
                print(' ' * 2, end='')

            print(separator)
        print('-' * separator_len)
