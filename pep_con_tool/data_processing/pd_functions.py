import os
import logging
import pandas as pd
from datetime import datetime
from janitor import clean_names
import janitor
from pep_con_tool.file_functions.navigate import find_files
from pep_con_tool.data_processing.arrow_funtions import csv2df


def get_columns_containing_string(df, string):
    """ get date columns from name """
    return [col for col in df.columns if string in col.lower()]

# parse date column function
def date_column_parser(df, date_column, date_format):
    """
    parse date column function
    df: pandas dataframe
    date_column: date column name
    date_format: date format
    """
    df[date_column] = pd.to_datetime(df[date_column], format=date_format, errors='coerce')
    return df  

def fix_date_columns(df, date_format, column_string):
    """ 
    fix date columns 
    df: pandas dataframe
    date_format: date format example: '%Y-%m-%d'
    column_string: string to search for in column names
    """

    date_columns = get_columns_containing_string(df, column_string)

    for col in date_columns:
        df = date_column_parser(df, col, date_format)
    
    return df

# function to add date and time columns
def add_date_time_columns(df, dt_col : list, remove_original : bool = True):
    """ 
    function to add date and time columns 
    df: pandas dataframe
    dt_col: list of tuples [(date_col, time_col), (date_col, time_col)]
    """

    for (date_column, time_column) in dt_col:
        df[(f"{date_column}_time")] = df[date_column] + (df[time_column] - datetime(1900, 1, 1))
    
    if remove_original:
        # remove dt_col columns
        for (date_column, time_column) in dt_col:
            df.drop([date_column, time_column], axis=1, inplace=True)
            
        
    return df


def set_col_cat(df, unique_n=10):
    """
    Looping through all the columns in the dataframe and checking the number of unique values in each
    column. 
    If the number of unique values is less than the unique_n argument
    it sets the column data type to category.
    """    
    
    for col in df.columns:
        un = len(df[col].unique())
        if un <= unique_n:
            #set dtype to category
            df[col] = df[col].astype('category')

    return df

def data_pipe_pba(csv_file):
    """data cleaning pipeline for reading PBA csv files"""

    # formatting date
    date_format = "%d.%m.%Y"
    date_string = "date"

    # formatting time columns
    # set date_format function to format the time column.
    time_format = "%H:%M:%S"
    time_string = "time"

    # combine date and time columns
    dt_col = [
        ("task_beginning_date", "task_beginning_time"),
        ("task_ending_date", "task_ending_time"),
    ]

    df = (
        csv2df(csv_file)
        .pipe(clean_names)
        .pipe(fix_date_columns, date_format, date_string)
        .pipe(fix_date_columns, time_format, time_string)
        .pipe(add_date_time_columns, dt_col)
        .pipe(set_col_cat)
    )

    return df

