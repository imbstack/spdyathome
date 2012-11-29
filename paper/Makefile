paper.pdf: paper.bbl
	pdflatex paper.tex
	pdflatex paper.tex
	rm -f ../TODO
	date > ../TODO
	grep -n TODO ./*.tex >> ../TODO

paper.dvi:  paper.tex
	latex paper
	bibtex paper
	latex paper
	latex paper

paper.bbl:  paper.dvi
	bibtex paper

clean:  
	rm -f *.aux *.log *.bbl *.blg *.out *.pdf *.dvi *.toc
