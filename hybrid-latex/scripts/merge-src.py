#!/usr/local/bin/python3

import re
import sys
import os.path

max_recurse_depth = 10 # limit depth of nested \Input statements

re_comment  = re.compile (r"^\s*%")
re_inc_file = re.compile (r'^\s*(\\|\$)Input\{"([_a-zA-Z0-9./-]+)"\}') # use \Input to avoid confusion with \input
re_dirname  = re.compile (r"([_a-zA-Z0-9./-]*\/)")                     # as per dirname in bash
re_file_ext = re.compile (r'(\.[a-z]+)"')
re_uuid     = re.compile (r'(.*?)(uuid):([a-fA-F0-9]{8}-[a-fA-F0-9]{4}-4[a-fA-F0-9]{3}-[89abAB][a-fA-F0-9]{3}-[a-fA-F0-9]{12})')

def make_str (num,digits):
    return '{number:0{width}d}'.format(number=num,width=digits)

def include_files (txt, prev_path, this_line, prev_indent, recurse_depth):

   def grep (this_line, regex, the_group):
       result = regex.search (this_line)
       if result:
          found = True
          group = result.group (the_group)
       else:
          found = False
          group = ""
       return group, found

   def is_include_file (the_line):
       return re_inc_file.search (the_line)

   def absolute_path (the_path, the_line):
       tmp_path, dummy = grep (the_path, re_dirname, 1)
       new_path, dummy = grep (the_line, re_inc_file, 2)
       return tmp_path + new_path

   def absolute_indent (the_indent, the_line):
       start = 0
       for i in range (0,len(the_line)):
          if the_line[i] != ' ':
             start = i
             break
       return start + the_indent

   def set_comment (the_line):
       the_ext, found = grep (the_line, re_file_ext,1)
       if found:
          if the_ext == ".tex":
             return "%"
          elif the_ext == ".py":
             return "#"
          elif the_ext == ".cdb":
             return "#"
          elif the_ext == ".ads":
             return "--"
          elif the_ext == ".adb":
             return "--"
          else:
             return "#"
       else:
          return "#"

   def filter (the_line):
       # "uuid" is reserved for the original source
       # the new file being created by this job must use a prefix other than "uuid"
       # replace the prefix "uuid" with "file"
       result = re_uuid.search (the_line)
       if result:
          return re_uuid.sub ("\\1file:\\3",the_line) # will truncate any text following the uuid
       else:
          return the_line

   recurse_depth = recurse_depth + 1

   if recurse_depth > max_recurse_depth:
      print ("> merge-src.py: Too many nested Input{...}'s (max = "+str(max_recurse_depth)+"), exit")
      sys.exit(1)

   the_path   = absolute_path (prev_path, this_line)
   the_indent = absolute_indent (prev_indent, this_line)
   comment    = set_comment (this_line)

   if markup:
      # print (type(comment))
      # print (type(the_path))
      txt.write (the_indent*" "+comment + " beg" + make_str(recurse_depth,2) + ": ./" + the_path + "\n")

   if not os.path.isfile (the_path):
      print ("> merge-src.py: Include file " + the_path + " not found, exit.\n")
      sys.exit(1)

   with open (the_path,'r') as src:

      for the_line in src:

         the_line = filter (the_line)

         if is_include_file (the_line):
            recurse_depth = include_files (txt, the_path, the_line, the_indent, recurse_depth)
         else:
            txt.write (the_indent*" "+str(the_line))

   if markup:
      txt.write (the_indent*" "+comment + " end" + make_str(recurse_depth,2) + ": ./" + the_path + "\n")

   recurse_depth = recurse_depth - 1

   return recurse_depth

# -----------------------------------------------------------------------------
# the main code

import argparse

parser = argparse.ArgumentParser(description="Merge a sequence of LaTeX files into a single LaTeX file")
parser.add_argument("-i", dest="input", metavar="foo.tex", help="source file", required=True)
parser.add_argument("-o", dest="output", metavar="bah.tex", help="output file", required=True)
parser.add_argument("-S", dest="silent", default="False", action='store_true', help="suppress markup lines for each \\Input{foo.tex}", required=False)

src_file_name = parser.parse_args().input
out_file_name = parser.parse_args().output

silent = parser.parse_args().silent

if silent == "False":
   markup = True
else:
   markup = False

if src_file_name == out_file_name:
   print ("> merge-src.py: Indentical files names for input and output, exit.")
   sys.exit (1)

if not os.path.isfile (src_file_name):
   print ("> merge-src.py: Source file " + src_file_name + " not found, exit.")
   sys.exit (1)

with open (out_file_name,"w") as txt:

   the_indent = 0
   recurse_depth = 0

   recurse_depth = include_files (txt, "", ""'\\Input{"' + src_file_name + '"}', the_indent, recurse_depth)

if not recurse_depth == 0:
   print("> merge-src.py: error during merger")
   print("> recursion depth should be zero, actual value: "+str(recurse_depth))
