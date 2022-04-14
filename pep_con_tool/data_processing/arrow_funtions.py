import os
from pathlib import Path

import pandas as pd
import pyarrow as pa
from pyarrow import csv

# function to add suffix list of string entries that are non-unique and use suffix to indicate how many times this entry appears
def add_suffix(list_of_strings):
    """function to add suffix list of string entries that are non-unique and use suffix to indicate how many times this entry appears"""

    # create list to store new entries
    new_list = []
    # create dictionary to store unique entries
    unique_dict = {}
    # loop through list of strings
    for i in range(len(list_of_strings)):
        # if string is not in dictionary, don't add suffix
        # set initial suffix to 1
        suffix = 0
        if list_of_strings[i] not in unique_dict:
            unique_dict[list_of_strings[i]] = list_of_strings[i]
            # add string to new list
            new_list.append(list_of_strings[i])
        # if string is in dictionary, add suffix
        else:
            suffix += 1
            while list_of_strings[i] + "_" + str(suffix) in unique_dict:
                suffix += 1
            
            unique_dict[list_of_strings[i] + "_" + str(suffix)] = list_of_strings[i] + "_" + str(suffix)
            # add string to new list
            new_list.append(list_of_strings[i] + "_" + str(suffix))
    
    return new_list
    
    
def read_csv_headers(file_path, delimiter=";"):
    """ read csv file to pyarrow table, add filename to column"""
    with open(file_path, 'r') as f:
        header = f.readline()
        header = header.strip().replace("\"", "")
        header = header.split(delimiter)
        header = add_suffix(header)
    return header

def read_csv_file(csv_file, cols,  firstrow, delim=";", fncolumn=True):
    """ 
    read csv file to pyarrow table, add filename to column
    csv_file: path to csv file
    cols: list of column names
    firstrow: first row of csv file
    delim: delimiter
    fncolumn: add filename to column (True/False)
    """
    
    table = csv.read_csv(csv_file, csv.ReadOptions(skip_rows=firstrow, column_names= cols), parse_options=csv.ParseOptions(delimiter=delim) )
    if fncolumn:
        table = table.append_column('filename', pa.array([Path(os.path.basename(csv_file)).stem] * len(table), pa.string()))
    
    return table

# pandas df from pyarrow table
def pa_to_df(pa_table):
    """convert pyarrow table to pandas df"""
    df = pd.DataFrame(pa_table.to_pandas())
    return df

# read csv file to pyarrow table, then convert to pandas df
def csv2df(Filename, delimiter=";"):
    """read csv file to pyarrow table, add filename to column"""
    headers = read_csv_headers(Filename, delimiter)
    pa_table = read_csv_file(Filename, headers, 1, delimiter, True)
    df = pa_to_df(pa_table)
    return df