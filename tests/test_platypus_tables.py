#!/bin/env python
#Copyright ReportLab Europe Ltd. 2000-2012
#see license.txt for license details
__version__=''' $Id$ '''
__doc__='Test script for reportlab.tables'
from reportlab.lib.testutils import setOutDir,makeSuiteForClasses, outputfile, printLocation
setOutDir(__name__)
import os,unittest
from reportlab.platypus import Spacer, SimpleDocTemplate, Table, TableStyle
from reportlab.platypus.paragraph import Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.lib import colors
from reportlab.graphics.charts.linecharts import HorizontalLineChart
from reportlab.graphics.shapes import Drawing, _DrawingEditorMixin
from reportlab.graphics.charts.barcharts import VerticalBarChart

styleSheet = getSampleStyleSheet()
    
def getTable():
    t = Table((('','North','South','East','West'),
             ('Quarter 1',100,200,300,400),
             ('Quarter 2',100,400,600,800),
             ('Total',300,600,900,'1,200')),
             (72,36,36,36,36),
             (24, 16,16,18)
            )
    return t

def makeStyles():
    styles = []
    for i in range(5):
        styles.append(TableStyle([('ALIGN', (1,1), (-1,-1), 'RIGHT'),
                                  ('ALIGN', (0,0), (-1,0), 'CENTRE'),
                                  ('HREF', (0,0), (0,0), 'www.google.com'),
                                  ]))
    for style in styles[1:]:
        style.add('GRID', (0,0), (-1,-1), 0.25, colors.black)
    for style in styles[2:]:
        style.add('LINEBELOW', (0,0), (-1,0), 2, colors.black)
    for style in styles[3:]:
        style.add('LINEABOVE', (0, -1), (-1,-1), 2, colors.black)
    styles[-1].add('LINEBELOW',(1,-1), (-1, -1), 2, (0.5, 0.5, 0.5))
    return styles

def run():
    doc = SimpleDocTemplate(outputfile('test_platypus_tables.pdf'), pagesize=(8.5*inch, 11*inch), showBoundary=1)
    lst = []
    from reportlab import Version
    styNormal = styleSheet['Normal']
    styBackground = ParagraphStyle('background', parent=styNormal, backColor=colors.pink)
    styH1 = styleSheet['Heading1']
    lst.append(Paragraph("First, a test of how tables align their content...", styH1))
    lst.append(Paragraph("""Generated with version %s""" % Version,
                        styNormal))
    lst.append(Paragraph("""In release 2.3, cells with plain text positioned their
                         text differently to cells with Paragraphs using the
                         same font.  Hopefully now they are back on the same baseline""",
                        styNormal))
    ts1 = TableStyle([
                ('ALIGN', (0,0), (-1,0), 'RIGHT'),
                ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
                ('VALIGN', (0,0), (-1,-1), 'TOP'),
                ('GRID', (0,0), (-1,-1), 0.25, colors.black),
                    ])
    t1 = Table([
        ('plain text','plain text','shortpara','plain text', 'long para'),
        ('Text','more text', Paragraph('Is this para level?', styBackground), 'Back to text', Paragraph('Short para again', styBackground)),
        ('Text',
            'more text',
            Paragraph('Is this level?', styBackground),
            'This is plain\ntext with line breaks\nto compare against\nthe para on right',
            Paragraph('Long paragraph we expect to wrap over several lines accurately', styBackground)),
        
        ])
    t1.setStyle(ts1)
    lst.append(t1)
    lst.append(Spacer(0,10))
    lst.append(Paragraph("Now we make a table with just one cell containing a string...note how the text sits low", styNormal))
    
    tsGrid = TableStyle([
                ('GRID', (0,0), (-1,-1), 0.25, colors.black),
                    ])
    lst.append(Table([['One cell of plain text']], style=tsGrid, colWidths=[200]))
    
    lst.append(Spacer(0,10))
    lst.append(Paragraph("Now we make a table with just one cell containing a para...should be same position.  Note that the overall bounding box is an approximation and lies - it always did.", styNormal))
    lst.append(Table([[Paragraph('One cell containing a paragraph.  &#196;&#201;&#8747;', styBackground)]], style=tsGrid, colWidths=[200]))

    lst.append(Spacer(0,10))
    lst.append(Paragraph("Paragraphs jumped up post 2.1.  Ideally they should align the same.", styNormal))
    
    
    lst.append(Spacer(0,30))
    lst.append(Paragraph("Now for all the tests we had before.  See also the much longer test_platypus_tables_2.pdf, which for reasons unknown was split into a separate file generated by the same script", styNormal))
    
    styles = makeStyles()
    for style in styles:
        t = getTable()
        t.setStyle(style)
##        print '--------------'
##        for rowstyle in t._cellstyles:
##            for s in rowstyle:
##                print s.alignment
        lst.append(t)
        lst.append(Spacer(0,12))
    doc.build(lst)

class TableBarChart(_DrawingEditorMixin,Drawing):
    def __init__(self,width=400,height=200,*args,**kw):
        Drawing.__init__(self,width,height,*args,**kw)
        self.width = 136
        self.height = 140
        self._add(self,VerticalBarChart(),name='chart',validate=None,desc=None)
        self.chart.y = 20
        self.chart.width = self.width - 21
        self.chart.height = self.height - 24
        self.chart.categoryAxis.categoryNames = ['Spring','Summer','Autumn','Winter']
        self.chart.categoryAxis.labels.fontSize = 7

def old_tables_test():
    from reportlab.lib.units import inch, cm
    from reportlab.platypus.flowables import Image, PageBreak, Spacer, XBox
    from reportlab.platypus.paragraph import Paragraph
    from reportlab.platypus.xpreformatted import XPreformatted
    from reportlab.platypus.flowables import Preformatted
    from reportlab.platypus.doctemplate import SimpleDocTemplate
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus.tables import GRID_STYLE, BOX_STYLE, LABELED_GRID_STYLE, COLORED_GRID_STYLE, LIST_STYLE, LongTable
    rowheights = (24, 16, 16, 16, 16)
    rowheights2 = (24, 16, 16, 16, 30)
    colwidths = (50, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32)
    data = (
        ('', 'Jan', 'Feb', 'Mar','Apr','May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'),
        ('Mugs', 0, 4, 17, 3, 21, 47, 12, 33, 2, -2, 44, 89),
        ('T-Shirts', 0, 42, 9, -3, 16, 4, 72, 89, 3, 19, 32, 119),
        ('Key Ring', 0,0,0,0,0,0,1,0,0,0,2,13),
        ('Hats', 893, 912, '1,212', 643, 789, 159, 888, '1,298', 832, 453, '1,344','2,843')
        )
    data2 = (
        ('', 'Jan', 'Feb', 'Mar','Apr','May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'),
        ('Mugs', 0, 4, 17, 3, 21, 47, 12, 33, 2, -2, 44, 89),
        ('T-Shirts', 0, 42, 9, -3, 16, 4, 72, 89, 3, 19, 32, 119),
        ('Key Ring', 0,0,0,0,0,0,1,0,0,0,2,13),
        ('Hats\nLarge', 893, 912, '1,212', 643, 789, 159, 888, '1,298', 832, 453, '1,344','2,843')
        )
    lst = []
    lst.append(Paragraph("Tables", styleSheet['Heading1']))
    lst.append(Paragraph(__doc__, styleSheet['BodyText']))
    lst.append(Paragraph("The Tables (shown in different styles below) were created using the following code:", styleSheet['BodyText']))
    lst.append(Preformatted("""
    colwidths = (50, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32)
    rowheights = (24, 16, 16, 16, 16)
    data = (
        ('', 'Jan', 'Feb', 'Mar','Apr','May', 'Jun',
           'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'),
        ('Mugs', 0, 4, 17, 3, 21, 47, 12, 33, 2, -2, 44, 89),
        ('T-Shirts', 0, 42, 9, -3, 16, 4, 72, 89, 3, 19, 32, 119),
        ('Key Ring', 0,0,0,0,0,0,1,0,0,0,2,13),
        ('Hats', 893, 912, '1,212', 643, 789, 159,
             888, '1,298', 832, 453, '1,344','2,843')
        )
    t = Table(data, colwidths, rowheights)
    """, styleSheet['Code'], dedent=4))
    lst.append(Paragraph("""
    You can then give the Table a TableStyle object to control its format. The first TableStyle used was
    created as follows:
    """, styleSheet['BodyText']))
    lst.append(Preformatted("""
GRID_STYLE = TableStyle(
    [('GRID', (0,0), (-1,-1), 0.25, colors.black),
     ('ALIGN', (1,1), (-1,-1), 'RIGHT')]
    )
    """, styleSheet['Code']))
    lst.append(Paragraph("""
    TableStyles are created by passing in a list of commands. There are two types of commands - line commands
    and cell formatting commands. In all cases, the first three elements of a command are the command name,
    the starting cell and the ending cell.
    """, styleSheet['BodyText']))
    lst.append(Paragraph("""
    Line commands always follow this with the weight and color of the desired lines. Colors can be names,
    or they can be specified as a (R,G,B) tuple, where R, G and B are floats and (0,0,0) is black. The line
    command names are: GRID, BOX, OUTLINE, INNERGRID, LINEBELOW, LINEABOVE, LINEBEFORE
    and LINEAFTER. BOX and OUTLINE are equivalent, and GRID is the equivalent of applying both BOX and
    INNERGRID.
    """, styleSheet['BodyText']))
    lst.append(Paragraph("""
    Cell formatting commands are:
    """, styleSheet['BodyText']))
    lst.append(Paragraph("""
    FONT - takes fontname, fontsize and (optional) leading.
    """, styleSheet['Definition']))
    lst.append(Paragraph("""
    TEXTCOLOR - takes a color name or (R,G,B) tuple.
    """, styleSheet['Definition']))
    lst.append(Paragraph("""
    ALIGNMENT (or ALIGN) - takes one of LEFT, RIGHT, CENTRE (or CENTER) or DECIMAL.
    """, styleSheet['Definition']))
    lst.append(Paragraph("""
    LEFTPADDING - defaults to 6.
    """, styleSheet['Definition']))
    lst.append(Paragraph("""
    RIGHTPADDING - defaults to 6.
    """, styleSheet['Definition']))
    lst.append(Paragraph("""
    BOTTOMPADDING - defaults to 3.
    """, styleSheet['Definition']))
    lst.append(Paragraph("""
    A tablestyle is applied to a table by calling Table.setStyle(tablestyle).
    """, styleSheet['BodyText']))
    t = Table(data, colwidths, rowheights)
    t.setStyle(GRID_STYLE)
    lst.append(PageBreak())
    lst.append(Paragraph("This is GRID_STYLE\n", styleSheet['BodyText']))
    lst.append(t)

    t = Table(data, colwidths, rowheights)
    t.setStyle(BOX_STYLE)
    lst.append(Paragraph("This is BOX_STYLE\n", styleSheet['BodyText']))
    lst.append(t)
    lst.append(Paragraph("""
    It was created as follows:
    """, styleSheet['BodyText']))
    lst.append(Preformatted("""
BOX_STYLE = TableStyle(
    [('BOX', (0,0), (-1,-1), 0.50, colors.black),
     ('ALIGN', (1,1), (-1,-1), 'RIGHT')]
    )
    """, styleSheet['Code']))

    t = Table(data, colwidths, rowheights)
    t.setStyle(LABELED_GRID_STYLE)
    lst.append(Paragraph("This is LABELED_GRID_STYLE\n", styleSheet['BodyText']))
    lst.append(t)
    t = Table(data2, colwidths, rowheights2)
    t.setStyle(LABELED_GRID_STYLE)
    lst.append(Paragraph("This is LABELED_GRID_STYLE ILLUSTRATES EXPLICIT LINE SPLITTING WITH NEWLINE (different heights and data)\n", styleSheet['BodyText']))
    lst.append(t)
    lst.append(Paragraph("""
    It was created as follows:
    """, styleSheet['BodyText']))
    lst.append(Preformatted("""
LABELED_GRID_STYLE = TableStyle(
    [('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
     ('BOX', (0,0), (-1,-1), 2, colors.black),
     ('LINEBELOW', (0,0), (-1,0), 2, colors.black),
     ('LINEAFTER', (0,0), (0,-1), 2, colors.black),
     ('ALIGN', (1,1), (-1,-1), 'RIGHT')]
    )
    """, styleSheet['Code']))
    lst.append(PageBreak())

    t = Table(data, colwidths, rowheights)
    t.setStyle(COLORED_GRID_STYLE)
    lst.append(Paragraph("This is COLORED_GRID_STYLE\n", styleSheet['BodyText']))
    lst.append(t)
    lst.append(Paragraph("""
    It was created as follows:
    """, styleSheet['BodyText']))
    lst.append(Preformatted("""
COLORED_GRID_STYLE = TableStyle(
    [('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
     ('BOX', (0,0), (-1,-1), 2, colors.red),
     ('LINEBELOW', (0,0), (-1,0), 2, colors.black),
     ('LINEAFTER', (0,0), (0,-1), 2, colors.black),
     ('ALIGN', (1,1), (-1,-1), 'RIGHT')]
    )
    """, styleSheet['Code']))

    t = Table(data, colwidths, rowheights)
    t.setStyle(LIST_STYLE)
    lst.append(Paragraph("This is LIST_STYLE\n", styleSheet['BodyText']))
    lst.append(t)
    lst.append(Paragraph("""
    It was created as follows:
    """, styleSheet['BodyText']))
    lst.append(Preformatted("""
LIST_STYLE = TableStyle(
    [('LINEABOVE', (0,0), (-1,0), 2, colors.green),
     ('LINEABOVE', (0,1), (-1,-1), 0.25, colors.black),
     ('LINEBELOW', (0,-1), (-1,-1), 2, colors.green),
     ('ALIGN', (1,1), (-1,-1), 'RIGHT')]
    )
    """, styleSheet['Code']))

    t = Table(data, colwidths, rowheights)
    ts = TableStyle(
    [('LINEABOVE', (0,0), (-1,0), 2, colors.green),
     ('LINEABOVE', (0,1), (-1,-1), 0.25, colors.black),
     ('LINEBELOW', (0,-1), (-1,-1), 3, colors.green,'butt'),
     ('LINEBELOW', (0,-1), (-1,-1), 1, colors.white,'butt'),
     ('ALIGN', (1,1), (-1,-1), 'RIGHT'),
     ('TEXTCOLOR', (0,1), (0,-1), colors.red),
     ('BACKGROUND', (0,0), (-1,0), colors.Color(0,0.7,0.7))]
    )
    t.setStyle(ts)
    lst.append(Paragraph("This is a custom style\n", styleSheet['BodyText']))
    lst.append(t)
    lst.append(Paragraph("""
    It was created as follows:
    """, styleSheet['BodyText']))
    lst.append(Preformatted("""
   ts = TableStyle(
    [('LINEABOVE', (0,0), (-1,0), 2, colors.green),
     ('LINEABOVE', (0,1), (-1,-1), 0.25, colors.black),
     ('LINEBELOW', (0,-1), (-1,-1), 3, colors.green,'butt'),
     ('LINEBELOW', (0,-1), (-1,-1), 1, colors.white,'butt'),
     ('ALIGN', (1,1), (-1,-1), 'RIGHT'),
     ('TEXTCOLOR', (0,1), (0,-1), colors.red),
     ('BACKGROUND', (0,0), (-1,0), colors.Color(0,0.7,0.7))]
    )
    """, styleSheet['Code']))
    data = (
        ('', 'Jan\nCold', 'Feb\n', 'Mar\n','Apr\n','May\n', 'Jun\nHot', 'Jul\n', 'Aug\nThunder', 'Sep\n', 'Oct\n', 'Nov\n', 'Dec\n'),
        ('Mugs', 0, 4, 17, 3, 21, 47, 12, 33, 2, -2, 44, 89),
        ('T-Shirts', 0, 42, 9, -3, 16, 4, 72, 89, 3, 19, 32, 119),
        ('Key Ring', 0,0,0,0,0,0,1,0,0,0,2,13),
        ('Hats', 893, 912, '1,212', 643, 789, 159, 888, '1,298', 832, 453, '1,344','2,843')
        )
    c = list(colwidths)
    c[0] = None
    c[8] = None
    t = Table(data, c, [None]+list(rowheights[1:]))
    t.setStyle(LIST_STYLE)
    lst.append(Paragraph("""
        This is a LIST_STYLE table with the first rowheight set to None ie automatic.
        The top row cells are split at a newline '\\n' character. The first and August
        column widths were also set to None.
    """, styleSheet['BodyText']))
    lst.append(t)

    lst.append(Paragraph("""
        This demonstrates a number of features useful in financial statements. The first is decimal alignment;
        with ALIGN=DECIMAL the numbers align on the points; and the points are aligned based on
        the RIGHTPADDING, which is usually 3 points so you should set it higher.  The second is multiple lines;
        one can specify double or triple lines and control the separation if desired. Finally, the coloured
        negative numbers were (we regret to say) done in the style; we don't have a way to conditionally
        format numbers based on value yet.
    """, styleSheet['BodyText']))


    t = Table([[u'Corporate Assets','Amount'],
               ['Fixed Assets','1,234,567.89'],
               ['Company Vehicle','1,234.8901'],
               ['Petty Cash','42'],
               [u'Intellectual Property\u00ae','(42,078,231.56)'],
               ['Overdraft','(12,345)'],
               ['Boardroom Flat Screen','60 inches'],
               ['Net Position','Deep Sh*t.Really']
               ],
              [144,72])

    ts = TableStyle(
        [#first the top row
         ('ALIGN', (1,1), (-1,-1), 'CENTER'),
         ('LINEABOVE', (0,0), (-1,0), 1, colors.purple),
         ('LINEBELOW', (0,0), (-1,0), 1, colors.purple),
         ('FONT', (0,0), (-1,0), 'Times-Bold'),

        #bottom row has a line above, and two lines below
         ('LINEABOVE', (0,-1), (-1,-1), 1, colors.purple),  #last 2 are count, sep
         ('LINEBELOW', (0,-1), (-1,-1), 0.5, colors.purple, 1, None, None, 4,1),
         ('LINEBELOW', (0,-1), (-1,-1), 1, colors.red),
         ('FONT', (0,-1), (-1,-1), 'Times-Bold'),

        #numbers column
         ('ALIGN', (1,1), (-1,-1), 'DECIMAL'),
         ('RIGHTPADDING', (1,1), (-1,-1), 36),
         ('TEXTCOLOR', (1,4), (1,4), colors.red),

        #red cell         
        ]
        )

    t.setStyle(ts)
    lst.append(t)
    lst.append(Spacer(36,36))    
    lst.append(Paragraph("""
        The red numbers should be aligned LEFT &amp; BOTTOM, the blue RIGHT &amp; TOP
        and the green CENTER &amp; MIDDLE.
    """, styleSheet['BodyText']))
    XY  =   [['X00y', 'X01y', 'X02y', 'X03y', 'X04y'],
            ['X10y', 'X11y', 'X12y', 'X13y', 'X14y'],
            ['X20y', 'X21y', 'X22y', 'X23y', 'X24y'],
            ['X30y', 'X31y', 'X32y', 'X33y', 'X34y']]
    t=Table(XY, 5*[0.6*inch], 4*[0.6*inch])
    t.setStyle([('ALIGN',(1,1),(-2,-2),'LEFT'),
                ('TEXTCOLOR',(1,1),(-2,-2),colors.red),

                ('VALIGN',(0,0),(1,-1),'TOP'),
                ('ALIGN',(0,0),(1,-1),'RIGHT'),
                ('TEXTCOLOR',(0,0),(1,-1),colors.blue),

                ('ALIGN',(0,-1),(-1,-1),'CENTER'),
                ('VALIGN',(0,-1),(-1,-1),'MIDDLE'),
                ('TEXTCOLOR',(0,-1),(-1,-1),colors.green),
                ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                ])
    lst.append(t)
    data = [('alignment', 'align\012alignment'),
            ('bulletColor', 'bulletcolor\012bcolor'),
            ('bulletFontName', 'bfont\012bulletfontname'),
            ('bulletFontSize', 'bfontsize\012bulletfontsize'),
            ('bulletIndent', 'bindent\012bulletindent'),
            ('firstLineIndent', 'findent\012firstlineindent'),
            ('fontName', 'face\012fontname\012font'),
            ('fontSize', 'size\012fontsize'),
            ('leading', 'leading'),
            ('leftIndent', 'leftindent\012lindent'),
            ('rightIndent', 'rightindent\012rindent'),
            ('spaceAfter', 'spaceafter\012spacea'),
            ('spaceBefore', 'spacebefore\012spaceb'),
            ('textColor', 'fg\012textcolor\012color')]
    t = Table(data)
    t.setStyle([
            ('VALIGN',(0,0),(-1,-1),'TOP'),
            ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
            ('BOX', (0,0), (-1,-1), 0.25, colors.black),
            ])
    lst.append(t)
    t = Table([ ('Attribute', 'Synonyms'),
                ('alignment', 'align, alignment'),
                ('bulletColor', 'bulletcolor, bcolor'),
                ('bulletFontName', 'bfont, bulletfontname'),
                ('bulletFontSize', 'bfontsize, bulletfontsize'),
                ('bulletIndent', 'bindent, bulletindent'),
                ('firstLineIndent', 'findent, firstlineindent'),
                ('fontName', 'face, fontname, font'),
                ('fontSize', 'size, fontsize'),
                ('leading', 'leading'),
                ('leftIndent', 'leftindent, lindent'),
                ('rightIndent', 'rightindent, rindent'),
                ('spaceAfter', 'spaceafter, spacea'),
                ('spaceBefore', 'spacebefore, spaceb'),
                ('textColor', 'fg, textcolor, color')])
    t.repeatRows = 1
    t.setStyle([
                ('FONT',(0,0),(-1,1),'Times-Bold',10,12),
                ('FONT',(0,1),(-1,-1),'Courier',8,8),
                ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
                ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                ('BACKGROUND', (0, 0), (-1, 0), colors.green),
                ('BACKGROUND', (0, 1), (-1, -1), colors.pink),
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                ('ALIGN', (0, 1), (0, -1), 'LEFT'),
                ('ALIGN', (-1, 1), (-1, -1), 'RIGHT'),
                ('FONT', (0, 0), (-1, 0), 'Times-Bold', 12),
                ('ALIGN', (1, 1), (1, -1), 'CENTER'),
                ])
    lst.append(t)
    lst.append(Table(XY,
            style=[ ('FONT',(0,0),(-1,-1),'Times-Roman', 5,6),
                    ('GRID', (0,0), (-1,-1), 0.25, colors.blue),]))
    lst.append(Table(XY,
            style=[ ('FONT',(0,0),(-1,-1),'Times-Roman', 10,12),
                    ('GRID', (0,0), (-1,-1), 0.25, colors.black),]))
    lst.append(Table(XY,
            style=[ ('FONT',(0,0),(-1,-1),'Times-Roman', 20,24),
                    ('GRID', (0,0), (-1,-1), 0.25, colors.red),]))
    lst.append(PageBreak())
    data=  [['00', '01', '02', '03', '04'],
            ['10', '11', '12', '13', '14'],
            ['20', '21', '22', '23', '24'],
            ['30', '31', '32', '33', '34']]
    t=Table(data,style=[
                    ('GRID',(0,0),(-1,-1),0.5,colors.grey),
                    ('GRID',(1,1),(-2,-2),1,colors.green),
                    ('BOX',(0,0),(1,-1),2,colors.red),
                    ('BOX',(0,0),(-1,-1),2,colors.black),
                    ('LINEABOVE',(1,2),(-2,2),1,colors.blue),
                    ('LINEBEFORE',(2,1),(2,-2),1,colors.pink),
                    ('BACKGROUND', (0, 0), (0, 1), colors.pink),
                    ('BACKGROUND', (1, 1), (1, 2), colors.lavender),
                    ('BACKGROUND', (2, 2), (2, 3), colors.orange),
                    ])
    lst.append(Paragraph("Illustrating splits: nosplit", styleSheet['BodyText']))
    lst.append(t)
    lst.append(Spacer(0,6))
    lst.append(Paragraph("Illustrating splits: split(4in,30)", styleSheet['BodyText']))
    for s in t.split(4*inch,30):
        lst.append(s)
        lst.append(Spacer(0,6))
    lst.append(Spacer(0,6))
    lst.append(Paragraph("Illustrating splits: split(4in,36)", styleSheet['BodyText']))
    for s in t.split(4*inch,36):
        lst.append(s)
        lst.append(Spacer(0,6))
    lst.append(Paragraph("Illustrating splits: split(4in,56)", styleSheet['BodyText']))
    lst.append(Spacer(0,6))
    for s in t.split(4*inch,56):
        lst.append(s)
        lst.append(Spacer(0,6))

    lst.append(PageBreak())
    data=  [['00', '01', '02', '03', '04'],
            ['', '11', '12', '13', '14'],
            ['20', '21', '22', '23', '24'],
            ['30', '31', '', '33', '34']]
    sty=[
                    ('GRID',(0,0),(-1,-1),0.5,colors.grey),
                    ('GRID',(1,1),(-2,-2),1,colors.green),
                    ('BOX',(0,0),(1,-1),2,colors.red),
                    ('BOX',(0,0),(-1,-1),2,colors.black),
                    ('LINEABOVE',(1,2),(-2,2),1,colors.blue),
                    ('LINEBEFORE',(2,1),(2,-2),1,colors.pink),
                    ('BACKGROUND', (0, 0), (0, 1), colors.pink),
                    ('SPAN',(0,0),(0,1)),
                    ('BACKGROUND', (2, 2), (2, 3), colors.orange),
                    ('SPAN',(2,2),(2,3)),
                    ]
    t=Table(data,style=sty)
    lst.append(Paragraph("Illustrating splits with spans: nosplit", styleSheet['BodyText']))
    lst.append(t)
    lst.append(Spacer(0,6))
    lst.append(Paragraph("Illustrating splits with spans: split(4in,30)", styleSheet['BodyText']))
    for s in t.split(4*inch,30):
        lst.append(s)
        lst.append(Spacer(0,6))
    lst.append(Spacer(0,6))
    lst.append(Paragraph("Illustrating splits with spans: split(4in,36)", styleSheet['BodyText']))
    for s in t.split(4*inch,36):
        lst.append(s)
        lst.append(Spacer(0,6))
    lst.append(Paragraph("Illustrating splits with spans: split(4in,56)", styleSheet['BodyText']))
    lst.append(Spacer(0,6))
    for s in t.split(4*inch,56):
        lst.append(s)
        lst.append(Spacer(0,6))

    data=  [['00', '01', '02', '03', '04'],
            ['', '11', '12', '13', ''],
            ['20', '21', '22', '23', '24'],
            ['30', '31', '', '33', ''],
            ['40', '41', '', '43', '44']]
    sty=[
        ('GRID',(0,0),(-1,-1),0.5,colors.grey),
        ('GRID',(1,1),(-2,-2),1,colors.green),
        ('BOX',(0,0),(1,-1),2,colors.red),
        ('BOX',(0,0),(-1,-1),2,colors.black),
        ('LINEABOVE',(1,2),(-2,2),1,colors.blue),
        ('LINEBEFORE',(2,1),(2,-2),1,colors.pink),
        ('BACKGROUND', (0, 0), (0, 1), colors.pink),
        ('SPAN',(0,0),(0,1)),
        ('BACKGROUND',(-2,1),(-1,1),colors.palegreen),
        ('SPAN',(-2,1),(-1,1)),
        ('BACKGROUND',(-2,3),(-1,3),colors.yellow),
        ('SPAN',(-2,3),(-1,3)),
        ('BACKGROUND', (2, 3), (2, 4), colors.orange),
        ('SPAN',(2,3),(2,4)),
        ]

    t=Table(data,style=sty,repeatRows=2)
    lst.append(Paragraph("Illustrating splits with spans and repeatRows: nosplit", styleSheet['BodyText']))
    lst.append(t)
    lst.append(Spacer(0,6))
    if  1:
        lst.append(Paragraph("Illustrating splits with spans and repeatRows: split(4in,30)", styleSheet['BodyText']))
        for s in t.split(4*inch,30):
            lst.append(s)
            lst.append(Spacer(0,6))
        lst.append(Spacer(0,6))
        lst.append(Paragraph("Illustrating splits with spans and repeatRows: split(4in,36)", styleSheet['BodyText']))
        for s in t.split(4*inch,36):
            lst.append(s)
            lst.append(Spacer(0,6))
    lst.append(Paragraph("Illustrating splits with spans and repeatRows: split(4in,56)", styleSheet['BodyText']))
    lst.append(Spacer(0,6))
    for s in t.split(4*inch,56):
        lst.append(s)
        lst.append(Spacer(0,6))

    lst.append(PageBreak())
    from reportlab.lib.testutils import testsFolder
    I = Image(os.path.join(os.path.dirname(testsFolder),'tools','pythonpoint','demos','leftlogo.gif'))
    I.drawHeight = 1.25*inch*I.drawHeight / I.drawWidth
    I.drawWidth = 1.25*inch
    #I.drawWidth = 9.25*inch #uncomment to see better messaging
    P = Paragraph("<para align=center spaceb=3>The <b>ReportLab Left <font color=red>Logo</font></b> Image</para>", styleSheet["BodyText"])
    B = TableBarChart()
    BP = Paragraph("<para align=center spaceb=3>A bar chart in a cell.</para>", styleSheet["BodyText"])

    data=  [['A', 'B', 'C', Paragraph("<b>A pa<font color=red>r</font>a<i>graph</i></b><super><font color=yellow>1</font></super>",styleSheet["BodyText"]), 'D'],
            ['00', '01', '02', [I,P], '04'],
            ['10', '11', '12', [I,P], '14'],
            ['20', '21', '22', '23', '24'],
            ['30', '31', '32', '33', '34'],
            ['40', '41', '42', [B,BP], '44']]

    t=Table(data,style=[('GRID',(1,1),(-2,-2),1,colors.green),
                    ('BOX',(0,0),(1,-1),2,colors.red),
                    ('LINEABOVE',(1,2),(-2,2),1,colors.blue),
                    ('LINEBEFORE',(2,1),(2,-2),1,colors.pink),
                    ('BACKGROUND', (0, 0), (0, 1), colors.pink),
                    ('BACKGROUND', (1, 1), (1, 2), colors.lavender),
                    ('BACKGROUND', (2, 2), (2, 3), colors.orange),
                    ('BOX',(0,0),(-1,-1),2,colors.black),
                    ('GRID',(0,0),(-1,-1),0.5,colors.black),
                    ('VALIGN',(3,0),(3,0),'BOTTOM'),
                    ('BACKGROUND',(3,0),(3,0),colors.limegreen),
                    ('BACKGROUND',(3,1),(3,1),colors.khaki),
                    ('ALIGN',(3,1),(3,1),'CENTER'),
                    ('BACKGROUND',(3,2),(3,2),colors.beige),
                    ('ALIGN',(3,2),(3,2),'LEFT'),
                    ])

    t._argW[3]=1.5*inch
    lst.append(t)

    # now for an attempt at column spanning.
    lst.append(PageBreak())
    data=  [['A', 'BBBBB', 'C', 'D', 'E'],
            ['00', '01', '02', '03', '04'],
            ['10', '11', '12', '13', '14'],
            ['20', '21', '22', '23', '24'],
            ['30', '31', '32', '33', '34']]
    sty = [
            ('ALIGN',(0,0),(-1,-1),'CENTER'),
            ('VALIGN',(0,0),(-1,-1),'TOP'),
            ('GRID',(0,0),(-1,-1),1,colors.green),
            ('BOX',(0,0),(-1,-1),2,colors.red),

            #span 'BBBB' across middle 3 cells in top row
            ('SPAN',(1,0),(3,0)),
            #now color the first cell in this range only,
            #i.e. the one we want to have spanned.  Hopefuly
            #the range of 3 will come out khaki.
            ('BACKGROUND',(1,0),(1,0),colors.khaki),

            ('SPAN',(0,2),(-1,2)),


            #span 'AAA'down entire left column
            ('SPAN',(0,0), (0, 1)),
            ('BACKGROUND',(0,0),(0,0),colors.cyan),
            ('LINEBELOW', (0,'splitlast'), (-1,'splitlast'), 1, colors.white,'butt'),
           ]
    t=Table(data,style=sty, colWidths = [20] * 5, rowHeights = [20]*5)
    lst.append(t)

    # now for an attempt at percentage widths
    lst.append(Spacer(18,18))
    lst.append(Paragraph("This table has colWidths=5*['14%']!", styleSheet['BodyText']))
    t=Table(data,style=sty, colWidths = ['14%'] * 5, rowHeights = [20]*5)
    lst.append(t)

    lst.append(Spacer(18,18))
    lst.append(Paragraph("This table has colWidths=['14%','10%','19%','22%','*']!", styleSheet['BodyText']))
    t=Table(data,style=sty, colWidths = ['14%','10%','19%','22%','*'], rowHeights = [20]*5)
    lst.append(t)

    # Mike's test example
    lst.append(Spacer(18,18))
    lst.append(Paragraph('Mike\'s Spanning Example', styleSheet['Heading1']))
    data=  [[Paragraph('World Domination: The First Five Years', styleSheet['BodyText']), ''],
            [Paragraph('World <font color="green">Domination</font>: The First Five Years', styleSheet['BodyText']),''],
            [Paragraph('World Domination: The First Five Years', styleSheet['BodyText']), ''],
            ]
    t=Table(data, style=[('SPAN',(0,0),(1,0)),('SPAN',(0,1),(1,1)),('SPAN',(0,2),(1,2)),], colWidths = [3*cm,8*cm], rowHeights = [None]*3)
    lst.append(t)

    lst.append(Spacer(18,18))
    lst.append(Paragraph('Mike\'s Non-spanning Example', styleSheet['Heading1']))
    data=  [[Paragraph('World Domination: The First Five Years', styleSheet['BodyText'])],
            [Paragraph('World <font color="magenta">Domination</font>: The First Five Years', styleSheet['BodyText'])],
            [Paragraph('World Domination: The First Five Years', styleSheet['BodyText'])],
            ]
    t=Table(data, style=[], colWidths = [11*cm], rowHeights = [None]*3)
    lst.append(t)

    lst.append(Spacer(18,18))
    lst.append(Paragraph('xpre example', styleSheet['Heading1']))
    data=  [    [
                XPreformatted('Account Details', styleSheet['Heading3']),
                '', XPreformatted('Client Details', styleSheet['Heading3']),
                ],  #end of row 0
            ]
    t=Table(data, style=[], colWidths = [80,230.0,80], rowHeights = [None]*1)
    lst.append(t)

    lst.append(PageBreak())

    lst.append(Paragraph('Trying colour cycling in background', styleSheet['Heading1']))
    lst.append(Paragraph("This should alternate pale blue and uncolored by row", styleSheet['BodyText']))
    data=  [['001', '01', '02', '03', '04', '05'],
            ['002', '01', '02', '03', '04', '05'],
            ['003', '01', '02', '03', '04', '05'],
            ['004', '01', '02', '03', '04', '05'],
            ['005', '01', '02', '03', '04', '05'],
            ['006', '01', '02', '03', '04', '05'],
            ['007', '01', '02', '03', '04', '05'],
            ['008', '01', '02', '03', '04', '05'],
            ['009', '01', '02', '03', '04', '05'],
            ['010', '01', '02', '03', '04', '05'],

            ]
    t=Table(data,style=[
                    ('GRID',(0,0),(-1,-1),0.5,colors.grey),
                    ('ROWBACKGROUNDS', (0, 0), (-1, -1), (0xD0D0FF, None)),
                    ])
    lst.append(t)
    lst.append(Spacer(0,6))
    lst.append(Paragraph("And this should pale blue, pale pink and None by column", styleSheet['BodyText']))
    data=  [['001', '01', '02', '03', '04', '05'],
            ['002', '01', '02', '03', '04', '05'],
            ['003', '01', '02', '03', '04', '05'],
            ['004', '01', '02', '03', '04', '05'],
            ['005', '01', '02', '03', '04', '05'],
            ['006', '01', '02', '03', '04', '05'],
            ['007', '01', '02', '03', '04', '05'],
            ['008', '01', '02', '03', '04', '05'],
            ['009', '01', '02', '03', '04', '05'],
            ['010', '01', '02', '03', '04', '05'],

            ]
    t=Table(data,style=[
                    ('GRID',(0,0),(-1,-1),0.5,colors.grey),
                    ('COLBACKGROUNDS', (0, 0), (-1, -1), (0xD0D0FF, 0xFFD0D0, None)),
                    ])
    lst.append(t)

    lst.append(PageBreak())
    lst.append(Paragraph("This spanning example illustrates automatic removal of grids and lines in spanned cells!", styleSheet['BodyText']))
    lst.append(Spacer(0,6))
    data=  [['Top\nLeft', '', '02', '03', '04', '05', '06', '07'],
            ['', '', '12', 'Span (3,1) (6,2)', '','','','17'],
            ['20', '21', '22', '', '','','','27'],
            ['30', '31', '32', '33', '34','35','36','37'],
            ['40', 'In The\nMiddle', '', '', '44','45','46','47'],
            ['50', '', '', '', '54','55','56','57'],
            ['60', '', '', '','64', '65', 'Bottom\nRight', ''],
            ['70', '71', '72', '73','74', '75', '', '']]
    t=Table(data,style=[
            ('GRID',(0,0),(-1,-1),0.5,colors.grey),
            ('BACKGROUND',(0,0),(1,1),colors.palegreen),
            ('SPAN',(0,0),(1,1)),
            ('BACKGROUND',(-2,-2),(-1,-1), colors.pink),
            ('SPAN',(-2,-2),(-1,-1)),
            ('SPAN',(1,4),(3,6)),
            ('BACKGROUND',(1,4),(3,6), colors.lightblue),
            ('SPAN',(3,1),(6,2)),
            ('BACKGROUND',(3,1),(6,2), colors.peachpuff),
            ('VALIGN',(3,1),(6,2),'TOP'),
            ('LINEABOVE', (0,2),(-1,2), 1, colors.black, 0, None, None, 2, 2),
            ('LINEBEFORE', (3,0),(3,-1), 1, colors.black, 0, None, None, 2, 2),
            ])
    lst.append(t)

    lst.append(PageBreak())

    lst.append(Paragraph("und jetzt noch eine Tabelle mit 5000 Zeilen:", styleSheet['BodyText']))
    sty = [ ('GRID',(0,0),(-1,-1),1,colors.green),
            ('BOX',(0,0),(-1,-1),2,colors.red),
           ]
    data = [[str(i), Paragraph("xx "* (i%10), styleSheet["BodyText"]), Paragraph("blah "*(i%40), styleSheet["BodyText"])] for i in xrange(500)]
    t=LongTable(data, style=sty, colWidths = [50,100,200])
    lst.append(t)

    #Yuan Hong's bug tester
    lst.append(PageBreak())
    lst.append(Paragraph('Yian Hong\'s Bug Case (should not blow up)', styleSheet['Heading2']))
    data = ([['Col1', 'Col2', 'Col3', 'Col4', 'Col5']]+
                [['01', Paragraph('This is cell one that contains a paragraph.', styleSheet['Normal']), '02', '03', '04']
                    for i in xrange(50)])

    t = Table(data, ['20%']*5, repeatRows=1)
    t.setStyle(TableStyle([
        ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
        ('BOX', (0,0), (-1,-1), 0.25, colors.black),
        ('SPAN', (0,50), (-2,50)),
        ]))

    lst.append(t)
    lst.append(PageBreak())

    #Volker Haas' example extended
    #the optimal row heights are the solution of an LP similar to
    #
    #Objective function
    #   min: 3*h0+3*h1+3*h2+2*h3;
    #
    #constraints
    #   h0>=12;
    #   h1>=12;
    #   h2>=12;
    #   h3>=12;
    #   h0+h1+h2>=48;
    #   h0+h1>=12;
    #   h2+h3>=60;
    #
    #the solution H=[12,12,24,36]
    def makeTable(x,y):
        return Table([
                ['00', '01', '02', '03', '04', '05\nline2\nline3\nline4'],
                ['', '11', '12', x, '',''],
                ['20', '21', y, '23', '24',''],
                ['30', '31', '', '33', '34','35'],
                ],
                style=[
                    ('TOPPADDING',(0,0),(-1,-1),0),
                    ('BOTTOMPADDING',(0,0),(-1,-1),0),
                    ('RIGHTPADDING',(0,0),(-1,-1),0),
                    ('LEFTPADDING',(0,0),(-1,-1),0),
                    ('GRID',(0,0),(-1,-1),0.5,colors.grey),
                    ('BACKGROUND', (0, 0), (0, 1), colors.pink),
                    ('SPAN',(0,0),(0,1)),
                    ('BACKGROUND', (2, 2), (2, 3), colors.orange),
                    ('SPAN',(2,2),(2,3)),
                    ('SPAN',(3,1),(4,1)),
                    ('SPAN',(5,0),(5,2)),
                ])
    p_style= ParagraphStyle('Normal')
    lst.append(makeTable(
            Paragraph('This is a string',p_style),
            Paragraph('22<br/>blub<br/>asfd<br/>afd<br/>asdfs', p_style)
            ))

    lst.append(Spacer(10,10))
    lst.append(makeTable(
            XPreformatted('This is a string',p_style),
            Paragraph('22<br/>blub<br/>asfd<br/>afd<br/>asdfs', p_style)
            ))
    lst.append(Spacer(10,10))
    lst.append(makeTable(
            'This is a string',
            '22\nblub\nasfd\nafd\nasdfs',
            ))
    lst.append(Spacer(10,10))
    lst.append(makeTable(
            'This is a string',
            Paragraph('22<br/>blub<br/>asfd<br/>afd<br/>asdfs', p_style)
            ))
    SimpleDocTemplate(outputfile('test_platypus_tables_2.pdf'), showBoundary=1).build(lst)

class TablesTestCase(unittest.TestCase):
    "Make documents with tables"

    def test0(self):
        "Make a document full of tables"
        run()

    def test1(self):
        "Make a document full of tables"
        old_tables_test()


def makeSuite():
    return makeSuiteForClasses(TablesTestCase)


#noruntests
if __name__ == "__main__":
    unittest.TextTestRunner().run(makeSuite())
    printLocation()
