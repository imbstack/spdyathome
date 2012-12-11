infile = ~/Desktop/report.json
sitelist = ../spdyathome/data/sitelist.txt
sitedump = ../spdyathome/data/sitedump.json

plots: plot1.png plot3.png plot9.png plot2.png plot5.png geoip.txt plot6.png plot12.png plot13.png plot8.png plot10.png
	@echo "Complete"

%.png: %.gpi %.txt
	gnuplot $<

%.txt: %.py
	python $< $(infile) > $@

plot8.txt: plot8.py
	python plot8.py $(infile) $(sitelist) $(sitedump) > plot8.txt

plot10.txt: plot10.py
	python plot10.py $(infile) $(sitelist) $(sitedump) > plot10.txt

geoip.txt: geoip.rb
	ruby geoip.rb $(infile) > ./geoip.txt

clean:
	rm -f plot*.txt plot*.png geoip.txt

.PHONY: clean
