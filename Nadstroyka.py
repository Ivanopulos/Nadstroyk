#import Nadstroika as nd
import os
import re
import time
from os.path import getmtime
from datetime import datetime
import inspect
import pandas as pd
# Если ваш модуль зависит от внешних библиотек, убедитесь, что они указаны в файле requirements.txt или в секции install_requires вашего setup.py, если вы планируете распространять ваш модуль:
#
# python
# Copy code
# # setup.py
# from setuptools import setup
#
# setup(
#     name='nadstroika',
#     version='0.1',
#     packages=['nadstroika'],
#     install_requires=[
#         'os',  # Хотя os является частью стандартной библиотеки Python
#         're'   # и re тоже
#         'datetime'   # и тоже
#     ]
# )
def newest(pattern, rank=-1, search_in_subfolders=0, full_path=0, exclude_pattern=None):  # возвращает самый новый файл соответствующий паттерну
#                                                                 /исключающий паттерн
#          /паттерн /ранг с конца                    /вывести полный путь папки
#                            /искать ли в папках или указать имя папки
# result = newest(r'.+\.bat', -1, "venv/Scripts", 1, "pydoc")
# print(result)
    root_dir = '.'  # Настраиваем начальную директорию для поиска
    if isinstance(search_in_subfolders, str):
        root_dir = search_in_subfolders  # Если это путь, используем его
    elif search_in_subfolders:
        root_dir = '.'  # Если истина, ищем в текущей директории и всех поддиректориях

    file_paths = []
    for root, dirs, files in os.walk(root_dir):
        # Обходим файлы и проверяем совпадение с регулярным выражением
        for name in files:
            if re.match(pattern, name):
                if exclude_pattern and re.match(exclude_pattern, name):
                    continue
                file_paths.append(os.path.join(root, name))
        # Если поиск в поддиректориях не требуется, останавливаемся после первой итерации
        if not isinstance(search_in_subfolders, str) and not search_in_subfolders:
            break

    if not file_paths:
        return None

    # Сортируем файлы по времени изменения
    file_paths.sort(key=lambda x: getmtime(x), reverse=(rank < 0))
    adjusted_rank = abs(rank) - 1
    if adjusted_rank >= len(file_paths):
        return None

    # Выбираем файл по рангу и определяем, нужен полный путь или только имя
    file_path = file_paths[adjusted_rank]
    return os.path.abspath(file_path) if full_path else os.path.basename(file_path)
def dtm():  # функция эхо времени(надо ее вызвать в начале программы и в любое время в дальнейшем для вывода времени и времени выполнения программы)
#/n время от последнего вызова, строка которая вызвала
    if not hasattr(dtm, 'dt0'):
        dtm.dt0 = datetime.now()
    else:
        dt1 = datetime.now()
        print(dt1-dtm.dt0, "//", dt1)
def prin(pr):  # функция альтернативного вывода на принт с номером строки и временем
    stack = inspect.stack()  # Получаем стек вызовов # `stack[1]` содержит запись о том, кто вызвал текущую функцию
    print(pr, '--', stack[1].lineno, stack[1].code_context)
    dtm()
print(pd.__version__)

df = pd.DataFrame({
     'country': ['Kazakhstan', 'Russia', 'Belarus', 'Ukraine'],
     'population': [17.04, 143.5, 9.5, 45.5],
     'square': [2724902, 17125191, 207600, 603628]
 }, index=['KZ', 'RU', 'BY', 'UA'])

prin(df)
