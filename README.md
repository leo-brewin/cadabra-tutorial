# A tutorial on Cadabra

## Overview

[Cadabra][1] is an open access program ideally suited to complex tensor commutations in General Relativity. Tensor expressions are written in LaTeX while an enhanced version of Python is used to control the computations. This tutorial assumes no prior knowledge of Cadabra. It consists of a series of examples covering a range of topics from basic syntax such as declarations, functions, program control, component computations, input and output through to complete computations including a derivation of the BSSN equations from the ADM equations. Numerous exercises are included along with complete solutions.

All of the sources for the tutorial (including the examples and exercises) are written with the Cadabra sources embedded in a LaTeX documents. Simple tools are used to extract and execute the embedded Cadabra source while also capturing the output and making it available elsewhere in the LaTeX document. These tools have been cloned from the [hybrid-latex][2] project and can be found in the `support/` directory. A copy of the documentation for the Hybrid-LaTeX project is also included in the `support/` directory.

Note that the hybrid LaTeX tools are not essential in order to work through the project. The raw Cadabra files (stripped bare of any of the Hybrid-Latex markup) are also included (e.g., `foo.cdb` is the Cadabra source extracted from the LaTeX file `foo.tex`). These can be run either at the command line or copied into the Cadabra2 gui. Though taking this approach does mean that the formatting of the Cadabra output will not appear exactly as shown in the tutorial's pdf files (in `pdf/`).

## Documentation

The complete tutorial, examples and solutions to the exercises are provided as pdf files (in `pdf/`) as well as the full LaTeX/Cadabra sources (in `sources/tex`, `sources/cadabra` and  `sources/cadabra/exrecises`).

## Installation

Full details on how to install Cadabra can be found on the [Cadabra repository][3].

If you chose not to use the Hybrid-Latex tools then there is no installation required (apart from Cadabra).

If you do choose to use the Hybrid-LaTeX tools you will need to copy a few files into appropriate places. The tools include Bash and Python shell scripts (`support/shell`), Python libraries (`support/python`) and LaTeX style files (`support/latex`). Each file can be copied to wherever their respective program expects to find them. For example, the shell scripts could be sudo copied to `/usr/local/bin` (for access by all users) or to `~/bin` (for your personal access). The Python libraries should be copied to a place that can be found in `PYTHONPATH` while the LaTeX style files should be copied to wherever they will be visible to LaTeX (see [this discussion][4] on tex.stackexchange for useful suggestions). If you place the files in non-standard locations you may need to adjust your `PATH`, `PYTHONPATH` and `TEXINPUT` environment variables accordingly.

## Running the examples

If you want to recreate the output for `source/cadabra/example-03` (for example) you should execute the following commands

    $ cd source/cadabra
    $ cdblatex.sh -i example-03

This should generate the `example-03.pdf` file (along with a few other support files). A list of the command line options for `cdblatex.sh` can be found using

    $ cdblatex.sh -h

The command line option `-k` will keep all intermediate files and can be useful when trying to locate errors.

The `cdblatex.sh` script will attempt to open the pdf file. You may need to edit that script to use the correct pdf viewer for your platform.

If you are not using the Hybrid-LaTeX tools then you would type

    $ cd source/cadabra/cdb
    $ cadabra2python example-03.cdb example-03.py
    $ cadabra2 example-03.py

This will produce plain text output.

You could also copy and paste `example-03.cdb` into the Cadabra2 gui.

## Testing

You can check your installation by open running (from the command line)

    $ cd source/cadabra/
    $ make
    $ tests.sh

If all goes well then you should see a few lines like

      diff *.cdbtex
    > diff example-01.cdbtex
    > diff example-02.cdbtex
    > diff example-03.cdbtex
    > diff example-04.cdbtex

There will be more lines (from the other examples). The key thing to observe is that each `diff` command produces no output. There are also some tests that do not use the `diff` command. These tests are run by Cadabra. It reads in the expected results and compares them with the actual results printing out any differences (this allows for non-important differences in expressions to be ignored, for example reordering a sum). The results of those (semantic) tests are recorded in `source/cadabra/tests/json/summary.pdf`.

There are similar tests for the exercises (see `source/cadabra/exercises/`).

## License

All files in this collection are distributed under the [MIT][5] license. See the file LICENSE.txt for the full details.

  [1]: https://cadabra.science
  [2]: https://github.com/leo-brewin/hybrid-latex
  [3]: https://github.com/kpeeters/cadabra2
  [4]: https://tex.stackexchange.com/questions/1137/where-do-i-place-my-own-sty-or-cls-files-to-make-them-available-to-all-my-te
  [5]: https://opensource.org/licenses/MIT
