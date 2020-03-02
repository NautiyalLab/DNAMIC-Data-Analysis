from tkinter import *
from tkinter import filedialog
import os
import glob
from natsort import natsorted, ns
import re
import pandas as pd

# returns a list of relevant files within the directory + directory title
def get_txt_files_in_directory():
    """
    :return: (file_list, selected_folder_title)
    """
    files_list = []
    root = Tk();   root.withdraw()

    home = os.path.expanduser('~')  # returns the home directory on any OS --> ex) /Users/jhl
    selected_folder_title = filedialog.askdirectory(initialdir = home)
    file_pattern = os.path.join(selected_folder_title, '*.txt')

    for file in natsorted(glob.glob(file_pattern), alg=ns.IGNORECASE):  # using natsorted to naturally sort the files
        files_list.append(file)

    return files_list, selected_folder_title


def get_box_numbers(files_list):
    """
    :param files_list: list of the individual files within that directory (dtype:list)
    :return: box_num_list - box numbers from the individual files stored in a list (parsed using regex)
    """
    box_num_list = []

    file_count = len(files_list)

    for i in range(file_count):
        full_path = files_list[i]
        file_name = full_path.split("/")[-1]  # File name is always the last in the list

        # Do NOT change the filname format (from Processing side) - Unless you want to change the regex below!
        # Regex
        box = re.findall(r'box\d+', file_name)[0]  # Returns box and number in string ex)"box7"
        box_num = re.findall(r'\d+', box)[0]  # Returns only the number in string ex) "7"

        box_num_list.append(box_num)

    return box_num_list


def save_multilevel_df_to_csv(files_list, box_numbers, col_names, selected_folder_title):
    """
    :param files_list: list of files to concatenate
    :param box_numbers: list of the actual box numbers extracted from files (instead of numbers by location)
    :param col_names: array of column names (usually ['event_code', 'timestamp', 'counter'])
    :param selected_folder_title: path of the selected directory --> later to become title of csv file
    :return: saves multiindex dataframe into a csv within the Pycharm project folder --> change path later!
    """
    col_names = col_names
    files = files_list
    result = []

    for i in range(len(files)):
        f = files[i]
        # box_num.append(i + 1)  # box_number for outermost level (index)

        df = pd.read_csv(f, sep=":", header=None, names=col_names)   # read_csv can also read in txt files! 
        result.append(df)

    multi_df = pd.concat(result, axis=1, keys=box_numbers, names=['Box Number', 'Columns'])
    df_title = os.path.basename(selected_folder_title)  # Returns the lowest directory of path (basename)

    # Saves it within current scope (within this project folder)
    multi_df.to_csv(df_title + ".csv")


# # # # # # # # # # # FINAL FUNCTION CALLS # # # # # # # # # # #

# # Change here for different columns to use (: delimiter value)
# anything with double ::
col_names = ['event_code', 'timestamp', 'counter'] # For TIR (Groups 1,2)
## After Groups 3, use double :: exclusively!

# anything with single :
# col_names = ['event_code', 'timestamp']  # For Port Habituation + Continuous Cue + Random Forced Choice (RFC) (Groups 3+)


(files_list, selected_folder_title) = get_files_in_directory()
box_numbers = get_box_numbers(files_list)

save_multilevel_df_to_csv(files_list, box_numbers, col_names, selected_folder_title)
