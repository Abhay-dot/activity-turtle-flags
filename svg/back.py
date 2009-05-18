#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Copyright (c) 2009, Sugar Labs

#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in
#all copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#THE SOFTWARE.

import sys
import os
import os.path
import gettext

def main():

    myname = "back"
    if len(sys.argv) != 2:
        print "Error: Usage is " + myname + ".py lang"
        return

    t = gettext.translation("org.laptop.TurtleArtActivity", "../locale", languages=[sys.argv[1]])
    _ = t.ugettext
    t.install()

    mystring = _("back")
    mygroup = "turtle"

    print mystring

    data0 = \
"<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?> \n \
<svg \n \
   xmlns=\"http://www.w3.org/2000/svg\" \n \
   xmlns:xlink=\"http://www.w3.org/1999/xlink\" \n \
   width=\"87\" \n \
   height=\"44\"> \n \
  <defs> \n \
    <linearGradient \n \
       id=\"linearGradient3166\"> \n \
      <stop \n \
         style=\"stop-color:#ffffff;stop-opacity:1;\" \n \
         offset=\"0\" \n \
         id=\"stop3168\" /> \n \
      <stop \n \
         style=\"stop-color:#00ff00;stop-opacity:1;\" \n \
         offset=\"1\" \n \
         id=\"stop3170\" /> \n \
    </linearGradient> \n \
    <linearGradient \n \
       xlink:href=\"#linearGradient3166\" \n \
       id=\"linearGradient3172\" \n \
       x1=\"0\" \n \
       y1=\"22\" \n \
       x2=\"74\" \n \
       y2=\"22\" \n \
       gradientUnits=\"userSpaceOnUse\" /> \n \
  </defs> \n \
  <path \n \
     style=\"fill:#00e000;fill-opacity:1;stroke:#008000;stroke-width:1.5;stroke-opacity:1\" \n \
     d=\"M 70,6 L 86.5,6 L 86.5,12 L 82.5,12 L 82.5,9 L 72,9\" /> \n \
  <path \n \
     style=\"fill:#00e000;fill-opacity:1;stroke:#008000;stroke-width:1.5;stroke-opacity:1\" \n \
     d=\"M 70,33.5 L 86.5,33.5 L 86.5,27.5 L 82.5,27.5 L 82.5,30.5 L 72,30.5\" /> \n \
  <path \n \
     style=\"fill:url(#linearGradient3172);fill-opacity:1;stroke:#00a000;stroke-width:2;stroke-opacity:1\" \n \
     d=\"M 48,1 C 64,1 64,1 64,1 C 64,1 68.1,3.5 69.5,5 C 70.9,6.5 73,11 73,11 L 73,30 C 73,30 70.8,33.7 69.5,35 C 68.1,36.5 64,39 64,39 L 47,39 L 47,39 L 47,43 L 27,43 L 27,39 L 10,39 C 10,39 5.9,36.5 4.5,35 C 3.2,33.7 1,30 1,30 L 1,11 C 1,11 3.1,6.5 4.5,5 C 5.9,3.5 10,1 10,1 L 26,1 L 26,6 L 48,6 L 48,1 z\" /> \n \
  <text \n \
     style=\"font-size:12px;text-anchor:middle;text-align:center;font-family:Bitstream Vera Sans\"> \n \
      <tspan \n \
       x=\"37\" \n \
       y=\"26\" \n \
       style=\"font-size:16px;\">"

    data1 = \
"</tspan> \n \
  </text> \n \
</svg> \n "

    FILE = open(os.path.join("../images", sys.argv[1], mygroup, myname + ".svg"), "w")
    FILE.write(data0)
    FILE.write(mystring.encode("utf-8"))
    FILE.write(data1)
    FILE.close()
    return

if __name__ == "__main__":
    main()