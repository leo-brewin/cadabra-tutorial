# A tutorial on Cadabra

## Overview

[Cadabra][1] is an open access program ideally suited to complex tensor computations in General Relativity. Tensor expressions are written in LaTeX while an enhanced version of Python is used to control the computations. This tutorial assumes no prior knowledge of Cadabra. It consists of a series of examples covering a range of topics from basic syntax such as declarations, functions, program control, component computations, input and output through to complete computations including a derivation of the BSSN equations from the ADM equations. Numerous exercises are included along with complete solutions.

All of the sources for the tutorial (including the examples and exercises) are written with the Cadabra sources embedded in LaTeX documents. Simple tools are used to extract and execute the embedded Cadabra source while also capturing the output and making it available elsewhere in the LaTeX document. These tools have been cloned from the [Hybrid-LaTeX][2] project and can be found in the `hybrid-latex/` directory. A copy of the documentation for the Hybrid-LaTeX project is also included in the `hybrid-latex/` directory.

Note that the hybrid LaTeX tools are not essential in order to work through the project. The raw Cadabra files (stripped bare of any of the hybrid Latex markup) can be found in `source/cadabra/cdb/`. They can be run either at the command line or copied into the Cadabra2 gui. Using just the raw Cadabra files does have one disadavantage -- the formatting of the Cadabra output will not appear exactly as shown in the tutorial's pdf files (in `pdf/`).

It is highly recommended that you do install the hybrid LaTeX tools as their use greatly simplifies any experiments you might want to run on the included examples. The tools are also of use in their own right (see for example the collection of examples in the [Hybrid-LaTeX][2] project).

## Documentation

The complete tutorial, examples and solutions to the exercises are provided as pdf files (in `pdf/`) as well as the full LaTeX/Cadabra sources (in `sources/tex`, `sources/cadabra` and  `sources/cadabra/exrecises`).

## Installation

Full details on how to install Cadabra can be found on the [Cadabra repository][3].

If you chose not to use the hybrid latex files then there is no installation required (apart from Cadabra).

The simplest way to install the hybrid latex files is to run the command

    $ source SETPATHS; make install

from the top directory. This will copy the files to newly created directories while also adjusting the various paths to make these files visible to LaTeX, Maple, Mathematic etc. The files, the new directories and their associated paths are as given in the following table.

|  Directory  | Content | Path variable |
|:------------:|:--------|:-------------|
| `$HOME/local/cadabra-tutorial/bin/` | Python and Shell scripts | `$PATH` |
| `$HOME/local/cadabra-tutorial/lib/` | Python libraries | `$PYTHONPATH` |
| `$HOME/local/cadabra-tutorial/tex/` | LaTeX files | `$TEXINPUTS` |

The command `source SETPATHS` will __prepend__ the directories to the appropriate paths while the command `make install` copies the files to their destinations. If you need to recover the original paths, just run `source OLDPATHS`.

If you prefer to install the hybrid latex files in some other directory then you can run the command

    $ source SETPATHS /full/path/to/dir/; make install

where /full/path/to/dir/ is the full path to your prefered directory. The `bin`, `lib` and `tex` directories will be ceated underneath this directory.

## Uninstall

The hybrid latex tools can be uninstalled by deleting the directory `$HOME/local/cadabra-tutorial/` (or the approrpriate directory if you chose a non-default installation).

## Running the examples

To build everything from scratch just run

    $ build.sh

from the top directory. This will run Cadabra and LaTeX on each of the sources in `source/cadabra/` and `source/tex/`. Some of the Cadabra codes will take a few minutes to run (see `source/cadabra/TIME.txt` for a list of approximate times).

Makefiles are also provided so you can build individual codes, for example `source/cadabra/example-03`, using

    $ cd source/cadabra
    $ make example-03

You can also compile `source/cadabra/example-03` without using `make` by executing

    $ cd source/cadabra
    $ cdblatex.sh -i example-03

This should generate the `example-03.pdf` file (along with a few other support files). A list of the command line options for `cdblatex.sh` can be found using

    $ cdblatex.sh -h

The command line option `-k` will keep all intermediate files and can be useful when trying to locate errors.

The `cdblatex.sh` script will attempt to open the pdf file. You may need to edit that script to use the correct pdf viewer for your platform.

If you are not using the hybrid latex tools then you would type

    $ cd source/cadabra/cdb
    $ cadabra2python example-03.cdb example-03.py
    $ cadabra2 example-03.py

This will produce plain text output.

You could also copy and paste `example-03.cdb` into the Cadabra2 gui.

## Testing

You can check your installation by running (from the command line)

    $ cd source/cadabra/
    $ make
    $ make tests

If all goes well then you should see a few lines like

    > diff example-01.cdbtex
    > diff example-02.cdbtex
    > diff example-03.cdbtex
    > diff example-04.cdbtex

There will be more lines (from the other examples). The key thing to observe is that each `diff` command produces no output. There are also some tests that do not use the `diff` command. These tests are run by Cadabra. It reads in the expected results and compares them with the actual results printing out any differences (this allows for non-important differences in expressions to be ignored, for example reordering a sum). The results of those (semantic) tests are recorded in `source/cadabra/tests/semantic/summary.pdf`.

There are similar tests for the exercises (see `source/cadabra/exercises/`).

## Dependencies

You will need the Cadabra/Python/SymPy software.

### Cadabra

Cadabra is easy to compile and install. Full details can be found on the [Cadabra repository][3].

### Python/SymPy

The codes have been tested with both Python2 and Python3. Since Python2 is deprecated it would be wise to use Python3. A popular distribution of Python3 can be found at the [Anaconda website][4].

## License

All files in this collection are distributed under the [MIT][5] license. See the file LICENSE.txt for the full details.

  [1]: https://cadabra.science
  [2]: https://github.com/leo-brewin/hybrid-latex
  [3]: https://github.com/kpeeters/cadabra2
  [4]: https://www.anaconda.com/products/individual
  [5]: https://opensource.org/licenses/MIT
