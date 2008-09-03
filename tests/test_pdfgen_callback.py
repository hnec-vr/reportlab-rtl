#!/bin/env python
#Copyright ReportLab Europe Ltd. 2000-2004
#see license.txt for license details
#history http://www.reportlab.co.uk/cgi-bin/viewcvs.cgi/public/reportlab/trunk/reportlab/test/test_pdfgen_callback.py
__version__=''' $Id$ '''
__doc__='checks callbacks work'

import unittest
from tests.utils import makeSuiteForClasses, outputfile, printLocation

from reportlab.pdfgen.canvas import Canvas
from tests.test_pdfgen_general import makeDocument

_PAGE_COUNT = 0


class CallBackTestCase(unittest.TestCase):
    "checks it gets called"

    def callMe(self, pageNo):
        self.pageCount = pageNo

    def test0(self):
        "Make a PDFgen document with most graphics features"

        self.pageCount = 0
        makeDocument(outputfile('test_pdfgen_callback.pdf'), pageCallBack=self.callMe)
        #no point saving it!
        assert self.pageCount >= 7, 'page count not called!'


def makeSuite():
    return makeSuiteForClasses(CallBackTestCase)


#noruntests
if __name__ == "__main__":
    unittest.TextTestRunner().run(makeSuite())
    printLocation()
