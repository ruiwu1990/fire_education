# simply run `make` to build the pdf and open it in your favorite viewer
#
# Author: Matthew A. Turner
# Date: 25 Feb 2016

opdf: pdf
	open main.pdf

pdf:
	pandoc -s -S --bibliography vwbib.bib --filter pandoc-citeproc \
		main.md -o main.pdf
