infile = ~/Desktop/report.json

plots: plot1.png plot3.png plot9.png plot2.png plot5.png geoip.txt plot6.png plot12.png plot13.png
	@echo "Complete"

%.png: %.gpi %.txt
	gnuplot $<

%.txt: %.py
	python $< $(infile) > $@

geoip.txt: geoip.rb
	ruby geoip.rb $(infile) > ./geoip.txt

clean:
	rm -f plot*.txt plot*.png geoip.txt

.PHONY: clean
