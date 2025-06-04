#!/usr/bin/env ruby

log = ARGV[0]
from = log.match(/\[from:(.*?)\]/)[1]
to = log.match(/\[to:(.*?)\]/)[1]
flags = log.match(/\[flags:(.*?)\]/)[1]

puts "#{from},#{to},#{flags}"
