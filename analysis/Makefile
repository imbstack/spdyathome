infile = ~/Desktop/report.json

plots: plot1.png plot3.png plot9.png plot2.png
	@echo "Complete"

%.png: %.gpi %.txt
	gnuplot $<

%.txt: %.py
	python $< $(infile) > $@

clean:
	rm -f plot*.txt plot*.png

.PHONY: clean
