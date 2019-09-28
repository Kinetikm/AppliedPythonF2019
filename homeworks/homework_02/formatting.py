from validation import check_schema
from exceptions import ValidDataException


def tsv_to_json(data):
    header = data[0]
    res_data = []
    try:
        for row in data[1:]:
            begin = 0
            end = 4
            temp_dict = {}
            for i, j in list(zip(header, row))[begin:end]:
                if i == "Оценка":
                    j = int(j)
                temp_dict[i] = j
            res_data.append(temp_dict)
            begin += 4
            end += 4
    except (ValueError, IndexError):
        raise ValidDataException("Validation Error")
    return res_data


def transform_to_schema(data):
    check_schema(data)

    num_space_template = [len("Название"), len("Ссылка"), len("Теги"), len("Оценка")]

    for string in data:
        col1, col2, col3, col4 = string.values()
        if len(col1) > num_space_template[0]:
            num_space_template[0] = len(col1)
        if len(col2) > num_space_template[1]:
            num_space_template[1] = len(col2)
        if len(col3) > num_space_template[2]:
            num_space_template[2] = len(col3)
        if len(str(col4)) > num_space_template[3]:
            num_space_template[3] = len(str(col4))  # В четвёртой колонке int

    space_template = [" " * num + 4 * " " for num in num_space_template]

    res_str = (len("".join(space_template)) + 5) * "-" + "\n"

    res_str += "|  "

    for i in range(len(num_space_template)):
        res_str += (
            f"{list(data[0].keys())[i]}".center(num_space_template[i], " ") + "  |  "
        )

    res_str += "\n"

    for j in range(len(data)):
        res_str += "|  "
        for i in range(len(num_space_template)):
            if i != 3:
                res_str += (
                    f"{list(data[j].values())[i]}".ljust(num_space_template[i], " ")
                    + "  |  "
                )
            else:
                res_str += (
                    f"{list(data[j].values())[i]}".rjust(num_space_template[i], " ")
                    + "  |  "
                )
        res_str = res_str.rstrip() + "\n"

    res_str += (len("".join(space_template)) + 5) * "-"

    return res_str
