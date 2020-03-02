import os
import tkinter as tk
from tkinter import filedialog

from Code_Dictionaries import *


def select_csv_file():
    root = tk.Tk()
    root.withdraw()

    home = os.path.expanduser('~')
    file_path = filedialog.askopenfilename(initialdir=home)

    # multi_df = pd.read_csv(file_path, header=[0, 1], index_col=[0], low_memory=False)

    return file_path   # multi_df


d = select_csv_file()
