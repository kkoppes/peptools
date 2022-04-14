#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `pep_con_tool` file_functions package."""

import pytest
from pep_con_tool.file_functions.navigate import find_files

TEST_DIR = "tests\\test_files"
# test for find_files function
def test_find_files():
    """test for the find_files function"""
    # test for find_files function
    assert find_files(TEST_DIR) == ['tests\\test_files\\test.txt', 'tests\\test_files\\test_csv_1.csv', 'tests\\test_files\\test_csv_sc_1.csv' ]
    assert find_files(TEST_DIR, extension='.csv') == ['tests\\test_files\\test_csv_1.csv', 'tests\\test_files\\test_csv_sc_1.csv' ]