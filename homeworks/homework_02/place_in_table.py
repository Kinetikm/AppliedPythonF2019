def place_in_table(data):
    num_of_col = len(data[0])  # nут уже проверенные
    widths = determine_widths(data, num_of_col)
    table = make_a_table(data, num_of_col, widths)
    return table


def determine_widths(data, num_of_col):
    widths = []
    for i in range(num_of_col):
        width_of_col = 0
        for d in data:
            width_of_col = max(width_of_col, len(str(d[i]))+2)
        widths.append(width_of_col)
    return widths


def make_a_table(data, num_of_col, widths):
    table = ''
    line = (num_of_col+1)*'-'
    for i in range(num_of_col):
        for i in range(widths[i]+2):
            line += '-'
    table += line+'\n'
    line0 = '|'
    for i in range(num_of_col):
        line0 += ' '*((widths[i]-len(str(data[0][i])))//2+1)+str(data[0][i])
        line0 += ' '*((widths[i]-len(str(data[0][i])))//2)+' |'  # for first line
    table += line0+'\n'
    line0 = '|  '
    for lines in data[1:]:  # for others lines
        line0 = '|  '
        for i in range(num_of_col-1):
            line0 += str(lines[i])+' '*(widths[i]-len(str(lines[i])))+'|  '
        line0 += ' '*(widths[num_of_col-1]-len(str(lines[num_of_col-1]))-2)+str(lines[num_of_col-1])+'  |'
        table += line0+'\n'
    table += line
    return table
