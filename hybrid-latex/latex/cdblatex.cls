\NeedsTeXFormat{LaTeX2e}
\LoadClassWithOptions{article}
%-------------------------------------------------------------------------------
\input{cdblatex.sty}
\usepackage[papersize={297mm,210mm},hmargin=2cm,tmargin=1.0cm,bmargin=1.5cm]{geometry}
\usepackage{hyperref}
%-------------------------------------------------------------------------------
\thispagestyle{empty}
%-------------------------------------------------------------------------------
\parindent=0pt
\parskip=8pt plus 2pt minus 1pt
%-------------------------------------------------------------------------------
\InputIfFileExists{./\jobname.sty}{}{}% over ride defaults, e.g., papersize
%-------------------------------------------------------------------------------
