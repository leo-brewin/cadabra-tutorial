#!/usr/local/bin/python3

import re
import sys
import os.path

import enum

class Type (enum.Enum):
   BegTag    = 1
   EndTag    = 2
   PlainText = 3
   Unknown   = 4

def empty_line (this_line):
   if len(this_line) == 0:
      return True
   else:
      return re.search ("(^ *$)",this_line)

def get_index (this_line):
   result = re.search ("tag([0-9]+)",this_line)
   if result:
      return int(result.group (1))
   else:
      print ("> Error reading tag index on: " + this_line)
      sys.exit (1)

def get_text (this_line):
   result = re.search ("tag([0-9]+)=(.*)",this_line)
   if result:
      return result.group (2)
   else:
      print ("> Error reading tag text on: " + this_line)
      sys.exit (1)

def has_tag (this_line):
   return re.search (r"(tag[0-9]+=)",this_line)

def is_beg_tag (this_line):
   return re.search (r"(^beg_tag[0-9]+$)",this_line)

def is_end_tag (this_line):
   return re.search (r"(^end_tag[0-9]+$)",this_line)

# -------------------------------------------------------------------------
#  stack operations

stack = []
stack_index = 0
max_stack_index = 5
for i in range (0,max_stack_index):   # create an empty stack
   stack.append(0)  # using zero forces any non-tagged output to be stored in tag_output[0]

def read_stack (index):
   return stack [index]

def push_stack (index, stack_index):
   if stack_index < max_stack_index:
      stack_index = stack_index + 1
      stack [stack_index] = index
      return stack_index
   else:
      print ("> Depth of nested pyBeg/pyEnd pairs exceeded, max = "+str(max_stack_index)+", exit\n")
      sys.exit (1)

def pop_stack (index, stack_index):
   if stack_index > 0:
      if index == read_stack (stack_index):
         stack [stack_index] = 0
         return stack_index - 1
      else:
         print ("> Error with pyBeg/pyEnd pairs for tag index: "+str(index)+", exit\n")
         sys.exit (1)
   else:
      print ("> Error with pyBeg/pyEnd pairs, check for missing pyBeg or pyEnd, exit\n")
      sys.exit (1)

def parse (this_line):
   if is_beg_tag (this_line):
      return Type.BegTag
   elif is_end_tag (this_line):
      return Type.EndTag
   else:
      return Type.PlainText

def append_text (this_line, index):
   tag_output[index].append(this_line.rstrip("\n"))

def copy_text (out, index):
   the_lines = tag_output [index]
   for i in range (0,len(the_lines)):
      out.write (the_lines[i]+"\n")

# -----------------------------------------------------------------------------
# the main code

import argparse

parser = argparse.ArgumentParser(description="Post-process Python output")
parser.add_argument("-i", dest="input",  metavar="source",    help="LaTeX-Python source file (without .tex file extension)", required=True)
parser.add_argument("-o", dest="output", metavar="output",    help="Where to save the copied text, full file name.", required=True)
parser.add_argument("-t", dest="tag",    metavar="target",    help="Target tag, copy the text of this tag.", required=True)
parser.add_argument("-W", dest="warn",   action='store_true', help="Report errors for missing output")

inp_file_name  = parser.parse_args().input
out_file_name  = parser.parse_args().output
the_target_tag = parser.parse_args().tag
report_errors  = parser.parse_args().warn

# ----------------------------------------------------------------------------
# file names

idx_file_name = inp_file_name + ".pyidx"
src_file_name = inp_file_name + ".pytxt"

# ----------------------------------------------------------------------------
# any tag index/name pairs to read?

if not os.path.isfile (idx_file_name):
   with open(out_file_name,"w") as out:
      out.write ("% no Python output")
   sys.exit (0)

# ----------------------------------------------------------------------------
# read tag index/name pairs

tag_name   = [""]     # dummy entry at index = 0
tag_done   = [False]  # ditto
tag_found  = [False]  # ditto
tag_output = [[]]     # ditto
num_tag    = 0
tag_index  = 0

target = 1 # default is the first tag

with open(idx_file_name, "r") as idx:
   for this_line in idx:
      if has_tag (this_line): # skip any non-tag text (e.g., comments)
         num_tag = num_tag + 1                       # the tag index
         tag_name.append (get_text (this_line))      # the tag name
         tag_done.append (False)
         tag_found.append (False)
         tag_output.append ([])
         the_name = get_text (this_line)
         if the_name == the_target_tag:
            target = num_tag

# note: num_tag = number of tags declared in the Python/LaTeX source
#       these tags are stored in locations 1,2,3 ... num_tag in the various arrays
#       tag_output[0] will contain all non-tagged Python output.

# ----------------------------------------------------------------------------
# read Python output and create LaTeX macros for each tag

if num_tag == 0:
   with open(out_file_name,"w") as out:
      out.write ("% no Python output")
else:

   if not os.path.isfile (src_file_name):
      with open(out_file_name,"w") as out:
         out.write ("% no Python output")
      print ("> post-process: Source file " + src_file_name + " not found, exit.")
      print ("> possible error during execution of Python.")
      sys.exit (1)

   # -------------------------------------------------------------------------
   # read Python output

   with open(src_file_name,"r") as src:
      for this_line in src:

         line_type = parse (this_line)
         if line_type == Type.BegTag:

            tag_index = get_index (this_line)
            tag_done   [tag_index] = False
            tag_found  [tag_index] = True
            stack_index = push_stack (tag_index,stack_index)

         elif line_type == Type.EndTag:

            tag_index = get_index (this_line)
            tag_done   [tag_index] = True
            tag_found  [tag_index] = True
            stack_index = pop_stack  (tag_index,stack_index)
            tag_index = read_stack (stack_index)

         elif line_type == Type.PlainText:

            append_text (this_line,tag_index)

         else:
            pass # should never get here

   # -----------------------------------------------------------------------
   # create the latex macros, one for each tag

   with open(out_file_name,"w") as out:

      copy_text (out, target)

   if report_errors:

      # -------------------------------------------------------------------------
      # report tags that didn't have matching Python output

      for i in range (1,num_tag+1):
         if not tag_found [i]:
            print ("> post-process: Failed to find output for tag: "+tag_name[i])

      # -------------------------------------------------------------------------
      # report problems with un-matched beg/end pairs

      for i in range (1,num_tag+1):
         if not tag_done [i]:
            print ("> post-process: Something is missing for tag: "+tag_name[i])
