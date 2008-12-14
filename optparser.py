#!/usr/bin/env python

import optparse

p = optparse.OptionParser()
p.add_option('--filename', '-f', help='the file you want to fuck with')
options, arguments = p.parse_args()
print options.filename