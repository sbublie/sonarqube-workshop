#! /usr/bin/python3
#
# SPDX-License-Identifier: MIT
import argparse

import odxtools

argparser = argparse.ArgumentParser(
    description="\n".join([
        "Read in a PDX file and write back the resulting database object.",
        "",
        "This is primarily intended to be a demonstration of how to write",
        "PDX files using odxtools, but it can also be used to strip",
        "'unnecessary' auxiliary data from the input PDX file.",
    ]),
    formatter_class=argparse.RawTextHelpFormatter,
)

argparser.add_argument(
    "input_pdx_file", metavar="INPUT_PDX_FILE", help="Path to the input .pdx file")
argparser.add_argument(
    "output_pdx_file",
    metavar="OUTPUT_PDX_FILE",
    help="Path to the where the resulting .pdx file is written",
)

args = argparser.parse_args()

in_file_name = args.input_pdx_file
out_file_name = args.output_pdx_file

print(f"Loading input file '{in_file_name}'...", end="", flush=True)
db = odxtools.load_pdx_file(in_file_name)
print(" done")

print(f"Writing output file '{out_file_name}'...", end="", flush=True)
odxtools.write_pdx_file(out_file_name, db)
print(" done")
