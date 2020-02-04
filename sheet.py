from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4, inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus.flowables import PageBreak, Spacer
from reportlab.lib.units import mm
from reportlab.graphics import renderPDF, renderPM
from svglib.svglib import svg2rlg
from lxml import etree
import os


class SheetExport():

    def export_sheet(self, filename, data):
        styleSheet = getSampleStyleSheet()
        doc = SimpleDocTemplate(filename, pagesize=A4)
        elements = []

        pdfmetrics.registerFont(TTFont('Arial', 'arial.ttf'))

        elements.append(Paragraph("Skeleton form - adult inventory",
                                  styleSheet['Title']))
        elements.append(Spacer(0, 10 * mm))

        p_site = Paragraph('''<b>SITE</b>''', styleSheet["BodyText"])
        p_location = Paragraph('''<b>LOCATION</b>''', styleSheet["BodyText"])
        p_skeleton = Paragraph('''<b>SKELETON</b>''', styleSheet["BodyText"])
        p_observer = Paragraph('''<b>OBSERVER</b>''', styleSheet["BodyText"])
        p_date = Paragraph('''<b>DATE</b>''', styleSheet["BodyText"])

        tdata = [
            [p_site, data['site'], '', ''],
            [p_location, data['location'], p_skeleton, data['skeleton']],
            [p_date, data['obs_date'], p_observer, data['observer']]
        ]

        t = Table(tdata)
        t.setStyle(TableStyle([('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                               ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                               ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                               ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                               ('SPAN', (1, 0), (3, 0)),
                               ('FONTNAME', (0, 0), (-1, -1), 'Arial')
                               ]))

        t._argW[0] = 25 * mm
        t._argW[1] = 63 * mm
        t._argW[2] = 25 * mm
        t._argW[3] = 63 * mm

        elements.append(t)

        # Skull
        elements.append(Spacer(0, 2 * mm))
        custom_style = styleSheet['Heading2']
        custom_style.alignment = 1
        elements.append(Paragraph("Skull inventory", custom_style))
        elements.append(Spacer(0, 2 * mm))

        row1 = ['Bone', 'L', 'R', 'Bone', 'L', 'R', 'Bone', 'L', 'R', 'Vomer', '']

        row2 = ['Frontal',
                data['frontal'],
                '',
                'Sphenoid',
                data['sphenoid'],
                '',
                'Mandible',
                data['mandible'],
                '',
                'Ethmoid',
                data['ethmoid']
                ]

        row3 = ['Parietal',
                data['parietal_l'],
                data['parietal_r'],
                'Nasal',
                data['nasal_l'],
                data['nasal_r'],
                'Palatine',
                data['palatine_l'],
                data['palatine_r'],
                'Thyroid',
                data['thyroid']
                ]

        row4 = ['Occipital',
                data['occipital'],
                '',
                'Maxilla',
                data['maxilla_l'],
                data['maxilla_r'],
                'Lacrimal',
                data['lacrimal_l'],
                data['lacrimal_r'],
                'Hyoid',
                data['hyoid']
                ]

        row5 = ['Temporal',
                data['temporal_l'],
                data['temporal_r'],
                'Zygomatic',
                data['zygomatic_l'],
                data['zygomatic_r'],
                'Orbit',
                data['orbit_l'],
                data['orbit_r'],
                'Calotte',
                data['calotte']
                ]

        sdata = [
            row1,
            row2,
            row3,
            row4,
            row5
        ]

        s = Table(sdata)

        s.setStyle(TableStyle([('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                               ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                               ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                               ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                               ('FONTNAME', (0, 0), (-1, -1), 'Arial'),
                               ('SPAN', (1, 1), (2, 1)),
                               ('SPAN', (4, 1), (5, 1)),
                               ('SPAN', (7, 1), (8, 1)),
                               ('SPAN', (1, 3), (2, 3)),
                               ('ALIGN', (0, 0), (8, 0), 'CENTER'),
                               ('ALIGN', (1, 1), (2, 4), 'CENTER'),
                               ('ALIGN', (4, 1), (5, 4), 'CENTER'),
                               ('ALIGN', (7, 1), (8, 4), 'CENTER'),
                               ('ALIGN', (10, 1), (10, 4), 'CENTER'),
                               ]))

        s._argW[0] = 23 * mm
        s._argW[1] = 12 * mm
        s._argW[2] = 12 * mm
        s._argW[3] = 23 * mm
        s._argW[4] = 12 * mm
        s._argW[5] = 12 * mm
        s._argW[6] = 23 * mm
        s._argW[7] = 12 * mm
        s._argW[8] = 12 * mm
        s._argW[9] = 24 * mm
        s._argW[10] = 12 * mm

        elements.append(s)

        # prepare SVG
        self.create_svg("skull_tmp", data)

        # add svg to report
        drawing = svg2rlg("skull_tmp.svg")
        drawing.hAlign = 'CENTER'
        elements.append(drawing)

        # write the document to disk
        try:
            doc.build(elements)
        except Exception as e:
            result = '{}'.format(e)
        else:
            result = ''
        finally:
            if os.path.exists('skull_tmp.svg'):
                os.remove('skull_tmp.svg')

        return result

    def create_svg(self, file_out, bone):
        """ """
        colors = {}
        colors[0] = 'fill:#ffffff'
        colors[1] = 'fill:#e1e1e1'
        colors[2] = 'fill:#808080'
        colors[3] = 'fill:#4b4b4b'
        colors[4] = 'fill:#000000'

        doc = etree.parse('svg/skull_small.svg')
        for action, el in etree.iterwalk(doc):
            id = el.attrib.get('id')
            if id in bone:
                # print(el.tag)
                # print(el.attrib)
                attributes = el.attrib
                attributes["style"] = colors[bone[id]] + ";fill-opacity:1"
                if len(el) > 0:
                    for item in el:
                        item_attr = item.attrib
                        styl = item_attr["style"]
                        if "fill:#ffffff" in styl:
                            styl = styl.replace('fill:#ffffff', colors[bone[id]])
                        item_attr["style"] = styl

        with open(file_out + '.svg', 'w') as f:
            f.write('<?xml version="1.0" encoding="UTF-8"?>\n' +
                    etree.tostring(doc, pretty_print=True).decode('utf-8'))

        drawing = svg2rlg(file_out + '.svg')
        #renderPDF.drawToFile(drawing, file_out + '.pdf')
        #renderPM.drawToFile(drawing, file_out + '.png', fmt="PNG")
