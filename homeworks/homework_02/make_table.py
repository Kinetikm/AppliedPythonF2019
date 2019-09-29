def do_table(dict_text):
    try:
        max_width = [len(str(name)) for name in dict_text[0].keys()]
        values = [dic.values() for dic in dict_text]
        for value in values:
            for num, field in enumerate(value):
                max_width[num] = max(max_width[num], len(str(field)))

        result = (sum(max_width) + 5 * len(max_width) + 1) * '-' + '\n'
        keys = list(dict_text[0].keys())
        for num, key in enumerate(dict_text[0].keys()):
            keys[num] = " " * (max_width[num] // 2 - len(key) // 2) + key + " " * (
                    max_width[num] - max_width[num] // 2 - len(key) + len(key) // 2)
        result += "|  " + "  |  ".join(keys) + "  |""\n"
        for i in values:
            new_val = []
            for num, val in enumerate(i):
                try:
                    float(val)
                    new_val.append(str(val).rjust(max_width[num]))
                except Exception:
                    new_val.append(str(val).ljust(max_width[num]))

            result += "|  " + "  |  ".join(new_val) + "  |""\n"
        result += (sum(max_width) + 5 * len(max_width) + 1) * '-' + '\n'
        return result
    except Exception:
        return None
