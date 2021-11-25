# use this for Cadabra objects
def cdb_write_code (ex,name,filename,num):

    import os

    import sympy as sym

    # -- 24 sep 2021 ----------------------------------------- old
    # from sympy.printing.ccode import C99CodePrinter as printer
    # from sympy.printing.codeprinter import Assignment
    # -- 24 sep 2021 ----------------------------------------- new
    # changes due to upgrade of SymPy to v 1.7
    from sympy.printing.c import C99CodePrinter as printer
    from sympy.codegen.ast import Assignment
    # -------------------------------------------------------- 24 sep 2021

    # this block for scalars
    if num == 0:

       mat = sym.Matrix([ex._sympy_()])             # row vector with one term

       sub_exprs, simplified_rhs = sym.cse(mat)     # optimise code

       with open(os.getcwd() + '/' + filename, 'w') as out:

          for lhs, rhs in sub_exprs:
             out.write(printer().doprint(Assignment(lhs, rhs))+'\n')

          for index, rhs in enumerate (simplified_rhs[0]):
             lhs = sym.Symbol(name)
             out.write(printer().doprint(Assignment(lhs, rhs))+'\n')

    # this block for tensors
    else:

       idx=[]  # indices in the form [{x, x}, {x, y} ...]
       lst=[]  # corresponding terms [termxx, termxy, ...]

       for i in range( len(ex[num]) ):                  # num = number of free indices
           idx.append( str(ex[num][i][0]._sympy_()) )   # indices for this term
           lst.append( str(ex[num][i][1]._sympy_()) )   # the matching term

       mat = sym.Matrix([lst])                          # row vector of terms

       sub_exprs, simplified_rhs = sym.cse(mat)         # optimise code

       with open(os.getcwd() + '/' + filename, 'w') as out:

          for lhs, rhs in sub_exprs:
             out.write(printer().doprint(Assignment(lhs, rhs))+'\n')

          for index, rhs in enumerate (simplified_rhs[0]):
             lhs = sym.Symbol(name+' ('+idx[index][1:-1]+')')
             # lhs = sym.Symbol(name+' '+(idx[index]).replace(', ',']['))
             out.write(printer().doprint(Assignment(lhs, rhs))+'\n')

# use this for Python objects
def py_write_code (lst,idx,name,filename):

    import os

    import sympy as sym

    # -- 24 sep 2021 ----------------------------------------- old
    # from sympy.printing.ccode import C99CodePrinter as printer
    # from sympy.printing.codeprinter import Assignment
    # -- 24 sep 2021 ----------------------------------------- new
    # changes due to upgrade of SymPy to v 1.7
    from sympy.printing.c import C99CodePrinter as printer
    from sympy.codegen.ast import Assignment
    # -------------------------------------------------------- 24 sep 2021

    mat = sym.Matrix([lst])                   # row vector of terms

    sub_exprs, simplified_rhs = sym.cse(mat)  # optimise code

    with open(os.getcwd() + '/' + filename, 'w') as out:

       for lhs, rhs in sub_exprs:
          out.write(printer().doprint(Assignment(lhs, rhs))+'\n')

       # this block for scalars
       if len(idx) == 0:

          for index, rhs in enumerate (simplified_rhs[0]):
             lhs = sym.Symbol(name)
             out.write(printer().doprint(Assignment(lhs, rhs))+'\n')

       # this block for matrices
       else:

          for index, rhs in enumerate (simplified_rhs[0]):
             lhs = sym.Symbol(name+' ('+idx[index][1:-1]+')')
             # lhs = sym.Symbol(name+' '+(idx[index]).replace(', ',']['))
             out.write(printer().doprint(Assignment(lhs, rhs))+'\n')
