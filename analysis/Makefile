infile = ~/Desktop/report.json

plots: plot1.png plot3.png plot9.png plot2.png plot5.png
	ruby geoip.rb $(infile) > ./geoip.txt
	@echo "Complete"

%.png: %.gpi %.txt
	gnuplot $<

%.txt: %.py
	python $< $(infile) > $@

clean:
	rm -f plot*.txt plot*.png geoip.txt

.PHONY: clean
