#!/usr/local/bin/python3

import re
import sys
import os.path

re_beg_python_environ     = re.compile (r'^\s*\\begin{python}')
re_end_python_environ     = re.compile (r'^\s*\\end{python}')

re_beg_python_verbatim    = re.compile (r'^\s*\\PySetup{(.*?)action=verbatim')
re_end_python_verbatim    = re.compile (r'^\s*\\PySetup{(.*?)action=(show|hide)')

re_beg_latex_document     = re.compile (r'^\s*\\begin{document}')
re_end_latex_document     = re.compile (r'^\s*\\end{document}')

re_indent         = re.compile (r'(^\s*)')
re_assignment     = re.compile (r'(^\s*)([a-zA-Z0-9_.]+\s*=)')
re_empty_line     = re.compile (r'(^\s*$)')
re_latex_comment  = re.compile (r'(^\s*%)')
re_python_comment = re.compile (r'(^\s*#)')
re_python_markup  = re.compile (r'(#\s*(py\s*\(|pyBeg\s*\(|pyEnd))')
re_hidden_markup  = re.compile (r'(^\s*#.*#\s*(py\s*\(|pyBeg\s*\(|pyEnd))')
re_pure_markup    = re.compile (r'(^\s*#\s*(py\s*\(|pyBeg\s*\(|pyEnd))')
re_capture        = re.compile (r'(#\s*((pyBeg|pyEnd)\s*\(\s*([a-zA-Z0-9_.]+)\)))')
re_beg_capture    = re.compile (r'(#\s*(pyBeg\s*\(\s*([a-zA-Z0-9_.]+)\)))')
re_end_capture    = re.compile (r'(#\s*(pyEnd\s*(\(\s*([a-zA-Z0-9_.]+)\))?))')
re_py_tag         = re.compile (r'(#\s*(py\s*\(\s*([a-zA-Z0-9_.]+)\s*(,\s*([a-zA-Z0-9_]+)\s*)?\)))')
                               # Allow two forms of tag, py(foo,bah) and py(bah).
                               # In both cases bah must be a valid python expression.

def make_str (num,digits):
    return '{number:0{width}d}'.format(number=num,width=digits)

def grep (this_line, regex, the_group):
    result = regex.search (this_line)
    if result:
       found = True
       the_beg = result.start (the_group)
       the_end = result.end (the_group)
    else:
       found = False
       the_beg = -1
       the_end = -1
    return the_beg, the_end, found

def not_empty_line (this_line):
    return not re_empty_line.search (this_line)

def not_latex_comment (this_line):
    return not re_latex_comment.search (this_line)

def not_python_comment (this_line):
    return not re_python_comment.search (this_line)

def is_assignment (this_line):
    return re_assignment.search (this_line)

def is_beg_latex_document (this_line):
    return re_beg_latex_document.search (this_line)

def is_end_latex_document (this_line):
    return re_end_latex_document.search (this_line)

def is_beg_python_environ (this_line):
    return re_beg_python_environ.search (this_line)

def is_end_python_environ (this_line):
    return re_end_python_environ.search (this_line)

def is_beg_python_verbatim (this_line):
    return re_beg_python_verbatim.search (this_line)

def is_end_python_verbatim (this_line):
    return re_end_python_verbatim.search (this_line)

def has_beg_python_capture (this_line):
    return re_beg_capture.search (this_line)

def has_end_python_capture (this_line):
    return re_end_capture.search (this_line)

def has_python_tag (this_line):
    return re_py_tag.search (this_line)

def has_python_markup (this_line):
    return re_python_markup.search (this_line)

def not_python_markup (this_line):
    return not re_python_markup.search (this_line)

def not_hidden_markup (this_line):
    return not re_hidden_markup.search (this_line)

def not_pure_python_markup (this_line):
    return not re_pure_markup.search (this_line)

def filter_python_markup (this_line):
    if len(this_line) == 0:
       return ""
    else:
       if has_python_markup (this_line):
          the_beg,the_end,found = grep (this_line,re_python_markup,1)
          if the_beg > 0 :
             return this_line[0:the_beg].rstrip(" ")
          else:
             return this_line.rstrip("\n")
       else:
          return this_line.rstrip("\n")

# -----------------------------------------------------------------------------
# 1st pass: copy Python source from source.tex to source.py file
#           leave in-line comments in place, these will be removed in pass2

def pass1 (src_file_name, out_file_name, the_file_name):

   global num_head_lines

   in_latex_document = False
   in_python_environ = False
   in_python_verbatim = False

   # --------------------------------------------------------------------------
   # find the first non-empty, non-comment line in the Python blocks
   # record the indent of that line

   indent_num = 0 # number of leading spaces of first non-trivial Python line

   with open(src_file_name, "r") as src:
      for this_line in src:
         if not_latex_comment (this_line):
            if in_latex_document:
               if is_end_latex_document (this_line):
                  in_latex_document = False
                  break
               else:
                  if is_beg_python_verbatim (this_line):
                     in_python_verbatim = True
                  elif is_end_python_verbatim (this_line):
                     in_python_verbatim = False
                  if in_python_environ:
                     if is_end_python_environ (this_line):
                        in_python_environ = False
                     else:
                        if not in_python_verbatim:
                           if len(this_line) > 1:
                              if not_python_comment (this_line):
                                 the_beg,the_end,found = grep (this_line,re_indent,1)
                                 if not found:
                                    print ("> read error in preproc/pass1")
                                    print ("> line: "&this_line)
                                    sys.exit (1)
                                 else:
                                    indent_num = the_end - the_beg  # number of leading spaces
                                    break
                  else:
                     if is_beg_python_environ (this_line):
                        in_python_environ = True
            else:
               if is_beg_latex_document (this_line):
                  in_latex_document = True

   # --------------------------------------------------------------------------
   # collect the Python begin/end blocks and write to a single file
   # will also shift the text to the left edge (while maintaing correct indentation)
   # the number of spaces to shift left equals indent_num which was computed in the above block

   in_latex_document = False
   in_python_environ = False
   in_python_verbatim = False

   with open (src_file_name,"r") as src:
      with open (out_file_name,"w") as out:

         num_head_lines = 11  # used later when cleaning out all markup
                              # must match exactly the number of header lines

         out.write ("# ----------------------------------------------\n")
         out.write ("# auto-generated from " + src_file_name + "\n")
         out.write ("# ----------------------------------------------\n")

         out.write ("def Print (obj):\n")
         out.write ("    import sympy as sp\n")
         out.write ("    try:\n")
         # following convoluted construction is to avoid an exception when
         # using sympy/symengine objects
         if mixed:
            out.write ("        print(sp.latex(sp.sympify(str(obj)),long_frac_ratio=1))\n")
         else:
            out.write ("        print(sp.latex(obj,long_frac_ratio=1))\n")
         out.write ("    except:\n")
         # print a raw string version of obj when an exception occured above
         out.write ("        print(obj)\n")
         out.write ("# ----------------------------------------------\n\n")

         for this_line in src:

            if not_latex_comment (this_line):
               if in_latex_document:
                  if is_end_latex_document (this_line):
                     in_latex_document = False
                     break
                  else:
                     if is_beg_python_verbatim (this_line):
                        in_python_verbatim = True
                     elif is_end_python_verbatim (this_line):
                        in_python_verbatim = False

                     if in_python_environ:
                        if is_end_python_environ (this_line):
                           in_python_environ = False
                           out.write("\n") # force blank line after every python code block
                        else:
                           if not in_python_verbatim:
                              if len(this_line) > 0:
                                 the_beg,the_end,found = grep (this_line,re_indent,1)
                                 start = min(indent_num,the_end-the_beg)
                                 out.write (this_line[start:len(this_line)-1]+"\n")  # use 0: to retain indent
                              else:
                                 out.write("\n")

                     else:
                        if is_beg_python_environ (this_line):
                           in_python_environ = True

               else:
                  if is_beg_latex_document (this_line):
                     in_latex_document = True

# -----------------------------------------------------------------------------
# 2nd pass: use the source.py (from pass1) file to build the following files

# source_.py : annotated file, contains extra lines to generate output for later capture
# source.pyidx : a list of tags, one line per tag, written as: tag index = tag name

def pass2 (src_file_name, out_file_name, idx_file_name):

   # -----------------------------------------------------------
   #  read functions, extract tag and expressions names

   def get_tag (this_line):
      the_beg,the_end,found = grep (this_line,re_py_tag,3)
      if found:
         return this_line[the_beg:the_end].strip(" ")
      else:
         return this_line.strip(" ")

   def get_exp (this_line):
      the_beg,the_end,found = grep (this_line,re_py_tag,5)
      if found and (the_beg > 0) and (the_end > 0):
         return this_line[the_beg:the_end].strip(" ")     # returns foo given py (foo,bah)
      else:
         return get_tag (this_line)                       # returns bah given py (bah)

   def get_src (this_line):
      the_beg,the_end,found = grep (this_line,re_py_tag,1)
      if found:
         if the_beg == 0:
            return ""
         else:
            return this_line [0:the_beg-1].rstrip(" ")
      else:
         return this_line.rstrip(" ")

   def get_indent (this_line):
      the_beg,the_end,found = grep (this_line,re_indent,1)
      if found:
         if the_beg == the_end:
            return ""
         else:
            return this_line [the_beg:the_end]
      else:
         return ""

   def get_capture (this_line):
      the_beg,the_end,found = grep (this_line,re_capture,4)
      if found:
         return this_line[the_beg:the_end].strip(" ")
      else:
         return this_line.strip(" ")

   def beg_capture_src (this_line):
      the_beg,the_end,found = grep (this_line,re_beg_capture,1)
      if found:
         if the_beg > 0:
            return this_line [0:the_beg-1].rstrip(" ")
         else:
            return ""
      else:
         return this_line.rstrip(" ")

   def end_capture_src (this_line):
      the_beg,the_end,found = grep (this_line,re_end_capture,1)
      if found:
         if the_beg > 0:
            return this_line [0:the_beg-1].rstrip(" ")
         else:
            return ""
      else:
         return this_line.rstrip(" ")

   # ----------------------------------------------------------
   #  output functions, writes to index file, temp files etc.

   def beg_tag (num):
      return 'print("beg_tag'+make_str(num,4)+'")'

   def end_tag (num):
      return 'print("end_tag'+make_str(num,4)+'")'

   def beg_capture (num):
      return beg_tag (num)

   def end_capture (num):
      return end_tag (num)

   def wrt_latex (this_line):
      this_text = get_exp (this_line)
      return "Print("+this_text+")"

   # -------------------------------------------------------------------------
   #  stack operations

   stack = []
   tag_name = []
   stack_index = 0
   max_stack_index = 5
   for i in range (0,max_stack_index+1):   # create an empty stack
      stack.append(-1)
      tag_name.append("")

   def read_stack (index):
      return stack [index]

   def push_stack (index, this_line, stack_index):
      if stack_index < max_stack_index:
         stack_index = stack_index + 1
         stack [stack_index] = index
         tag_name [stack_index] = get_capture (this_line)
         return stack_index
      else:
         print ("> Depth of nested pyBeg/pyEnd pairs exceeded, max = "+str(max_stack_index)+", exit")
         sys.exit (1)

   def pop_stack (index, this_line, stack_index):
      if stack_index > 0:
         tmp_name = get_capture (this_line)
         if tmp_name == tag_name [stack_index]:
            stack [stack_index] = -1
            return stack_index - 1
         else:
            print ("> Error in pyBeg/pyEnd pair for tag: "+str(tag_name[index])+", exit")
            sys.exit (1)
      else:
         print ("> Error with pyBeg/pyEnd pairs, check for missing pyBeg or pyEnd, exit")
         sys.exit (1)

   # create a temporary copy of the Python source

   from shutil import copyfile
   from uuid   import uuid4

   tmp_file_name = "/tmp/"+str(uuid4())
   copyfile (src_file_name,tmp_file_name)

   # create an annotated _.py and .pyidx files using the temporary file as source

   with open (out_file_name,"w") as out:
      with open (idx_file_name,"w") as idx:
         with open (tmp_file_name,"r") as src:

            tag_index = 0
            indent = ""

            for this_line in src:

               if not_python_comment (this_line) and not_empty_line (this_line):
                  if is_assignment (this_line):
                     indent = get_indent (this_line)

               if has_python_markup (this_line) and not_hidden_markup (this_line):

                  if has_beg_python_capture (this_line):

                     tag_index = tag_index + 1

                     out.write ( beg_capture_src (this_line) + "\n")
                     out.write ( beg_capture (tag_index) + "\n" )

                     idx.write ("tag"+make_str(tag_index,4)+"=")
                     idx.write ( get_capture (this_line) + "\n")

                     stack_index = push_stack (tag_index,this_line,stack_index)

                  elif has_end_python_capture (this_line):

                     out.write ( end_capture_src (this_line) + "\n" )
                     out.write ( end_capture (read_stack (stack_index)) + "\n")

                     stack_index = pop_stack (read_stack (stack_index),this_line,stack_index)

                  elif has_python_tag (this_line):

                     tag_index = tag_index + 1

                     out.write (         get_src   (this_line) + "\n")
                     out.write (indent + beg_tag   (tag_index) + "\n")
                     out.write (indent + wrt_latex (this_line) + "\n")
                     out.write (indent + end_tag   (tag_index) + "\n")

                     idx.write ("tag"+make_str(tag_index,4) + "=")
                     idx.write ( get_tag (this_line) + "\n")

                  else:

                     out.write (filter_python_markup (this_line)+"\n")

               else:

                  out.write (filter_python_markup (this_line)+"\n")

   # copy the temporary file back to the source with in-line comments removed
   # note: this clean copy is just for reference, it's never used

   num_line = 0 # use num_line to help skip header text added in pass 1
                # there are exactly num_head_lines in the header text

   with open (tmp_file_name,"r") as tmp:
      with open (src_file_name,"w") as src:
         for this_line in tmp:
            num_line = num_line + 1
            if num_line > num_head_lines:
               if not_pure_python_markup (this_line):
                  src.write (filter_python_markup (this_line)+"\n")

# -----------------------------------------------------------------------------
# the main code

import argparse

parser = argparse.ArgumentParser(description="Pre-process LaTeX-Python source")
parser.add_argument("-i", dest="input", metavar="input", help="LaTeX-Python source file (without .tex file extension)", required=True)
parser.add_argument("-m", dest="name", metavar="name", help="Merged LaTeX-Python source file (without .tex file extension)")
parser.add_argument("-M", dest="mixed", help="LaTeX-Python source contains mixed sympy/symengine code",   action='store_true')

src_file_name = parser.parse_args().input
mrg_file_name = parser.parse_args().name

mixed = parser.parse_args().mixed

if not mrg_file_name:

   if not os.path.isfile (src_file_name + ".tex"):
      print ("> pre-process: Source file " + src_file_name + ".tex" + " not found, exit.")
      sys.exit (1)

   pass1 (src_file_name + ".tex", src_file_name +  ".py", src_file_name)
   pass2 (src_file_name + ".py",  src_file_name + "_.py", src_file_name + ".pyidx")

else:

   if not os.path.isfile (mrg_file_name + ".tex"):
      print ("> pre-process: Source file " + mrg_file_name + ".tex" + " not found, exit.")
      sys.exit (1)

   pass1 (mrg_file_name + ".tex", src_file_name +  ".py", src_file_name)
   pass2 (src_file_name + ".py",  src_file_name + "_.py", src_file_name + ".pyidx")
