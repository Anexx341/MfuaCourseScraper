# Описание
Скрипт извлекает текст из js файлов, генерирующих слайды в презентации, приводя его в более-менее читабельный вид.

# Язык: Python
Версия: 3.6+
Необходимые библиотеки:
bs4

# Использование:
0. Установить Python 3.6+ и bs4
1. Найти нужную тему.
2. Пролистать презентацию. Нужно, чтобы были загружены все слайды.
3. Сохранить страницу в папку со скриптом.
4. Наслаждаться!
5. Править ошибки...

# Функционал:
Скрипт проходит по js файлам, выделяя заголовки в слайдах с помощью regular expressions, заменяя повторяющиеся заголовки в соседних слайдах, удаляя ненужные пробелы и переносы строк.

Текст по умолчанию сохраняется в "utf-8".
Логи работы скрипта по умолчанию сохраняются в файл logs.