# Copyright 2020 Louis Paternault
#
# This file is part of SpiX.
#
# SpiX is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# SpiX is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with SpiX.  If not, see <https://www.gnu.org/licenses/>.

"""Compile a `.tex` file, executing commands that are set inside the file itself."""

import argparse
import logging
import os
import sys

import spix
from . import NAME, VERSION


def commandline_parser():
    """Return a command line parser.

    :rtype: argparse.ArgumentParser
    """
    parser = argparse.ArgumentParser(
        prog="spix",
        description=(
            "Compile a `.tex` file, "
            "executing commands that are set inside the file itself."
        ),
    )
    parser.add_argument(
        "-n",
        "--dry-run",
        action="store_true",
        help="Print the commands that would be executed, but do not execute them.",
    )
    parser.add_argument(
        "--version",
        help="Show version and exit.",
        action="version",
        version=f"{NAME} {VERSION}",
    )
    parser.add_argument("TEX", nargs=1, help="File to process.")

    return parser


def main():
    """Main function."""
    arguments = commandline_parser().parse_args()

    if os.path.exists(arguments.TEX[0]):
        arguments.TEX = arguments.TEX[0]
    elif os.path.exists(f"{arguments.TEX[0]}.tex"):
        arguments.TEX = f"{arguments.TEX[0]}.tex"
    else:
        logging.error("""File not found: "%s".""", arguments.TEX[0])
        sys.exit(1)

    try:
        spix.compiletex(arguments.TEX, dryrun=arguments.dry_run)
    except spix.SpixError as error:
        if str(error):
            logging.error(error)
        sys.exit(1)


if __name__ == "__main__":
    main()
