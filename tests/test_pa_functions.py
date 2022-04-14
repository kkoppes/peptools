#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `pep_con_tool` package."""

import pytest

import pyarrow as pa
import pandas as pd

from pep_con_tool import pep_con_tool
from pep_con_tool import cli
from pep_con_tool.data_processing.arrow_funtions import (
    read_csv_file,
    read_csv_headers,
    pa_to_df,
    add_suffix,
)




# @pytest.fixture
# def response():
#    """Sample pytest fixture.
#
#    See more at: http://doc.pytest.org/en/latest/fixture.html
#    """
#    # import requests
#    # return requests.get("https://github.com/audreyr/cookiecutter-pypackage")
#
#
# def test_content(response):
#    """Sample pytest test function with the pytest fixture as an argument."""
#    # from bs4 import BeautifulSoup
#    # assert "GitHub" in BeautifulSoup(response.content).title.string
#
#
# def test_cli():
#    """Test the CLI."""
#
#    parser = cli.parse_args(["--foo", "test"])
#    assert parser.foo == "test"

CSV_TEST_C_FILE_1 = "./tests/test_files/test_csv_1.csv"
CSV_TEST_FILE_1_HEADER = [
    "header_0",
    "header_1",
    "header_2",
    "header_3",
    "header_4",
    "header_5",
    "header_6",
    "header_7",
    "header_8",
    "header_9",
    "header_10",
    "header_11",
    "header_12",
    "header_13",
    "header_14",
    "header_15",
]
CSV_TEST_SC_FILE_1 = "./tests/test_files/test_csv_sc_1.csv"


def test_read_csv_headers():
    """test for the read_csv_headers function"""
    assert read_csv_headers(CSV_TEST_C_FILE_1, ",") == CSV_TEST_FILE_1_HEADER
    assert read_csv_headers(CSV_TEST_SC_FILE_1, ";") == CSV_TEST_FILE_1_HEADER


# test for read_csv_file
def test_read_csv_file():
    """test for the read_csv_file function"""
    # read_csv_file("test_data/test_data.csv")
    headers = read_csv_headers(CSV_TEST_C_FILE_1, ",")
    pyarrow_table = read_csv_file(CSV_TEST_C_FILE_1, headers, 1, ",")
    assert type(pyarrow_table) == pa.Table
    # pa table headers include filename
    assert headers == list(pyarrow_table.column_names[:-1])

    firstrow = {
        "header_0": "row_0_col_0",
        "header_1": "row_0_col_1",
        "header_2": "row_0_col_2",
        "header_3": "row_0_col_3",
        "header_4": "row_0_col_4",
        "header_5": "row_0_col_5",
        "header_6": "row_0_col_6",
        "header_7": "row_0_col_7",
        "header_8": "row_0_col_8",
        "header_9": "row_0_col_9",
        "header_10": "row_0_col_10",
        "header_11": "row_0_col_11",
        "header_12": "row_0_col_12",
        "header_13": "row_0_col_13",
        "header_14": "row_0_col_14",
        "header_15": "row_0_col_15",
        "filename": "test_csv_1",
    }

    assert pyarrow_table.to_pylist()[0] == firstrow

    firstcol = [
        "row_0_col_0",
        "row_1_col_0",
        "row_2_col_0",
        "row_3_col_0",
        "row_4_col_0",
        "row_5_col_0",
        "row_6_col_0",
        "row_7_col_0",
        "row_8_col_0",
        "row_9_col_0",
        "row_10_col_0",
        "row_11_col_0",
        "row_12_col_0",
    ]

    assert pyarrow_table.to_pydict()[headers[0]] == firstcol


# test for pa_to_df
def test_pa_to_df():
    """test for the pa_to_df function"""
    headers = read_csv_headers(CSV_TEST_C_FILE_1, ",")
    pa_table = read_csv_file(CSV_TEST_C_FILE_1, headers, 1, ",", False)
    df_from_pa = pa_to_df(pa_table)
    df_from_csv = pd.read_csv(CSV_TEST_C_FILE_1, sep=",")
    # This is a test to check that the output of the pa_to_df function is a pandas dataframe.
    assert isinstance(pa_to_df(pa_table), pd.DataFrame)
    assert df_from_pa.equals(df_from_csv)


MYLIST = [
    "a",
    "a",
    "b",
    "c",
    "d",
    "e",
    "e",
    "f",
    "g",
    "h",
    "i",
    "i",
    "i",
    "j",
    "k",
    "l",
    "m",
    "x",
    "x",
    "x",
    "x",
    "y",
    "z",
]

# test for add_suffix
def test_add_suffix():
    """test for the add_suffix function"""
    assert add_suffix(MYLIST) == [
        "a",
        "a_1",
        "b",
        "c",
        "d",
        "e",
        "e_1",
        "f",
        "g",
        "h",
        "i",
        "i_1",
        "i_2",
        "j",
        "k",
        "l",
        "m",
        "x",
        "x_1",
        "x_2",
        "x_3",
        "y",
        "z",
    ]

