from tkinter import *
from tkinter import filedialog
import os
import glob

import pandas as pd

from natsort import natsorted, ns
from Metric_Code_to_String import *

### Selecting all the metric files (within folder) parsed by day

def get_csv_files_in_directory():
    """
    :return: (file_list, selected_folder_title)
    """
    files_list = []
    root = Tk();   root.withdraw()

    home = os.path.expanduser('~')  # returns the home directory on any OS --> ex) /Users/jhl
    selected_folder_title = filedialog.askdirectory(initialdir = home)
    csv_path = os.path.join(selected_folder_title, '*.csv')

    base_title = csv_path.split("/")[-2]    ## Last element is just .csv

    return csv_path, base_title



## Merging all the daily metrics within the folder!

def merge_metrics(csv_path):
    df_list = []
    for fname in natsorted(glob.glob(csv_path), alg=ns.IGNORECASE):
        df = pd.read_csv(fname, header=[0, 1], index_col=0, dtype='object', low_memory=False)  # read in multi-index dataframe
        df_list.append(df)

    combined_df = pd.concat(df_list, axis=0)  # concat vertically! axis=0 --> along columns

    return combined_df

def return_metrics_code(metric_string):
    return working_code_dict[metric_string]



working_code_dict = {}
for k, v in metric_code_to_dict.items():
    for key in k:
        working_code_dict[key] = v

p1 = ["pokes_iti_window", "pokes_paradigm_total", "pokes_trial_window", "trials_reward"]
p2 = ["pokes_iti_window", "pokes_paradigm_total", "pokes_trial_window", "trials_reward"]
p3 = ["pokes_iti_window", "pokes_paradigm_total", "pokes_trial_window", "trials_reward"]
p3 = ["pokes_iti_window", "pokes_paradigm_total", "pokes_trial_window", "trials_reward", "trials_valid_ports"]
p5 = ["pokes_iti_window", "pokes_paradigm_total", "pokes_trial_window", "pokes_reward_window", "trials_reward", "trials_incorrect", "trials_initiated", "trials_omission"]
p6 = ["pokes_iti_window", "pokes_paradigm_total", "pokes_trial_window", "pokes_reward_window", "pokes_delay_window","trials_reward", "trials_incorrect", "trials_initiated", "trials_omission"]
## Make a List (trials by paradigm)

def save_individual_metrics(combined_df, base_title, paradigm):

    df_idx = combined_df.index.tolist()

    ## Each parameter according to in paradigm list
    for i in range(len(paradigm)):

        filename = paradigm[i]
        code = return_metrics_code(filename)

        metric_idx = [i for i, s in enumerate(df_idx) if code in s]
        final_metric_csv = combined_df.iloc[metric_idx]

        final_metric_csv.to_csv(filename + "_" + base_title + ".csv")

## Base_Title is "Dark vs. 23hr"


(csv_path, base_title) = get_csv_files_in_directory()

combined_df = merge_metrics(csv_path)

save_individual_metrics(combined_df, base_title, p1)