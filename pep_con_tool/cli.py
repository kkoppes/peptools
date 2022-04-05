# -*- coding: utf-8 -*-

"""Console script for pep_con_tool."""
import sys
import argparse


def parse_args(args):
    """Returns parsed command line arguments.
    """

    parser = argparse.ArgumentParser(description="Commandline interface for pep_con_tool")
    parser.add_argument("--foo")
    return parser.parse_args(args)


def main():
    """Console script for pep_con_tool."""
    parse_args(sys.argv[1:])
    return 0


if __name__ == "__main__":
    sys.exit(main())
