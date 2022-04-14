#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `pep_con_tool` package."""

import pytest

import pyarrow as pa
import pandas as pd

from pep_con_tool import pep_con_tool
from pep_con_tool import cli
from pep_con_tool.data_processing.pd_functions import (
    get_columns_containing_string,
    date_column_parser,
    fix_date_columns,
    add_date_time_columns,
    set_col_cat
)


# test for get_columns_containing_string
def test_get_columns_containing_string():
    """test for get_columns_containing_string"""
    df = pd.DataFrame({"col_1": [1, 2, 3], "col_2": [1, 2, 3], "col_3": [1, 2, 3]})
    assert get_columns_containing_string(df, "col") == ["col_1", "col_2", "col_3"]
    assert get_columns_containing_string(df, "col_1") == ["col_1"]
    assert get_columns_containing_string(df, "col_2") == ["col_2"]
    assert get_columns_containing_string(df, "col_3") == ["col_3"]
    assert get_columns_containing_string(df, "col_4") == []


# test for date_column_parser
def test_date_column_parser():
    """test for date_column_parser"""
    df = pd.DataFrame({"col_1": ["2020-01-01", "2020-01-02", "2020-01-03"], "col_2": ["2020-01-01", "2020-01-02", "2020-01-03"]})
    df = date_column_parser(df, "col_1", "%Y-%m-%d")
    assert df["col_1"].dtype == "datetime64[ns]"
    assert df["col_1"][0] == pd.Timestamp("2020-01-01")
    assert df["col_1"][1] == pd.Timestamp("2020-01-02")
    assert df["col_1"][2] == pd.Timestamp("2020-01-03")


# test for fix_date_columns
def test_fix_date_columns():
    """test for fix_date_columns"""
    df = pd.DataFrame({"date_1": ["2020-01-01", "2020-01-02", "2020-01-03"], "time_2": ["14:15:16", "17:18:19", "20:21:22"]})
    df = fix_date_columns(df, "%Y-%m-%d", "date")
    assert df["date_1"].dtype == "datetime64[ns]"
    assert df["date_1"][0] == pd.Timestamp("2020-01-01")
    assert df["date_1"][1] == pd.Timestamp("2020-01-02")
    assert df["date_1"][2] == pd.Timestamp("2020-01-03")
    df = fix_date_columns(df, "%H:%M:%S", "time")
    assert df["time_2"].dtype == "datetime64[ns]"
    assert df["time_2"][0] == pd.Timestamp("1900-01-01 14:15:16")
    assert df["time_2"][1] == pd.Timestamp("1900-01-01 17:18:19")
    assert df["time_2"][2] == pd.Timestamp("1900-01-01 20:21:22")


# test for add_date_time_columns
def test_add_date_time_columns():
    """test for add_date_time_columns"""
    df = pd.DataFrame({"date_1": ["2020-01-01", "2020-01-02", "2020-01-03"], "time_2": ["14:15:16", "17:18:19", "20:21:22"]})
    df = fix_date_columns(df, "%Y-%m-%d", "date")
    df = fix_date_columns(df, "%H:%M:%S", "time")
    df = add_date_time_columns(df, [("date_1", "time_2")])
    assert df["date_1_time"].dtype == "datetime64[ns]"
    assert df["date_1_time"][0] == pd.Timestamp("2020-01-01 14:15:16")
    assert df["date_1_time"][1] == pd.Timestamp("2020-01-02 17:18:19")
    assert df["date_1_time"][2] == pd.Timestamp("2020-01-03 20:21:22")

# test for set_col_cat
def test_set_col_cat():
    """test for set_col_cat"""
    df = pd.DataFrame({"col_1": ["a", "b", "b"], "col_2": ["a", "b", "c"]})
    df = set_col_cat(df, 2)
    assert df["col_1"].dtype == "category"
    assert df["col_1"][0] == "a"
    assert df["col_1"][1] == "b"
    assert df["col_1"][2] == "b"
    assert df["col_2"].dtype != "category"
    assert df["col_2"][0] == "a"
    assert df["col_2"][1] == "b"
    assert df["col_2"][2] == "c"

