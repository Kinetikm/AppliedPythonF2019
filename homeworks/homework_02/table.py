import sys

from codding import check_type_codding
from tsv_or_json import unpack
from col_size import measure_column_size

if __name__ == '__main__':
    filename = sys.argv[1]

cod = check_type_codding(path_of_file)
if cod == 'Файл не валиден' or cod == 'Формат не валиден':
    print(cod)
    return cod
fp_in_lines = unpack(path_of_file, cod)
check_len = len(fp_in_lines[0])
for line in fp_in_lines:
    if check_len != len(line):
        return "Формат не валиден"
col_size = measure_column_size(fp_in_lines)
sum = 0
for i in col_size:
    sum += i
print('-' * (sum + 5 * len(fp_in_lines[0]) + 1))
for i in range(len(fp_in_lines)):
    print('|', end='')
    for j in range(len(fp_in_lines[i])):
        if i == 0:
            print('{0:^{1}}'.format(fp_in_lines[i][j], col_size[j] + 4),  end='|')
            if j == len(fp_in_lines[i]) - 1:
                print('')
        else:
            if j != len(fp_in_lines[0]) - 1:
                print(' ', '{0:<{1}}'.format(fp_in_lines[i][j], col_size[j] + 1), '|', end='')
            else:
                print('{0:>{1}}'.format(fp_in_lines[i][j], col_size[j] + 2), ' |')
print('-' * (sum + 5 * len(fp_in_lines[0]) + 1))
