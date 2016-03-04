# simply run `make` to build the pdf and open it in your favorite viewer
#
# Author: Matthew A. Turner
# Date: 25 Feb 2016

opdf: pdf
	open main.pdf

pdf:
	pandoc -s --bibliography vwbib.bib -F pandoc-citeproc main.md -o main.tex \
		&& pdflatex -shell-escape main.tex && open main.pdf
