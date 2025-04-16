# A tutorial on Cadabra

## Overview

[Cadabra][1] is an open access program ideally suited to complex tensor computations in General Relativity. Tensor expressions are written in LaTeX while an enhanced version of Python is used to control the computations. This tutorial assumes no prior knowledge of Cadabra. It consists of a series of examples covering a range of topics from basic syntax such as declarations, functions, program control, component computations, input and output through to complete computations including a derivation of the BSSN equations from the ADM equations. Numerous exercises are included along with complete solutions.

All of the sources for the tutorial (including the examples and exercises) are written with the Cadabra sources embedded in LaTeX documents. Simple tools are used to extract and execute the embedded Cadabra source while also capturing the output and making it available elsewhere in the LaTeX document. These tools have been cloned from the [Hybrid-LaTeX][2] project and can be found in the `hybrid-latex` directory. A copy of the documentation for the Hybrid-LaTeX project is also included in the `hybrid-latex` directory.

## Documentation

The complete tutorial, examples and solutions to the exercises are provided as pdf files (in the `pdf` firectory) as well as the full LaTeX/Cadabra sources (in `sources/tex`, `sources/cadabra` and  `sources/cadabra/exrecises`).

## Running the examples

All of the scripts for building and excuting the codes depend on a small set of environment variables. These need to be set just once in each session. To do so, just run

```sh
$ source SETUP.txt
```

form the top directory.

To build everything (provided all dependancies are satisfied, see below), just run

```sh
$ make
```

This will run Cadabra and LaTeX on each of the sources in `source/cadabra` and `source/tex`. Some of the Cadabra codes will take a few minutes to run (see `source/cadabra/TIME.txt` for a list of approximate times).

Makefiles are also provided so you can build individual codes, for example `source/cadabra/example-03`, using

```sh
$ cd source/cadabra
$ make example-03
```

You can also compile `source/cadabra/example-03` without using `make` by executing

```sh
$ cd source/cadabra
$ cdblatex.sh -i example-03
```

This should generate the `example-03.pdf` file (along with a few other support files). A list of the command line options for `cdblatex.sh` can be found using

```sh
$ cdblatex.sh -h
```

The command line option `-k` will keep all intermediate files and can be useful when trying to locate errors.

The `cdblatex.sh` script will attempt to open the pdf file. You may need to edit that script to use the correct pdf viewer for your platform.

## Testing

You can check your installation by running

```sh
$ cd source/cadabra/
$ make
$ make tests
```

If all goes well then you should see a few lines like

```sh
> diff example-01.cdbtex
> diff example-02.cdbtex
> diff example-03.cdbtex
> diff example-04.cdbtex
```

There will be more lines (from the other examples). The key thing to observe is that each `diff` command produces no output (apart from a few lines that record execution times as these may vary slightly from one run to the next). There are also some tests that do not use the `diff` command. These tests are run by Cadabra. It reads in the expected results and compares them with the actual results printing out any differences (this allows for non-important differences in expressions to be ignored, for example reordering a sum). The results of those (semantic) tests are recorded in `source/cadabra/tests/semantic/summary.pdf`.

There are similar tests for the exercises (see `source/cadabra/exercises`).

## Dependencies

You will need the Cadabra/Python/SymPy software.

### Cadabra

Ready to run binraries are available for many popular operating systems. These can be found on the [Cadabra binaries][6] page.

Cadabra can also be easily compiled from source. Full details can be found at the [Cadabra repository][3].

### Python/SymPy

Most of the popular operating system have Python3 already installed. You can check your version by running

```sh
$ python --version
```

If that does not report version 3 or later, then you will need to manually install python. Most operating system provide native package managers (HomeBrew on macOs, apt/dnf/yum on Linux) that you can use to do the job. Otherwise, you can install Python3 using [Conda miniforge][4].

You will also need version 1.7 or later of sympy. That may already be part of your python environment. You can check which version you have (if any) by running

```sh
$ pip list | grep sympy
```

You can upgrade sympy to the latest version using

```sh
$ pip install --upgrade sympy
```

If you need to install sympy, then it is best to do so using a python virtual environment. This ensures that you leave the operating system's version of python intact. See the official [Python docs][7] on creating, using and managing virtual environments. Another very useful introduction to virtual environments can be found in this [primer][8].

## Uninstall

To uninstall this project simply delete this directory. This will delete all sources but it will not uninstall Cadabra.

## License

All files in this collection are distributed under the [MIT][5] license. See the file LICENSE.txt for the full details.

  [1]: https://cadabra.science
  [2]: https://github.com/leo-brewin/hybrid-latex
  [3]: https://github.com/kpeeters/cadabra2
  [4]: https://github.com/conda-forge/miniforge
  [5]: https://opensource.org/licenses/MIT
  [6]: https://cadabra.science/download.html
  [7]: https://docs.python.org/3/tutorial/venv.html
  [8]: https://realpython.com/python-virtual-environments-a-primer/