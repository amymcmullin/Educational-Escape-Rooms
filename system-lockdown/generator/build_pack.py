#!/usr/bin/env python3
"""SYSTEM LOCKDOWN — printable manipulatives pack."""
import math
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                TableStyle, PageBreak, Flowable, KeepTogether)

OUT = "out/SYSTEM_LOCKDOWN_Print_Pack.pdf"

NAVY  = HexColor('#0F2A43')
GREEN = HexColor('#136F52')
AMBER = HexColor('#9A5B06')
RED   = HexColor('#8C2F2F')
LIGHT = HexColor('#EDF1F5')
GRAY  = HexColor('#5B6B7A')
RULE  = HexColor('#B9C4CE')


# ================================================================ PUZZLE CONFIG
# Every station answer is derived from this block. Change these values and
# rebuild to produce a pack with different codes — do that before you run this
# with a cohort that can find this repository.
#
# The four station codes and the master code are printed to stdout on build.

# --- Station A: which digit sits on each component card -----------------------
# The requisition asks for, in order: processor, memory, storage, power supply.
COMPONENT_IDS = {
    'MOTHERBOARD': '1', 'NETWORK INTERFACE CARD': '2', 'MEMORY MODULE': '3',
    'SOLID-STATE DRIVE': '4', 'OPTICAL DRIVE': '5', 'GRAPHICS CARD': '6',
    'PROCESSOR': '7', 'CPU COOLER': '8', 'POWER SUPPLY UNIT': '9', 'MONITOR': '0',
}
REQUISITION_ORDER = ['PROCESSOR', 'MEMORY MODULE', 'SOLID-STATE DRIVE', 'POWER SUPPLY UNIT']

# --- Station B: the word hidden in the memory dump ----------------------------
# Must be uppercase A-Z. Code B = decimal of first char + decimal of last char.
RECOVERY_WORD = 'REBOOT'

# --- Station C: the rogue host and the protocol in the traffic log ------------
ROGUE_HOST_OCTET = 86          # last octet of the device on the wrong subnet
ROGUE_THIRD_OCTET = 11         # legitimate network is 192.168.10.0/24
CONTROL_PORT = 21              # FTP control port, from the reference card

# --- Station D: the Caesar-ciphered ransom note -------------------------------
CIPHER_SHIFT_WORD = 'CYBER'    # shift = len(this word)
RANSOM_PLAINTEXT = [
    'YOUR SYSTEMS ARE MINE.',
    'TO RESTORE, APPLY THE PATCH.',
    'OVERRIDE CODE: THREE ONE NINE TWO',
]
WORD_LOCK = 'PATCH'            # for the optional 5-letter word lock
STATION_D_CODE = '3192'        # must match the digits spelled out above

# --- Derived ------------------------------------------------------------------
CIPHER_SHIFT = len(CIPHER_SHIFT_WORD)


def caesar(text, shift):
    out = []
    for ch in text:
        if 'A' <= ch <= 'Z':
            out.append(chr((ord(ch) - 65 + shift) % 26 + 65))
        else:
            out.append(ch)
    return ''.join(out)


CODE_A = ''.join(COMPONENT_IDS[n] for n in REQUISITION_ORDER)
CODE_B = '%d%d' % (ord(RECOVERY_WORD[0]), ord(RECOVERY_WORD[-1]))
CODE_C = '%d%d' % (ROGUE_HOST_OCTET, CONTROL_PORT)
CODE_D = STATION_D_CODE
MASTER_CODE = ''.join(c[2] for c in (CODE_A, CODE_B, CODE_C, CODE_D))
RANSOM_CIPHERTEXT = [caesar(l, CIPHER_SHIFT) for l in RANSOM_PLAINTEXT]


AW = 7.5 * inch  # available width

S = {}
S['title']  = ParagraphStyle('title', fontName='Helvetica-Bold', fontSize=19, leading=22, textColor=white)
S['tag']    = ParagraphStyle('tag', fontName='Courier-Bold', fontSize=9, leading=11, textColor=white)
S['body']   = ParagraphStyle('body', fontName='Helvetica', fontSize=10.5, leading=14.5, textColor=black)
S['bodyc']  = ParagraphStyle('bodyc', parent=S['body'], alignment=TA_CENTER)
S['small']  = ParagraphStyle('small', fontName='Helvetica', fontSize=8.5, leading=11, textColor=GRAY)
S['smallc'] = ParagraphStyle('smallc', parent=S['small'], alignment=TA_CENTER)
S['h2']     = ParagraphStyle('h2', fontName='Helvetica-Bold', fontSize=12.5, leading=15, textColor=NAVY,
                             spaceBefore=6, spaceAfter=3)
S['mono']   = ParagraphStyle('mono', fontName='Courier', fontSize=10, leading=14, textColor=black)
S['monob']  = ParagraphStyle('monob', fontName='Courier-Bold', fontSize=11.5, leading=15, textColor=black)
S['cardt']  = ParagraphStyle('cardt', fontName='Helvetica-Bold', fontSize=10.5, leading=12.5, textColor=NAVY)
S['cardb']  = ParagraphStyle('cardb', fontName='Helvetica', fontSize=8.2, leading=10.2, textColor=black)
S['id']     = ParagraphStyle('id', fontName='Courier-Bold', fontSize=20, leading=22, textColor=AMBER,
                             alignment=TA_CENTER)
S['note']   = ParagraphStyle('note', fontName='Helvetica-Oblique', fontSize=9, leading=12, textColor=GRAY)


def P(t, st='body'):
    return Paragraph(t, S[st])


def header(tag, title, color=NAVY):
    t = Table([[Paragraph(tag, S['tag']), Paragraph(title, S['title'])]],
              colWidths=[1.55 * inch, AW - 1.55 * inch], rowHeights=[0.52 * inch])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), color),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (0, 0), 10),
        ('LEFTPADDING', (1, 0), (1, 0), 4),
        ('RIGHTPADDING', (-1, 0), (-1, 0), 10),
    ]))
    return [t, Spacer(1, 12)]


def box(content_flowables, bg=LIGHT, border=RULE, pad=10, width=AW):
    t = Table([[content_flowables]], colWidths=[width])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), bg),
        ('BOX', (0, 0), (-1, -1), 0.9, border),
        ('LEFTPADDING', (0, 0), (-1, -1), pad),
        ('RIGHTPADDING', (0, 0), (-1, -1), pad),
        ('TOPPADDING', (0, 0), (-1, -1), pad),
        ('BOTTOMPADDING', (0, 0), (-1, -1), pad),
    ]))
    return t


def cutline(label="CUT ALONG THE LINES"):
    return Paragraph(
        '- - - - - - - - - - - - - - - - - - - - - - -  %s  - - - - - - - - - - - - - - - - - - - - - - -' % label,
        ParagraphStyle('cl', fontName='Courier', fontSize=7.5, textColor=GRAY, alignment=TA_CENTER))


def answer_slots(label, n=4, size=0.42):
    """A row of empty boxes for writing a code."""
    cells = [''] * n
    t = Table([cells], colWidths=[size * inch] * n, rowHeights=[size * inch])
    t.setStyle(TableStyle([('GRID', (0, 0), (-1, -1), 1.1, NAVY)]))
    lab = Paragraph(label, ParagraphStyle('sl', fontName='Helvetica-Bold', fontSize=10, textColor=NAVY))
    outer = Table([[lab, t]], colWidths=[2.2 * inch, n * size * inch])
    outer.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                               ('LEFTPADDING', (0, 0), (-1, -1), 0)]))
    return outer


# ---------------------------------------------------------------- diagrams
class NetDiagram(Flowable):
    W, H = AW, 3.1 * inch

    def wrap(self, *a):
        return (self.W, self.H)

    def draw(self):
        c = self.canv
        cx, cy = self.W / 2, self.H / 2
        # switch
        c.setStrokeColor(NAVY); c.setFillColor(LIGHT); c.setLineWidth(1.4)
        c.roundRect(cx - 1.05 * inch, cy - 0.3 * inch, 2.1 * inch, 0.6 * inch, 6, stroke=1, fill=1)
        c.setFillColor(NAVY); c.setFont('Helvetica-Bold', 10)
        c.drawCentredString(cx, cy + 0.07 * inch, 'SW-CORE-01')
        c.setFont('Courier', 8)
        c.drawCentredString(cx, cy - 0.16 * inch, '24-port switch')

        nodes = [
            ('WKS-01', '192.168.10.24', -2.9, 1.05),
            ('SRV-DB', '192.168.10.15', -0.97, 1.15),
            ('WKS-02', '192.168.10.77', 0.97, 1.15),
            ('PRN-01', '192.168.10.40', 2.9, 1.05),
            ('WKS-03', '192.168.10.9', -1.9, -1.15),
            ('NODE-X', '192.168.%d.%d' % (ROGUE_THIRD_OCTET, ROGUE_HOST_OCTET), 1.9, -1.15),
        ]
        for name, ip, dx, dy in nodes:
            x = cx + dx * inch
            y = cy + dy * inch
            c.setStrokeColor(RULE); c.setLineWidth(1)
            c.line(cx, cy + (0.3 * inch if dy > 0 else -0.3 * inch), x, y - (0.32 * inch if dy > 0 else -0.32 * inch))
            c.setStrokeColor(NAVY); c.setFillColor(white); c.setLineWidth(1.1)
            c.roundRect(x - 0.78 * inch, y - 0.3 * inch, 1.56 * inch, 0.6 * inch, 5, stroke=1, fill=1)
            c.setFillColor(NAVY); c.setFont('Helvetica-Bold', 9)
            c.drawCentredString(x, y + 0.09 * inch, name)
            c.setFillColor(black); c.setFont('Courier', 8)
            c.drawCentredString(x, y - 0.17 * inch, ip)


class CipherWheel(Flowable):
    def __init__(self, radius, inner=False, inset=0.32):
        self.r = radius
        self.inner = inner
        self.inset = inset * inch
        Flowable.__init__(self)

    def wrap(self, *a):
        return (AW, 2 * self.r + 10)

    def draw(self):
        c = self.canv
        cx, cy = AW / 2, self.r + 5
        r = self.r
        c.setLineWidth(1.3); c.setStrokeColor(NAVY); c.setFillColor(white)
        c.circle(cx, cy, r, stroke=1, fill=1)
        # letter ring
        lr = r - self.inset
        c.setFont('Helvetica-Bold', 11)
        c.setFillColor(NAVY if not self.inner else AMBER)
        for i in range(26):
            ang = math.radians(90 - i * (360 / 26.0))
            x = cx + lr * math.cos(ang)
            y = cy + lr * math.sin(ang) - 3.6
            c.drawCentredString(x, y, chr(65 + i))
            # tick
            c.setStrokeColor(RULE); c.setLineWidth(0.6)
            tang = math.radians(90 - (i + 0.5) * (360 / 26.0))
            c.line(cx + (r - self.inset * 1.95) * math.cos(tang), cy + (r - self.inset * 1.95) * math.sin(tang),
                   cx + r * math.cos(tang), cy + r * math.sin(tang))
        c.setStrokeColor(NAVY); c.setLineWidth(0.8)
        c.circle(cx, cy, r - self.inset * 1.95, stroke=1, fill=0)
        # center mark
        c.setStrokeColor(RED); c.setLineWidth(1.2)
        c.line(cx - 7, cy, cx + 7, cy); c.line(cx, cy - 7, cx, cy + 7)
        c.setFillColor(GRAY); c.setFont('Helvetica-Bold', 8.5)
        if self.inner:
            c.drawCentredString(cx, cy - 0.34 * inch, 'INNER DISC')
            c.drawCentredString(cx, cy - 0.5 * inch, 'CIPHERTEXT')
        else:
            c.drawCentredString(cx, cy + 0.36 * inch, 'OUTER DISC')
            c.drawCentredString(cx, cy + 0.22 * inch, 'PLAINTEXT')
            c.setFont('Helvetica', 7.5)
            c.drawCentredString(cx, cy - 0.62 * inch, 'cut out the shaded center hole and pin')
            c.drawCentredString(cx, cy - 0.76 * inch, 'the INNER DISC on top with a brad')


# ================================================================ PAGES
story = []


def newpage():
    story.append(PageBreak())


# ---- P1 PREP SHEET
story += header('FACILITATOR', 'PRINT &amp; PREP CHECKLIST', GREEN)
story.append(P('Print this pack once, then duplicate the pages marked <b>per team</b>. Everything is black-and-white friendly. '
               'Total prep time: about 25 minutes for a class of 24 (6 teams of 4).'))
story.append(Spacer(1, 10))
rows = [['PAGE', 'ITEM', 'COPIES', 'PREP'],
        ['2', 'Incident Briefing', '1 per team', 'Hand out at start'],
        ['3', 'Team Roster + Role Cards', '1 per team', 'Cut the 5 role cards apart'],
        ['4', 'Station A - Parts Requisition Form', '1 per team', 'Envelope A'],
        ['5-6', 'Station A - Component Cards (10)', '1 set per team', 'Cut apart, shuffle, Envelope A'],
        ['7', 'Station B - Memory Dump', '1 per team', 'Envelope B'],
        ['8', 'Station B - Binary + ASCII Reference', '1 per team', 'Envelope B'],
        ['9', 'Station C - Network Map + Host Table', '1 per team', 'Envelope C'],
        ['10', 'Station C - Subnet + Ports Reference', '1 per team', 'Envelope C'],
        ['11', 'Station D - Ransom Note', '1 per team', 'Envelope D'],
        ['12-13', 'Station D - Cipher Wheel discs', '1 per team', 'Cut out, join with a brad'],
        ['14', 'Recovery Console (final worksheet)', '1 per team', 'Give at the start'],
        ['15', 'Hint Cards (9)', '1 set per team', 'Cut apart, facilitator keeps'],
        ['16', 'Bonus - Phishing Triage', 'fast finishers', 'Hold in reserve'],
        ['17', 'Exit Ticket', '1 per student', 'Debrief'],
        ['18', 'Completion Certificate', '1 per student', 'Optional'],
        ]
t = Table(rows, colWidths=[0.65 * inch, 3.1 * inch, 1.35 * inch, 2.4 * inch])
t.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), NAVY), ('TEXTCOLOR', (0, 0), (-1, 0), white),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'), ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
    ('GRID', (0, 0), (-1, -1), 0.5, RULE), ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, LIGHT]),
    ('TOPPADDING', (0, 0), (-1, -1), 5), ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
]))
story.append(t)
story.append(Spacer(1, 14))
story.append(box([P('<b>ALSO GATHER (optional):</b>', 'body'), Spacer(1, 4),
                  P('4 x four-digit combination locks, 1 lockbox or toolbox, 5 manila envelopes per team, '
                    'brads/paper fasteners (1 per team), scissors, a visible timer, and a small prize for the box. '
                    'No locks? Seal each envelope and write the code on the outside &mdash; teams may only open an '
                    'envelope once they can tell you the code. Or use the Google Form version in the Facilitator Guide.', 'body')]))
newpage()

# ---- P2 BRIEFING
story += header('BRIEFING', 'INCIDENT TICKET #4829', RED)
story.append(box([P('<font color="#8C2F2F"><b>PRIORITY 1 &mdash; SEV-1 &mdash; ACTIVE INCIDENT</b></font>', 'body')], bg=HexColor('#FBEDED'), border=RED))
story.append(Spacer(1, 12))
story.append(P('<b>07:42</b> &mdash; Gulf Coast Data Services calls the help desk. Every workstation in their office is showing '
               'the same message: a red screen, a countdown, and a ransom demand signed <b>BLACKOUT</b>. The primary server is locked. '
               'Payroll runs today.'))
story.append(Spacer(1, 8))
story.append(P('<b>07:51</b> &mdash; Their only IT tech quit two weeks ago. He left no passwords, no diagrams, and no notes &mdash; just '
               'four sealed envelopes in a desk drawer marked <b>A</b>, <b>B</b>, <b>C</b>, and <b>D</b>, and a locked recovery box.'))
story.append(Spacer(1, 8))
story.append(P('<b>07:58</b> &mdash; That is where you come in. You are the incident response team. You have <b>45 minutes</b> before '
               'BLACKOUT wipes the drives.'))
story.append(Spacer(1, 14))
story.append(P('YOUR MISSION', 'h2'))
story.append(P('Each envelope contains a puzzle left behind by the old tech. Each puzzle produces a <b>four-digit station code</b>. '
               'Log all four codes on your <b>Recovery Console</b> worksheet, then follow the recovery protocol printed on it to '
               'assemble the <b>MASTER CODE</b> that opens the recovery box.'))
story.append(Spacer(1, 12))
story.append(box([
    P('<b>RULES OF ENGAGEMENT</b>', 'body'), Spacer(1, 5),
    P('1. Work the envelopes in any order. Split up &mdash; you do not all have to look at the same page.<br/>'
      '2. Everything you need is in the envelopes. No phones, no searching. The reference cards are your documentation.<br/>'
      '3. Nothing counts until the Documentation Lead writes it on the Recovery Console.<br/>'
      '4. You may call for a <b>HINT</b> three times. Raise a hand and say which station.<br/>'
      '5. Do not force, tear, or dismantle anything. Every lock opens with information, not muscle.', 'body')]))
story.append(Spacer(1, 12))
story.append(P('Read the ransom note last if you want to sleep tonight. &mdash; <i>Help Desk Supervisor</i>', 'note'))
newpage()

# ---- P3 ROLES
story += header('TEAM SETUP', 'ROSTER &amp; ROLE CARDS')
story.append(P('Write your team name and assign every role before you open a single envelope. '
               'If your team has four people, the Timekeeper also takes Comms. If you have three, the Incident Commander doubles up.'))
story.append(Spacer(1, 10))
rr = [['TEAM NAME', '', 'START TIME', '', 'STOP TIME', '']]
t = Table(rr, colWidths=[1.05 * inch, 2.45 * inch, 0.9 * inch, 1.05 * inch, 0.9 * inch, 1.15 * inch], rowHeights=[0.4 * inch])
t.setStyle(TableStyle([('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'), ('FONTSIZE', (0, 0), (-1, -1), 8.5),
                       ('TEXTCOLOR', (0, 0), (-1, -1), NAVY), ('GRID', (0, 0), (-1, -1), 0.7, RULE),
                       ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')]))
story.append(t)
story.append(Spacer(1, 16))
story.append(cutline("CUT THE FIVE ROLE CARDS APART"))
story.append(Spacer(1, 8))

roles = [
    ('INCIDENT COMMANDER', 'Keeps the team moving. Decides what the team attacks next and who works on what. '
                           'The only person who may call for a hint. Does not have to be the person who knows the most.'),
    ('DOCUMENTATION LEAD', 'Owns the Recovery Console. Writes down every code the moment it is confirmed. '
                           'If it is not written down, it did not happen.'),
    ('ANALYST', 'Leads the math: binary conversion, IP addressing, and the cipher wheel. Shows the work so a '
                'teammate can check it.'),
    ('HARDWARE SPECIALIST', 'Leads component identification. Keeps the cards laid out face up and organized so '
                            'nothing gets lost under a folder.'),
    ('TIMEKEEPER / COMMS', 'Watches the clock and calls out the 30, 15, and 5 minute marks. Speaks to the facilitator '
                           'on behalf of the team.'),
]
data = []
for name, desc in roles:
    data.append([Paragraph('<b>%s</b>' % name, S['cardt']), Paragraph(desc, S['cardb']),
                 Paragraph('NAME: ______________________', S['cardb'])])
t = Table(data, colWidths=[1.75 * inch, 3.9 * inch, 1.85 * inch], rowHeights=[0.85 * inch] * 5)
t.setStyle(TableStyle([('GRID', (0, 0), (-1, -1), 0.8, NAVY), ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                       ('LEFTPADDING', (0, 0), (-1, -1), 8), ('RIGHTPADDING', (0, 0), (-1, -1), 8)]))
story.append(t)
story.append(Spacer(1, 10))
story.append(P('Every role solves puzzles. The titles describe who is <i>responsible</i>, not who is allowed to think.', 'note'))
newpage()

# ---- P4 STATION A FORM
story += header('ENVELOPE A', 'PARTS REQUISITION FORM', AMBER)
story.append(P('The old tech left a purchase requisition, but he never wrote down the part names &mdash; only what each part '
               '<b>does</b>. Ten component cards are in this envelope. Match each requisition line to the correct card, then write '
               'that card\'s <b>ID digit</b> in the box.'))
story.append(Spacer(1, 12))
req = [['LINE', 'FUNCTION REQUESTED', 'COMPONENT NAME', 'ID'],
       ['R1', 'Executes program instructions. The system\'s decision-maker.', '', ''],
       ['R2', 'Volatile working space. Everything stored here is lost the instant power is removed.', '', ''],
       ['R3', 'Non-volatile storage. Holds the operating system while the machine is powered off.', '', ''],
       ['R4', 'Converts AC from the wall outlet into the DC voltage rails the system needs.', '', '']]
t = Table(req, colWidths=[0.6 * inch, 3.85 * inch, 2.35 * inch, 0.7 * inch],
          rowHeights=[0.34 * inch] + [0.72 * inch] * 4)
t.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), NAVY), ('TEXTCOLOR', (0, 0), (-1, 0), white),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'), ('FONTSIZE', (0, 0), (-1, -1), 9.5),
    ('FONTNAME', (0, 1), (0, -1), 'Courier-Bold'), ('FONTSIZE', (0, 1), (0, -1), 12),
    ('FONTNAME', (1, 1), (1, -1), 'Helvetica'),
    ('GRID', (0, 0), (-1, -1), 0.6, RULE), ('BOX', (0, 0), (-1, -1), 1.1, NAVY),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'), ('ALIGN', (0, 0), (0, -1), 'CENTER'),
    ('ALIGN', (3, 0), (3, -1), 'CENTER'),
    ('BACKGROUND', (2, 1), (3, -1), HexColor('#FFFDF5')),
    ('LEFTPADDING', (1, 0), (1, -1), 8), ('RIGHTPADDING', (1, 0), (1, -1), 8),
]))
story.append(t)
story.append(Spacer(1, 18))
story.append(box([P('<b>STATION A CODE</b> &mdash; read the four ID digits top to bottom, R1 to R4.', 'body'), Spacer(1, 10),
                  answer_slots('CODE A =', 4, 0.5)], bg=HexColor('#FFF8EC'), border=AMBER))
story.append(Spacer(1, 14))
story.append(P('Six of the ten cards are decoys. That is on purpose &mdash; real requisitions arrive with parts you did not order.', 'note'))
newpage()

# ---- P5/P6 COMPONENT CARDS
_components_spec = [
    ('1', 'MOTHERBOARD', 'Large printed circuit board. ATX form factor, 30.5 x 24.4 cm. Chipset, DIMM slots, '
                         'PCIe slots, 24-pin header, SATA headers, rear I/O shield.'),
    ('2', 'NETWORK INTERFACE CARD', 'PCIe x1 expansion card. Single RJ-45 port, 10/100/1000 Mbps, two link LEDs, '
                                    'burned-in 48-bit hardware address.'),
    ('3', 'MEMORY MODULE', 'DDR4 DIMM. 8 GB, 3200 MT/s, 288 pins, off-center notch, low-profile aluminum heat spreader. '
                           'Sold in matched pairs.'),
    ('4', 'SOLID-STATE DRIVE', '2.5 inch, SATA III, 500 GB. NAND flash, no moving parts, 7 mm z-height, '
                               'data + power connectors on one edge.'),
    ('5', 'OPTICAL DRIVE', '5.25 inch bay device. Motorized tray, 650 nm laser assembly, spindle motor, '
                           'eject button and pinhole. Increasingly rare in new builds.'),
    ('6', 'GRAPHICS CARD', 'PCIe x16, dual-slot. Onboard GDDR6, dedicated cooler, 8-pin auxiliary power connector, '
                           'HDMI and DisplayPort outputs.'),
    ('7', 'PROCESSOR', 'Square package roughly 37 x 37 mm. LGA1700, 1700 contact pads, integrated heat spreader, '
                       'gold triangle in one corner for orientation.'),
    ('8', 'CPU COOLER', 'Finned aluminum tower with four copper heat pipes and a 92 mm PWM fan. '
                        'Mounts to the retention bracket. Requires thermal compound.'),
    ('9', 'POWER SUPPLY UNIT', 'Steel enclosure, 150 x 140 x 86 mm. 650 W, 80 PLUS Gold, 120 mm fan, IEC C14 inlet, '
                               'modular cable bundle: 24-pin, EPS, PCIe, SATA.'),
    ('0', 'MONITOR', '27 inch IPS panel, 1920 x 1080, 75 Hz. External peripheral. HDMI in, DisplayPort in, '
                     'VESA 100 mm mount, tilt stand.'),
]


components = [(COMPONENT_IDS.get(_n, _d), _n, _s) for _d, _n, _s in _components_spec]


def component_page(chunk, page_label):
    story.extend(header('ENVELOPE A', 'COMPONENT CARDS %s' % page_label, AMBER))
    story.append(cutline("CUT APART, THEN SHUFFLE"))
    story.append(Spacer(1, 8))
    data = []
    for i in range(0, len(chunk), 2):
        row = []
        for cid, name, spec in chunk[i:i + 2]:
            inner = Table([[Paragraph('<b>%s</b>' % name, S['cardt'])],
                           [Paragraph(spec, S['cardb'])],
                           [Paragraph('ID  %s' % cid, S['id'])]],
                          colWidths=[3.4 * inch], rowHeights=[0.35 * inch, 1.0 * inch, 0.45 * inch])
            inner.setStyle(TableStyle([
                ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'), ('VALIGN', (0, 1), (-1, 1), 'TOP'),
                ('VALIGN', (0, 2), (-1, 2), 'MIDDLE'),
                ('LEFTPADDING', (0, 0), (-1, -1), 0), ('RIGHTPADDING', (0, 0), (-1, -1), 0),
                ('LINEBELOW', (0, 0), (-1, 0), 0.7, RULE),
                ('TOPPADDING', (0, 1), (-1, 1), 6),
            ]))
            row.append(inner)
        while len(row) < 2:
            row.append('')
        data.append(row)
    t = Table(data, colWidths=[3.75 * inch, 3.75 * inch], rowHeights=[2.05 * inch] * len(data))
    t.setStyle(TableStyle([('GRID', (0, 0), (-1, -1), 0.9, NAVY), ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                           ('LEFTPADDING', (0, 0), (-1, -1), 12), ('RIGHTPADDING', (0, 0), (-1, -1), 12),
                           ('TOPPADDING', (0, 0), (-1, -1), 10)]))
    story.append(t)


component_page(components[:6], '1 of 2')
newpage()
component_page(components[6:], '2 of 2')
story.append(Spacer(1, 14))
story.append(box([P('<b>SPARE / BLANK CARDS</b> &mdash; write your own components here if you want to extend the puzzle, '
                    'or leave blank as extra decoys.', 'body')]))
newpage()

# ---- P7 MEMORY DUMP
story += header('ENVELOPE B', 'MEMORY DUMP 0x00 &mdash; 0x%02X' % (len(RECOVERY_WORD) - 1), GREEN)
_nb = {4:'four',5:'five',6:'six',7:'seven',8:'eight',9:'nine',10:'ten'}.get(len(RECOVERY_WORD), str(len(RECOVERY_WORD)))
story.append(P('Before BLACKOUT locked the console, the server flushed %s bytes of memory to the crash log. '
               'The old tech believed these %s bytes spell the <b>recovery command</b>.' % (_nb, _nb)))
story.append(Spacer(1, 12))
dump = [['OFFSET', 'BINARY (8 BITS)', 'DECIMAL', 'CHARACTER']]
for _i, _ch in enumerate(RECOVERY_WORD):
    dump.append(['0x%02X' % _i, ' '.join(format(ord(_ch), '08b')), '', ''])
t = Table(dump, colWidths=[1.1 * inch, 2.9 * inch, 1.75 * inch, 1.75 * inch],
          rowHeights=[0.34 * inch] + [0.52 * inch] * len(RECOVERY_WORD))
t.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), NAVY), ('TEXTCOLOR', (0, 0), (-1, 0), white),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'), ('FONTSIZE', (0, 0), (-1, 0), 9.5),
    ('FONTNAME', (0, 1), (1, -1), 'Courier-Bold'), ('FONTSIZE', (0, 1), (1, -1), 12.5),
    ('GRID', (0, 0), (-1, -1), 0.6, RULE), ('BOX', (0, 0), (-1, -1), 1.1, NAVY),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'), ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('BACKGROUND', (2, 1), (3, -1), HexColor('#F3FAF6')),
]))
story.append(t)
story.append(Spacer(1, 14))
story.append(P('THE RECOVERY COMMAND', 'h2'))
story.append(Table([['  '.join(['____'] * len(RECOVERY_WORD))]], colWidths=[AW],
                   style=TableStyle([('FONTNAME', (0, 0), (-1, -1), 'Courier-Bold'),
                                     ('FONTSIZE', (0, 0), (-1, -1), 22), ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                     ('TOPPADDING', (0, 0), (-1, -1), 6)])))
story.append(Spacer(1, 14))
story.append(box([P('<b>STATION B CODE</b> &mdash; take the <b>decimal value</b> of the <b>first</b> character, then the '
                    '<b>decimal value</b> of the <b>last</b> character, and write them side by side.', 'body'), Spacer(1, 10),
                  answer_slots('CODE B =', 4, 0.5)], bg=HexColor('#F1F8F5'), border=GREEN))
newpage()

# ---- P8 BINARY REFERENCE
story += header('REFERENCE B', 'BINARY &amp; ASCII DECODE CARD', GREEN)
story.append(P('PLACE VALUES &mdash; write these above any byte, then add the columns that hold a 1.', 'h2'))
pv = [['128', '64', '32', '16', '8', '4', '2', '1']]
t = Table(pv, colWidths=[0.9 * inch] * 8, rowHeights=[0.45 * inch])
t.setStyle(TableStyle([('GRID', (0, 0), (-1, -1), 0.9, NAVY), ('FONTNAME', (0, 0), (-1, -1), 'Courier-Bold'),
                       ('FONTSIZE', (0, 0), (-1, -1), 14), ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                       ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'), ('BACKGROUND', (0, 0), (-1, -1), LIGHT)]))
story.append(t)
story.append(Spacer(1, 8))
story.append(box([P('<b>WORKED EXAMPLE</b>', 'body'), Spacer(1, 4),
                  Paragraph('0 1 0 0 1 0 0 0  &rarr;  64 + 8  =  72  &rarr;  the letter  <b>H</b>', S['monob'])]))
story.append(Spacer(1, 16))
story.append(P('ASCII &mdash; UPPERCASE LETTERS', 'h2'))
letters = [(chr(65 + i), 65 + i) for i in range(26)]
rows = []
for start in range(0, 26, 13):
    chunk = letters[start:start + 13]
    rows.append([c for c, _ in chunk])
    rows.append([str(v) for _, v in chunk])
t = Table(rows, colWidths=[0.575 * inch] * 13, rowHeights=[0.3 * inch, 0.3 * inch] * 2)
t.setStyle(TableStyle([('GRID', (0, 0), (-1, -1), 0.5, RULE), ('BOX', (0, 0), (-1, -1), 1.0, NAVY),
                       ('FONTNAME', (0, 0), (-1, -1), 'Courier-Bold'), ('FONTSIZE', (0, 0), (-1, -1), 11),
                       ('ALIGN', (0, 0), (-1, -1), 'CENTER'), ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                       ('BACKGROUND', (0, 0), (-1, 0), LIGHT), ('BACKGROUND', (0, 2), (-1, 2), LIGHT),
                       ('TEXTCOLOR', (0, 0), (-1, 0), NAVY), ('TEXTCOLOR', (0, 2), (-1, 2), NAVY)]))
story.append(t)
story.append(Spacer(1, 16))
story.append(P('WHY IT MATTERS', 'h2'))
story.append(P('A computer stores no letters &mdash; only voltages, read as 1s and 0s. ASCII is the agreement that '
               'the number 82 means the letter R. Change the agreement and the same bits become something else entirely. '
               'This is the whole idea behind character encoding, and it is why a file opened with the wrong encoding '
               'turns into garbage.'))
story.append(Spacer(1, 10))
story.append(box([P('<b>SCRATCH SPACE</b>', 'body'), Spacer(1, 46)]))
newpage()

# ---- P9 NETWORK
story += header('ENVELOPE C', 'NETWORK MAP &amp; HOST TABLE')
story.append(P('This is the client network as the old tech last documented it. Every legitimate device sits on '
               '<b>192.168.10.0 /24</b>. One device on this map does not belong. Find it.'))
story.append(Spacer(1, 2))
story.append(NetDiagram())
story.append(Spacer(1, 2))
ht = [['HOSTNAME', 'IP ADDRESS', 'SUBNET MASK', 'ROLE', 'ON THE /24?'],
      ['WKS-01', '192.168.10.24', '255.255.255.0', 'Front desk workstation', ''],
      ['SRV-DB', '192.168.10.15', '255.255.255.0', 'Database server', ''],
      ['WKS-02', '192.168.10.77', '255.255.255.0', 'Accounting workstation', ''],
      ['PRN-01', '192.168.10.40', '255.255.255.0', 'Network printer', ''],
      ['WKS-03', '192.168.10.9', '255.255.255.0', 'Shop floor workstation', ''],
      ['NODE-X', '192.168.%d.%d' % (ROGUE_THIRD_OCTET, ROGUE_HOST_OCTET), '255.255.255.0', 'UNDOCUMENTED', '']]
t = Table(ht, colWidths=[1.15 * inch, 1.55 * inch, 1.6 * inch, 2.1 * inch, 1.1 * inch],
          rowHeights=[0.32 * inch] + [0.3 * inch] * 6)
t.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), NAVY), ('TEXTCOLOR', (0, 0), (-1, 0), white),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'), ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('FONTNAME', (0, 1), (2, -1), 'Courier'), ('FONTNAME', (3, 1), (3, -1), 'Helvetica'),
    ('GRID', (0, 0), (-1, -1), 0.5, RULE), ('BOX', (0, 0), (-1, -1), 1.0, NAVY),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'), ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
    ('LEFTPADDING', (0, 0), (0, -1), 8),
    ('BACKGROUND', (4, 1), (4, -1), HexColor('#F7F9FB')),
]))
story.append(t)
story.append(Spacer(1, 12))
story.append(Spacer(1, 4))
story.append(P('TRAFFIC LOG EXCERPT', 'h2'))
story.append(box([Paragraph(
    '08:03:11  ALLOW  &lt;rogue host&gt; -&gt; 203.0.113.44  dst-port ????  1.4 GB out<br/>'
    '08:03:11  NOTE   session is plaintext; credentials visible in capture<br/>'
    '08:03:12  NOTE   legacy file-transfer protocol, separate control and data channels',
    S['mono'])], bg=HexColor('#F7F9FB')))
story.append(Spacer(1, 12))
story.append(box([
    P('<b>STATION C CODE</b>', 'body'), Spacer(1, 6),
    P('<b>Part 1</b> &mdash; the <b>host octet</b> (last number) of the device NOT on the /24 network. '
      '<b>Part 2</b> &mdash; the <b>control port</b> of the protocol in the traffic log. Part 1 first, then Part 2.', 'body'),
    Spacer(1, 8),
    answer_slots('CODE C =', 4, 0.5)])) 
newpage()

# ---- P10 NETWORK REFERENCE
story += header('REFERENCE C', 'SUBNET &amp; PORT CARD')
story.append(P('READING AN IPv4 ADDRESS', 'h2'))
story.append(box([Paragraph('192  .  168  .  10  .  24<br/>'
                            '&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|<br/>'
                            'NETWORK PORTION (/24)&nbsp;&nbsp;&nbsp;HOST', S['monob'])]))
story.append(Spacer(1, 8))
story.append(P('A <b>/24</b> (mask 255.255.255.0) means the <b>first three octets identify the network</b> and only the '
               'fourth octet identifies the individual host. Two devices can talk directly to each other only if all three '
               'network octets match exactly. If they do not match, traffic must be routed &mdash; and an undocumented device '
               'on a different network sitting on your switch is a red flag, not a typo.'))
story.append(Spacer(1, 10))
story.append(box([P('<b>QUICK CHECK</b> &mdash; compare one column at a time:', 'body'), Spacer(1, 6),
                  Paragraph('192.168.<b>10</b>.24 &nbsp;and&nbsp; 192.168.<b>10</b>.77 &nbsp;&rarr;&nbsp; same network<br/>'
                            '192.168.<b>10</b>.24 &nbsp;and&nbsp; 192.168.<b>%d</b>.%d &nbsp;&rarr;&nbsp; DIFFERENT network' % (ROGUE_THIRD_OCTET, ROGUE_HOST_OCTET),
                            S['mono'])], bg=HexColor('#F7F9FB')))
story.append(Spacer(1, 16))
story.append(P('COMMON PORTS AND PROTOCOLS', 'h2'))
ports = [['PORT', 'PROTOCOL', 'WHAT IT DOES', 'ENCRYPTED?'],
         ['20', 'FTP (data)', 'File transfer - data channel', 'No'],
         ['21', 'FTP (control)', 'File transfer - commands and login', 'No'],
         ['22', 'SSH / SFTP', 'Secure remote shell and file transfer', 'Yes'],
         ['23', 'Telnet', 'Legacy remote shell', 'No'],
         ['25', 'SMTP', 'Sending mail between servers', 'No'],
         ['53', 'DNS', 'Resolves names to IP addresses', 'No'],
         ['67 / 68', 'DHCP', 'Hands out IP addresses automatically', 'No'],
         ['80', 'HTTP', 'Web traffic', 'No'],
         ['110', 'POP3', 'Retrieving mail', 'No'],
         ['143', 'IMAP', 'Retrieving mail, server-side', 'No'],
         ['443', 'HTTPS', 'Web traffic over TLS', 'Yes'],
         ['3389', 'RDP', 'Windows remote desktop', 'Yes']]
t = Table(ports, colWidths=[0.95 * inch, 1.5 * inch, 3.65 * inch, 1.4 * inch],
          rowHeights=[0.3 * inch] + [0.275 * inch] * 12)
t.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), NAVY), ('TEXTCOLOR', (0, 0), (-1, 0), white),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'), ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('FONTNAME', (0, 1), (1, -1), 'Courier-Bold'), ('FONTNAME', (2, 1), (-1, -1), 'Helvetica'),
    ('GRID', (0, 0), (-1, -1), 0.5, RULE), ('BOX', (0, 0), (-1, -1), 1.0, NAVY),
    ('ALIGN', (0, 0), (1, -1), 'CENTER'), ('ALIGN', (3, 0), (3, -1), 'CENTER'),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'), ('LEFTPADDING', (2, 0), (2, -1), 8),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, LIGHT]),
]))
story.append(t)
story.append(Spacer(1, 10))
story.append(P('"Legacy" and "unencrypted" are the two words that should make an analyst sit up. Anything in the '
               'No column can be read by anyone sitting between the two endpoints.', 'note'))
newpage()

# ---- P11 RANSOM NOTE
story += header('ENVELOPE D', 'THE RANSOM NOTE', RED)
story.append(P('This text was printed on every screen in the building. It is enciphered. BLACKOUT is arrogant enough '
               'to have left the shift value in the signature.'))
story.append(Spacer(1, 12))
note_style = ParagraphStyle('note_s', fontName='Courier-Bold', fontSize=15, leading=26,
                            textColor=HexColor('#7A1F1F'), alignment=TA_CENTER)
_c1, _c2, _c3 = RANSOM_CIPHERTEXT
_c3a, _c3b = _c3.split(': ', 1)
story.append(box([Paragraph(_c1.replace(' ', '  '), note_style),
                  Paragraph(_c2.replace(' ', '  '), note_style),
                  Spacer(1, 6),
                  Paragraph(_c3a + ':', note_style),
                  Paragraph(_c3b.replace(' ', '  '), note_style),
                  Spacer(1, 10),
                  Paragraph('&mdash; BLACKOUT', ParagraphStyle('sig', fontName='Courier-Bold', fontSize=11,
                                                               textColor=HexColor('#7A1F1F'), alignment=TA_CENTER)),
                  Paragraph('shift = the number of letters in the word ' + CIPHER_SHIFT_WORD,
                            ParagraphStyle('sig2', fontName='Courier', fontSize=9.5,
                                           textColor=HexColor('#7A1F1F'), alignment=TA_CENTER))],
                 bg=HexColor('#FBEDED'), border=RED, pad=16))
story.append(Spacer(1, 14))
story.append(P('DECODE IT HERE', 'h2'))
story.append(box([Spacer(1, 8),
                  Paragraph('_________________________________________________________', S['monob']), Spacer(1, 10),
                  Paragraph('_________________________________________________________', S['monob']), Spacer(1, 10),
                  Paragraph('_________________________________________________________', S['monob']), Spacer(1, 6)],
                 bg=white))
story.append(Spacer(1, 14))
story.append(box([
    P('<b>STATION D CODE</b> &mdash; the note spells the override code out in words. Write it as four digits. '
      '(If your station uses a five-letter word lock, the note also names the action you must take &mdash; that word is your lock code.)', 'body'),
    Spacer(1, 10), answer_slots('CODE D =', 4, 0.5)], bg=HexColor('#FBEDED'), border=RED))
newpage()

# ---- P12/13 CIPHER WHEEL
story += header('TOOL D', 'CIPHER WHEEL &mdash; OUTER DISC', RED)
story.append(P('Cut out both discs (this page and the next). Push a brad through the red cross at the center of each, '
               'inner disc on top. Now you can rotate one alphabet against the other.', 'small'))
story.append(Spacer(1, 4))
story.append(CipherWheel(3.05 * inch, inner=False))
newpage()

story += header('TOOL D', 'CIPHER WHEEL &mdash; INNER DISC', RED)
story.append(CipherWheel(2.52 * inch, inner=True, inset=0.17))
story.append(Spacer(1, 12))
story.append(box([
    P('<b>HOW TO USE IT</b>', 'body'), Spacer(1, 5),
    P('1. Work out the shift value from the signature on the ransom note.<br/>'
      '2. A Caesar cipher shifts <i>forward</i> to encrypt. With a shift of 3, plaintext A becomes ciphertext D. '
      'So line up <b>OUTER A</b> with the ciphertext letter that is that many steps ahead on the <b>INNER</b> ring.<br/>'
      '3. To decode: find each ciphertext letter on the <b>INNER</b> ring and read the letter directly outside it '
      'on the <b>OUTER</b> ring.<br/>'
      '4. Once the wheel is aligned, it stays aligned for the whole message. Do not spin it again.', 'body'),
    Spacer(1, 8),
    P('<b>WHY THIS MATTERS:</b> the Caesar cipher is roughly 2,000 years old and a modern laptop breaks it in under a '
      'millisecond &mdash; there are only 25 possible keys. It survives today only as a teaching tool and as ROT13 on '
      'internet forums. Every real cipher you will meet later solves the same problem this one does; it just uses a '
      'keyspace too large to walk through by hand.', 'body')]))
newpage()

# ---- P14 RECOVERY CONSOLE
story += header('FINAL', 'RECOVERY CONSOLE')
story.append(P('Log every station code the moment you confirm it. When all four are logged, run the recovery protocol '
               'at the bottom to assemble the MASTER CODE.'))
story.append(Spacer(1, 14))
con = [['STATION', 'SOURCE', 'CODE (4 DIGITS)', 'THIRD DIGIT', 'CONFIRMED BY'],
       ['A', 'Parts Requisition', '', '', ''],
       ['B', 'Memory Dump', '', '', ''],
       ['C', 'Network Map', '', '', ''],
       ['D', 'Ransom Note', '', '', '']]
t = Table(con, colWidths=[0.95 * inch, 2.1 * inch, 1.85 * inch, 1.15 * inch, 1.45 * inch],
          rowHeights=[0.36 * inch] + [0.72 * inch] * 4)
t.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), NAVY), ('TEXTCOLOR', (0, 0), (-1, 0), white),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'), ('FONTSIZE', (0, 0), (-1, -1), 9.5),
    ('FONTNAME', (0, 1), (0, -1), 'Courier-Bold'), ('FONTSIZE', (0, 1), (0, -1), 17),
    ('FONTNAME', (1, 1), (1, -1), 'Helvetica'),
    ('GRID', (0, 0), (-1, -1), 0.6, RULE), ('BOX', (0, 0), (-1, -1), 1.2, NAVY),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'), ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('BACKGROUND', (2, 1), (3, -1), HexColor('#F7F9FB')),
    ('BACKGROUND', (3, 1), (3, -1), HexColor('#FFF8EC')),
]))
story.append(t)
story.append(Spacer(1, 20))
story.append(box([
    P('<b>RECOVERY PROTOCOL</b>', 'body'), Spacer(1, 6),
    P('The recovery box does not accept any single station code. Take the <b>THIRD DIGIT FROM THE LEFT</b> of each '
      'station code and write them in order A, B, C, D.', 'body'), Spacer(1, 6),
    Paragraph('EXAMPLE:&nbsp;&nbsp;1 2 <b>3</b> 4&nbsp;&nbsp;&rarr;&nbsp;&nbsp;third digit is <b>3</b>', S['mono'])],
    bg=HexColor('#FFF8EC'), border=AMBER))
story.append(Spacer(1, 22))
mc = Table([['', '', '', '']], colWidths=[0.95 * inch] * 4, rowHeights=[0.95 * inch])
mc.setStyle(TableStyle([('GRID', (0, 0), (-1, -1), 2.0, NAVY), ('BACKGROUND', (0, 0), (-1, -1), white)]))
wrap = Table([[Paragraph('<b>MASTER<br/>CODE</b>', ParagraphStyle('mcl', fontName='Helvetica-Bold', fontSize=15,
                                                                 leading=18, textColor=NAVY, alignment=TA_CENTER)), mc]],
             colWidths=[2.0 * inch, 3.8 * inch])
wrap.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'MIDDLE'), ('ALIGN', (0, 0), (-1, -1), 'CENTER')]))
story.append(wrap)
story.append(Spacer(1, 18))
story.append(P('Bring this sheet to the facilitator with all four station codes filled in. An incident is not resolved '
               'until it is documented &mdash; in this room and in every job you will ever hold.', 'note'))
newpage()

# ---- P15 HINTS
story += header('FACILITATOR', 'HINT CARDS &mdash; CUT APART', GREEN)
story.append(P('Hand these out one at a time when a team calls a hint. Give the level-1 card first; only give level 2 '
               'if they are still stuck after two or three minutes.', 'small'))
story.append(Spacer(1, 10))
hints = [
    ('A - LEVEL 1', 'Ignore the specs for a second. Read only the requisition line and ask: what job does this part do? '
                    'Then find the card that could do that job.'),
    ('A - LEVEL 2', 'R1 is a square chip about the size of a postage stamp. R4 is the only card with a wattage rating.'),
    ('A - LEVEL 3', 'Order matters. Read the ID digits R1, R2, R3, R4 - top to bottom, not sorted.'),
    ('B - LEVEL 1', 'Write 128 64 32 16 8 4 2 1 above the eight bits. Add up only the columns that have a 1 under them.'),
    ('B - LEVEL 2', 'Those decimal numbers are ASCII codes. Use the letter table to turn each one into a character first.'),
    ('B - LEVEL 3', 'The word is %s. Now go back to your decimal column: what number is under %s, and what is under %s?' % (RECOVERY_WORD, RECOVERY_WORD[0], RECOVERY_WORD[-1])),
    ('C - LEVEL 1', 'A /24 means the first THREE octets must match. Compare the addresses one column at a time.'),
    ('C - LEVEL 2', 'The rogue device is NODE-X. Now: legacy, unencrypted, separate control and data channels. It is not SSH.'),
    ('D - LEVEL 1', 'Count the letters in the word ' + CIPHER_SHIFT_WORD + '. That number is your shift. Set the wheel and leave it alone.'),
    ('D - LEVEL 2', 'Ciphertext letters live on the INNER ring. Find each one there and read outward to the OUTER ring.'),
    ('D - LEVEL 3', 'The last line spells four digits out in English words. Write the digits, not the words.'),
    ('FINAL', 'The console wants the third digit from the LEFT of each code. In %s that would be %s.' % (' '.join(CODE_A), CODE_A[2])),
]
data = []
for i in range(0, len(hints), 2):
    row = []
    for label, txt in hints[i:i + 2]:
        inner = Table([[Paragraph('<b>%s</b>' % label, ParagraphStyle('hl', fontName='Courier-Bold', fontSize=10,
                                                                     textColor=GREEN))],
                       [Paragraph(txt, S['cardb'])]], colWidths=[3.3 * inch], rowHeights=[0.24 * inch, 0.85 * inch])
        inner.setStyle(TableStyle([('VALIGN', (0, 1), (-1, 1), 'TOP'),
                                   ('LEFTPADDING', (0, 0), (-1, -1), 0), ('RIGHTPADDING', (0, 0), (-1, -1), 0),
                                   ('TOPPADDING', (0, 1), (-1, 1), 4)]))
        row.append(inner)
    data.append(row)
t = Table(data, colWidths=[3.75 * inch, 3.75 * inch], rowHeights=[1.32 * inch] * len(data))
t.setStyle(TableStyle([('GRID', (0, 0), (-1, -1), 0.9, GREEN), ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                       ('LEFTPADDING', (0, 0), (-1, -1), 12), ('RIGHTPADDING', (0, 0), (-1, -1), 12),
                       ('TOPPADDING', (0, 0), (-1, -1), 9)]))
story.append(t)
newpage()

# ---- P16 BONUS
story += header('BONUS', 'PHISHING TRIAGE &mdash; FAST FINISHERS', AMBER)
story.append(P('You unlocked the box early. Before the client goes back online, triage the five messages sitting in the '
               'help desk queue. Mark each <b>PHISH</b> or <b>SAFE</b>, and name the single strongest signal that decided it.'))
story.append(Spacer(1, 12))
mails = [
    ('1', 'FROM: it-support@gulfcoastdata.co  |  SUBJ: Mandatory password reset\n'
          '"Your account expires in 2 hours. Click here to keep access."'),
    ('2', 'FROM: no-reply@ups.com  |  SUBJ: Delivery scheduled for Tuesday\n'
          '"Tracking 1Z8842. No action needed." (You ordered a switch last week.)'),
    ('3', 'FROM: ceo.gulfcoast@gmail.com  |  SUBJ: quick favor, in a meeting\n'
          '"Need you to buy 4 gift cards for a client. Send me the codes. Keep this between us."'),
    ('4', 'FROM: billing@microsoft-secure-login.net  |  SUBJ: Invoice 88213 overdue\n'
          '"Open the attached .zip to view your invoice and avoid suspension."'),
    ('5', 'FROM: jsmith@gulfcoastdata.com  |  SUBJ: Re: printer on the shop floor\n'
          '"Still jamming. Can someone come look at it today?" (Reply in an existing thread you started.)'),
]
rows = [['#', 'MESSAGE', 'PHISH / SAFE', 'STRONGEST SIGNAL']]
for n, body in mails:
    rows.append([n, Paragraph(body.replace('\n', '<br/>'), S['cardb']), '', ''])
t = Table(rows, colWidths=[0.4 * inch, 3.5 * inch, 1.2 * inch, 2.4 * inch],
          rowHeights=[0.32 * inch] + [0.92 * inch] * 5)
t.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), NAVY), ('TEXTCOLOR', (0, 0), (-1, 0), white),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'), ('FONTSIZE', (0, 0), (-1, 0), 9),
    ('FONTNAME', (0, 1), (0, -1), 'Courier-Bold'), ('FONTSIZE', (0, 1), (0, -1), 12),
    ('GRID', (0, 0), (-1, -1), 0.6, RULE), ('BOX', (0, 0), (-1, -1), 1.1, NAVY),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'), ('ALIGN', (0, 0), (0, -1), 'CENTER'),
    ('LEFTPADDING', (1, 0), (1, -1), 8), ('RIGHTPADDING', (1, 0), (1, -1), 8),
]))
story.append(t)
story.append(Spacer(1, 14))
story.append(box([P('<b>THEN ANSWER:</b> BLACKOUT got in somehow. Based on these five messages, write one sentence '
                    'naming the most likely entry point, and one sentence proposing a control that would have stopped it.', 'body'),
                  Spacer(1, 34)]))
newpage()

# ---- P17 EXIT TICKET
story += header('DEBRIEF', 'EXIT TICKET')
story.append(P('NAME ______________________________________     TEAM ______________________________________', 'body'))
story.append(Spacer(1, 16))
qs = [
    'Which station did your team solve fastest, and what made it click?',
    'Which station stalled you the longest? What finally moved it?',
    'Name one thing you know now that you did not know at 8 a.m. today.',
    'Your team had five roles. Which one did you actually end up doing most, and was it the one on your card?',
    'Real incident response looks a lot like this: incomplete documentation, time pressure, and a team you just met. '
    'What is one habit you want to bring into this program because of that?',
]
for i, q in enumerate(qs, 1):
    story.append(Paragraph('<b>%d.</b>  %s' % (i, q), S['body']))
    story.append(Spacer(1, 4))
    story.append(Table([['']], colWidths=[AW], rowHeights=[0.62 * inch],
                       style=TableStyle([('LINEBELOW', (0, 0), (-1, -1), 0.7, RULE),
                                         ('LINEBELOW', (0, 0), (-1, -1), 0.7, RULE)])))
    story.append(Spacer(1, 8))
newpage()

# ---- P18 CERTIFICATE
story.append(Spacer(1, 40))
story.append(Paragraph('CERTIFICATE OF COMPLETION',
                       ParagraphStyle('c1', fontName='Helvetica-Bold', fontSize=13, textColor=GRAY,
                                      alignment=TA_CENTER, spaceAfter=10)))
story.append(Paragraph('SYSTEM LOCKDOWN',
                       ParagraphStyle('c2', fontName='Helvetica-Bold', fontSize=40, textColor=NAVY,
                                      alignment=TA_CENTER, leading=44, spaceAfter=4)))
story.append(Paragraph('INCIDENT #4829 &mdash; RESOLVED',
                       ParagraphStyle('c3', fontName='Courier-Bold', fontSize=13, textColor=RED,
                                      alignment=TA_CENTER, spaceAfter=26)))
story.append(Paragraph('This certifies that', S['bodyc']))
story.append(Spacer(1, 22))
story.append(Table([['']], colWidths=[5.5 * inch], rowHeights=[0.35 * inch],
                   style=TableStyle([('LINEBELOW', (0, 0), (-1, -1), 1.1, NAVY), ('ALIGN', (0, 0), (-1, -1), 'CENTER')])))
story.append(Spacer(1, 8))
story.append(Paragraph('served as a member of the incident response team, recovered a compromised client network '
                       'under time pressure, and returned Gulf Coast Data Services to operation.', S['bodyc']))
story.append(Spacer(1, 26))
story.append(box([Paragraph('DEMONSTRATED: hardware component identification &bull; binary and ASCII conversion &bull; '
                            'IPv4 addressing and subnet logic &bull; port and protocol recognition &bull; basic cryptanalysis &bull; '
                            'incident documentation &bull; collaborative problem solving under pressure', S['smallc'])]))
story.append(Spacer(1, 34))
sig = Table([['', ''], ['TIME TO ESCAPE', 'INSTRUCTOR']],
            colWidths=[3.0 * inch, 3.0 * inch], rowHeights=[0.4 * inch, 0.25 * inch])
sig.setStyle(TableStyle([('LINEBELOW', (0, 0), (-1, 0), 0.9, NAVY),
                         ('FONTNAME', (0, 1), (-1, 1), 'Helvetica-Bold'), ('FONTSIZE', (0, 1), (-1, 1), 8),
                         ('TEXTCOLOR', (0, 1), (-1, 1), GRAY), ('ALIGN', (0, 0), (-1, -1), 'CENTER')]))
w = Table([[sig]], colWidths=[AW], style=TableStyle([('ALIGN', (0, 0), (-1, -1), 'CENTER')]))
story.append(w)


def deco(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(RULE); canvas.setLineWidth(0.6)
    canvas.line(0.5 * inch, 0.42 * inch, 8.0 * inch, 0.42 * inch)
    canvas.setFont('Helvetica', 7); canvas.setFillColor(GRAY)
    canvas.drawString(0.5 * inch, 0.3 * inch, 'SYSTEM LOCKDOWN  |  Computer Systems & IT  |  Escape Room Print Pack')
    canvas.drawRightString(8.0 * inch, 0.3 * inch, 'page %d' % doc.page)
    canvas.restoreState()


doc = SimpleDocTemplate(OUT, pagesize=letter, leftMargin=0.5 * inch, rightMargin=0.5 * inch,
                        topMargin=0.5 * inch, bottomMargin=0.6 * inch,
                        title='SYSTEM LOCKDOWN - Escape Room Print Pack',
                        author='iTECH Computer Systems & IT')
doc.build(story, onFirstPage=deco, onLaterPages=deco)
print('built', OUT)
print('  Station A (components) :', CODE_A)
print('  Station B (%s)     :' % RECOVERY_WORD, CODE_B)
print('  Station C (network)    :', CODE_C)
print('  Station D (cipher)     :', CODE_D, '| word lock:', WORD_LOCK)
print('  MASTER CODE            :', MASTER_CODE)