import sys
import homeworks.homework_02.table_modules.text_reformer as text_reformer
import homeworks.homework_02.table_modules.opener as opener
import homeworks.homework_02.table_modules.printer as printer

# Ваши импорты

if __name__ == '__main__':
    filename = sys.argv[1]
    """Отсюда управляем всеми компонентами программы.
    1. Opener - на вход файл, на выходе либо ошибка либо текст.
    2. Format check - на вход файл, на выходе формат кодировки. Проверка корректности формата, определение формата.
    3. Text reformer - на вход текст, на выходе текст отформатированный. Форматирует наш текст в необходимый нам вид
    4. Возможно Printer, = на вход текст, на выходе принт. Который в корректном формате печатает наши данные из 3."""

    text, type_file = opener.opener(filename)

    if text is not None:
        printer.print_text(text_reformer.reformate(text, type_file))
