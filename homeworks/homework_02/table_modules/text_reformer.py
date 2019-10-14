def reformate(text, encode):
    if encode == "json":
        # Делаем из list(dict) list of lists

        list_data = []
        header = []
        [header.append(keyz) for keyz in text[0].keys()]

        list_data.append(header)

        for dicts in text:
            temp_list = []
            for keys_column in header:
                temp_list.append(dicts[keys_column])
            list_data.append(temp_list)

        return list_data
    else:
        # Уже лист листов
        return text
