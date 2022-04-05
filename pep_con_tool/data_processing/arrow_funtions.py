import os
import pyarrow as pa
from pathlib import Path

from pyarrow import csv

def read_csv_file(csv_file, cols,  firstrow, delim=";", fncolumn=True):
    """ read csv file to pyarrow table, add filename to column"""
    
    table = csv.read_csv(csv_file, csv.ReadOptions(skip_rows=firstrow, column_names= cols), parse_options=csv.ParseOptions(delimiter=delim) )
    if fncolumn:
        table = table.append_column('filename', pa.array([Path(os.path.basename(csv_file)).stem] * len(table), pa.string()))
    
    return table