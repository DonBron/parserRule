import logging
import time
import tkinter as tk
from pathlib import Path
from tkinter import filedialog
from tkinter.messagebox import showinfo
from typing import NoReturn

import pandas as pd

from utils import check_web_category, get_like_cat_level_data, get_master_web_category_id, get_web_category_id
from utils import proverit, read_csv

logging.basicConfig(filename='logs.log', level=logging.DEBUG, encoding='utf-8')
log = logging.getLogger(__name__)


def parsing(file_path: Path) -> NoReturn:
    # file_path = Path(r'C:\Users\alexe\Documents\projects\parserRule\files\done_0205.csv')

    rows = read_csv(file_path)

    df_input = pd.DataFrame(rows)

    df_output = pd.DataFrame(rows)
    for index, row in df_output.iterrows():
        row_data = row[2]
        try:
            df_output.at[index, 'or'] = row_data.count('or')
            df_output.at[index, 'and'] = row_data.count('and')
            df_output.at[index, 'not'] = row_data.count('not')
            df_output.at[index, 'and not'] = row_data.count('and  not')
            df_output.at[index, 'like'] = row_data.count('like')
            df_output.at[index, '='] = row_data.count('=')
            df_output.at[index, 'Короткое интернет-имя'] = row_data.count('Короткое интернет-имя')
            df_output.at[index, 'есть id категории'] = check_web_category(row_data)
            df_output.at[index, 'id мастер-категории'] = get_web_category_id(row_data)
            df_output.at[index, 'id web-категории'] = get_master_web_category_id(row_data)
            df_output.at[index, 'Уровень категорий'] = get_like_cat_level_data(row_data)
        except AttributeError as err:
            log.warning(row_data)

    proverits = []
    for index, row in df_output.iterrows():
        row_data = row[2]
        try:
            proverits += proverit(row_data)
        except AttributeError as err:
            log.warning(row_data)
    df_new_sheet = pd.DataFrame(list(set(proverits)))

    filename = time.strftime('%Y-%m-%d %H-%M-%S') + '.xlsx'
    writer = pd.ExcelWriter(filename, engine='xlsxwriter')
    df_input.to_excel(writer, sheet_name='df_input')
    df_output.to_excel(writer, sheet_name='df_output')
    df_new_sheet.to_excel(writer, sheet_name='df_new_sheet')
    writer.close()


def open_file_dialog() -> Path:
    root = tk.Tk()
    root.withdraw()
    _path = filedialog.askopenfilename(filetypes=[('CSV files', '*.csv'), ('All files', '*.*')])
    if not _path:
        raise ValueError('>>>>>>>Файл не выбран<<<<<<<<<<<')
    parsing(Path(_path))
    showinfo('Выполнил', 'Выполнил')


if __name__ == '__main__':
    import customtkinter

    customtkinter.set_appearance_mode('System')  # Modes: system (default), light, dark
    customtkinter.set_default_color_theme('blue')  # Themes: blue (default), dark-blue, green

    app = customtkinter.CTk()  # create CTk window like you do with the Tk window
    app.geometry('240x240')

    # Use CTkButton instead of tkinter Button
    button_file = customtkinter.CTkButton(master=app, text='Выбрать файл', command=open_file_dialog)
    button_file.pack(padx=0, pady=0)

    app.mainloop()
