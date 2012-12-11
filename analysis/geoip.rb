require 'geoip'
require 'json'

c = GeoIP.new('GeoLiteCity.dat')
h = Hash.new(0)

File.open(ARGV[0]).each_line do |l|
    blob = JSON.parse(l)
    h[c.city(blob['ip']).city_name] += 1
end

h.sort_by{|k,v| -v}.each do |k,v|
    if k == ''
        k = 'unknown'
    end
    puts "#{k}: #{v}"
end
