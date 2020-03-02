
from natsort import natsorted, ns
from datetime import datetime


from select_csv_file import *

import pandas as pd
from matplotlib.dates import DateFormatter
import matplotlib.pyplot as plt

# import seaborn as sns
# sns.set(style="ticks")

import matplotlib.style as style

# style.available
# style.use('seaborn-bright')

from Code_Dictionaries import *





#####

def new_metric_to_tidy(filepath):
    """
    returns a tidy version of the metric
    """

    metric = pd.read_csv(filepath, header=[0, 1], index_col=0, dtype='object')

    # Passsing in headers as a list of ints will make it a MultiIndex --> Multilevel dataframe
    # index_col (As ints) sets the index_column
    # use dtype='object' to preserve data as stored in Excel

    stacked = metric.stack("Box Number")  # Stack Box Numbers (make it into a column)
    s_ = stacked.reset_index()  # reset index to make it into a single level dataframe
    s_.columns.name = ""  # null string for column name

    s_.rename(columns={'level_0': "date", "Box Number": "Box_Number"}, inplace=True)

    # # Melt Operation
    melt = pd.melt(s_, id_vars=['date', 'Box_Number'], var_name='Location', value_name='Frequency')

    melt.Frequency = pd.to_numeric(melt.Frequency)

    tidy = melt.copy()

    ## Use iterrows() to take advantage of the 'index' functionality!! (so that I can use .iloc)

    tidy['date'] = "2020/" + melt['date'].str[:5]  # Add in year here! since year defaults to 1900
    tidy['code'] = melt['date'].str[-2:]
    tidy['date'] = pd.to_datetime(tidy['date'], format="%Y/%m/%d")

    #     for index, row in melt.iterrows():   # iterating through the ORIGINAL dataframe to access the dates from rows

    #         if row['date'][:2] == '12':
    #             tidy.iloc[index, 0] = "2019/" + row['date'][:5]  # .iloc[row, column]

    #         elif row['date'][:2] == '01':
    #             tidy.iloc[index, 0] = "2020/" + row['date'][:5]

    #     tidy['date'] =  pd.to_datetime(tidy['date'], format="%Y/%m/%d")

    return tidy

#
def tidy_to_plot_format(loc_df, adults=['1', '2', '3', '4', '5'], adols=['6', '7', '8', '9', '10'], column_name="Frequency"):
    """
    loc_df = can be left/middle/right/total (usually will be total)
    """
    pivot = loc_df.pivot(index="date", columns='Box_Number', values=column_name)

    pivot["Adult Avg"] = pivot.loc[:, adults].mean(axis=1)  # average over first 5
    pivot['Adol Avg'] = pivot.loc[:, adols].mean(axis=1)  # average over next 5
    pivot['Adult Sem'] = pivot.loc[:, adults].sem(axis=1, ddof=1)
    pivot['Adol Sem'] = pivot.loc[:, adols].sem(axis=1, ddof=1)

    return pivot
#
#
def parse_by_location(file, location="Total"):

    """
    :param file:
    :param location: either left/middle/right/total
    :return:
    """
    tidy = new_metric_to_tidy(file)
    # melt = pd.melt(tidy, id_vars=['date', 'Box_Number'], var_name='Location', value_name='Frequency')

    df_by_loc = tidy[tidy.Location == location]
    final_plot_df = tidy_to_plot_format(df_by_loc)

    return final_plot_df
#
def get_graph_title(file):
    title_list = file.split(".")[0].split("_")[
                 1:]  # truncate the last part (by splitting with '.' and then split it by underscore)
    # (dropping the first and last word from title)
    title_key = '_'.join(title_list)  # Make the string from the list

    title = plot_code_dict[title_key]

    return title


def plot_metrics(file, adults=[1,2,3,4,5], adols=[6,7,8,9,10], paradigms=None, save_fig=False):

    # title = get_graph_title(file)

    plot_df = parse_by_location(file, location="Total")

    # # Start Plotting
    fig, ax = plt.subplots(figsize=(14, 12))

    for i in set(adults):
        box_number = str(i)  #
        plt.plot(plot_df[box_number], c='red', alpha=0.15)

    for j in set(adols):
        box_number = str(j)
        plt.plot(plot_df[box_number], c='blue', alpha=0.15)

    ax.errorbar(x=plot_df.index, y=plot_df["Adult Avg"], yerr=plot_df['Adult Sem'], c='red', alpha=0.9)
    ax.errorbar(x=plot_df.index, y=plot_df["Adol Avg"], yerr=plot_df['Adol Sem'], c='blue', alpha=0.9)

    ax.xaxis_date()

    ax.legend(['844', '845', '847', '852', '870', '871', '872', '873', '869', "Adult Avg", "Adol Avg"],
              loc='upper center', bbox_to_anchor=(1.1, 1.02))

    #     ax.set_ylim([10,6900])
    #     ax.set_ylim([0.53,1])
    ax.set_title("Default", fontdict={"fontsize": 22})
    # ax.set_xlabel("Days")
    #     ax.set_ylabel("Counts", fontdict={"fontsize":18})
    ax.set_ylabel("Counts", fontdict={"fontsize": 18})
    ax.tick_params(axis='both', which='major', labelsize=16)

    plt.xticks(plot_df.index, plot_df.index)  # (location, labels)

    myFmt = DateFormatter("%m-%d")  # set the date format (ex: 10/17)
    ax.xaxis.set_major_formatter(myFmt)
    fig.autofmt_xdate(rotation=70, ha='center')

    # # Creating Paradigm Cutoff Dates

    if paradigms is not None:
        if not isinstance(paradigms, (list, tuple)):
            raise TypeError("Only lists or tuples are accepted as 'paradigms' parameter")


        elif not all(isinstance(elem, str) for elem in paradigms):  # If all the elements of list, array are string
            raise ValueError("All dates in 'paradigms' must be in strings in datetime format (YYYY-MM-DD)")

        else:  # should check for datetime formats too?? --> looks like pandas does it for me
            paradigm_position = []
            for i in paradigms:
                dt = pd.to_datetime(i)
                paradigm_position.append(dt)

            # # plot dates of paradigms (vertical lines)
            for p in paradigm_position:
                ax.axvline(x=p, color='k', linestyle='--', dashes=(3, 5), linewidth=2, alpha=0.5)

    if save_fig:
        plt.tight_layout()
        plt.savefig("default")  # filename
    else:
        plt.show()


file_path = select_csv_file()
ad = new_metric_to_tidy(file_path)
parse_by_location(file_path, "Left")

plot_metrics(file_path, save_fig=True)

# tidy_to_plot_format()

# plot_metrics(file)