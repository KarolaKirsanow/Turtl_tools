#!/usr/bin/env python3

import os
import argparse
import random
import re
import codecs

#process escape sequences  in note text following rspeers on StackOverflow:
ESCAPE_SEQUENCE_RE = re.compile(r'''
    ( \\U........      # 8-digit hex escapes
    | \\u....          # 4-digit hex escapes
    | \\x..            # 2-digit hex escapes
    | \\[0-7]{1,3}     # Octal escapes
    | \\N\{[^}]+\}     # Unicode characters by name
    | \\[\\'"abfnrtv]  # Single-character escapes
    )''', re.UNICODE | re.VERBOSE)

def decode_escapes(s):
    def decode_match(match):
        return codecs.decode(match.group(0), 'unicode-escape')

    return ESCAPE_SEQUENCE_RE.sub(decode_match, s)

# specific strings to look for in the turtl_backup json:
start_delimiter = '"text":'
end_delimiter = '"type:"'

# parse command line arguments:
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input-file", required=True, help="input filename")
parser.add_argument("-o", "--output-dir", required=True, help="output directory")

args = parser.parse_args()

# read the input file:
with open(args.input_file, 'r') as input_file:
    input_data = input_file.read()

# create list iterator to iterate through the input data by line:
input_lines = iter(input_data.splitlines())

#find text and title of each note:
for line in input_lines:
    if start_delimiter in line:
        
        print_line = line.replace('"text": ','').lstrip().lstrip('"').rstrip('"').rstrip(',')
        filename = (next(input_lines))
        title = filename.replace('"title": "','## ').lstrip().rstrip(',').rstrip('"')
        decoded_line = decode_escapes(print_line)
        print(title)
        print(decoded_line)
    # extract the output filename from the start delimiter,stripping leading whitespace & symbols, add markdown extension:
        output_filename = filename.lstrip().replace('(','').replace(')','').replace('"title": ','').strip('"').replace(',','').replace(' ','_').replace('…','').replace('“','').replace('”','').replace('/','_').replace('\\','_' ).replace(':','-').replace("'",'').replace('"','')+'.md'
        # if note has no title, generate filename using random #s (not foolproof against conflicts!):
        if output_filename == ".md":
            output_filename = "note_{0}{1}".format(random.randint(1,21),(random.randint(1,21)))+".md"

        output_path = os.path.join(args.output_dir, output_filename)

    # open the output file:
        #print("extracting file: {0}".format(output_path))

        #with open(output_path, 'w') as output_file:
            #output_file.write("{0}\n".format(title) + "{0}\n".format(decoded_line))
            

        


###run with python3 new_splitfile.py -i input-file.txt -o ./output-folder/ 