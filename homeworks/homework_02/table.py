import sys

import module1_open as m1
import module2_format as m2
import module3_print as m3

if __name__ == '__main__':
    filename = 'files/' + sys.argv[1]

    open_result = m1.open_file(filename)  # определение кодировки
    if open_result != -1:
        format_data = m2.format_data(data=open_result, filename=filename)  # определение формта
        m3.print_table(data=open_result, format_data=format_data)  # форматированный вывод
