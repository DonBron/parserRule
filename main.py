import time
import tkinter as tk
from pathlib import Path
from tkinter import filedialog

import pandas as pd

from utils import check_web_category, get_like_cat_level_data, get_master_web_category_id, get_web_category_id, read_csv


def open_file_dialog() -> Path:
    root = tk.Tk()
    root.withdraw()
    _path = filedialog.askopenfilename(filetypes=[('CSV files', '*.csv'), ('All files', '*.*')])
    if not _path:
        raise ValueError('>>>>>>>Файл не выбран<<<<<<<<<<<')
    return Path(_path)


if __name__ == '__main__':
    file_path = open_file_dialog()

    rows = read_csv(file_path)

    df = pd.DataFrame(rows)

    for index, row in df.iterrows():
        row_data = row[2]
        try:
            df.at[index, 'or'] = row_data.count('or')
            df.at[index, 'and'] = row_data.count('and')
            df.at[index, 'not'] = row_data.count('not')
            df.at[index, 'and not'] = row_data.count('and  not')
            df.at[index, 'like'] = row_data.count('like')
            df.at[index, '='] = row_data.count('=')
            df.at[index, 'Короткое интернет-имя'] = row_data.count('Короткое интернет-имя')
            df.at[index, 'есть id категории'] = check_web_category(row_data)
            df.at[index, 'id мастер-категории'] = get_web_category_id(row_data)
            df.at[index, 'id web-категории'] = get_master_web_category_id(row_data)
            df.at[index, 'Уровень категорий'] = get_like_cat_level_data(row_data)

        except AttributeError as err:
            print(row_data)
            pass

    filename = time.strftime('%Y-%m-%d %H-%M-%S') + '.xlsx'

    df.to_excel(filename)
