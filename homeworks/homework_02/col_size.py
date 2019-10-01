def measure_column_size(list_c) -> list:
    column_size = [0] * len(list_c[0])
    for i in range(len(list_c)):
        for j in range(len(list_c[i])):
            if len(list_c[i][j]) > column_size[j]:
                column_size[j] = len(list_c[i][j])
    return column_size
