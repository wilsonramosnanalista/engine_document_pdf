#### Read-me ####
# -------------------------------------------------------------------------------------------
# File responsible for:
#       Specifying component dimensions for the PDF
#       Adding widgets (bar, ball, stripe, screen) to the PDF with pre-defined dimensions
#       Creating a PDF page embedding the JavaScript
#       Saving/Generating the PDF and opening it in the Opera browser
# -------------------------------------------------------------------------------------------

#### Imports ####

import os
import webbrowser
from pdfrw import PdfWriter, PdfReader
from pdfrw.objects.pdfname import PdfName
from pdfrw.objects.pdfstring import PdfString
from pdfrw.objects.pdfdict import PdfDict
from pdfrw.objects.pdfarray import PdfArray

from main_engine import create_field, create_js_action, create_page, create_button


#### Component Dimensions ####

# Page
PAGE_WIDTH = 612
PAGE_HEIGHT = 792

# Canvas
CANVAS_WIDTH = 612
CANVAS_HEIGHT = 400
CANVAS_BASE = PAGE_HEIGHT - CANVAS_HEIGHT

# Bar
BAR_WIDTH = 70
BAR_HEIGHT = 10
BAR_BASE_DISTANCE = CANVAS_BASE + 10

# Ball
BALL_WIDTH = 70
BALL_HEIGHT = 70


#### Add interactive fields (widgets) for the project to work ####
fields = []

# Bar
bar = create_field(
    'bar',
    x=(CANVAS_WIDTH - BAR_WIDTH)/2, y=BAR_BASE_DISTANCE,
    width=BAR_WIDTH, height=BAR_HEIGHT,
    r=0.7, g=0.1, b=0 # Brown color
)
fields.append(bar)

# Ball
ball = create_field(
    'ball',
    x=(CANVAS_WIDTH - BAR_WIDTH)/2, y=CANVAS_BASE + 30,
    width=BALL_WIDTH, height=BALL_HEIGHT,
    r=0.8, g=0, b=0.8
)
fields.append(ball)

# Score Area
scoreArea = create_field(
    'scoreArea',
    x=231,
    y=746,
    width=130,
    height=36,
    r=0.9, g=0.9, b=0.9, opaque=False
)
fields.append(scoreArea)


# Stripes: Add 612 text columns to capture mouse coordinate
for x in range(0, CANVAS_WIDTH):
    stripe = create_field(
        'stripe' + str(x),
        x=x, y=0,
        width=1, height=CANVAS_BASE,
        r=0, g=1, b=0
    )
    stripe.AA = PdfDict()
    stripe.AA.E = create_js_action("""
    global.mouseX = %d;
    """ % x)
    fields.append(stripe)

# Auxiliary field used for rendering in Chrome
# Flow: Displays a large white screen, redraws screen components (ball, bar), then hides the white screen
# Purpose: To refresh components on screen
fields.append(create_field(
    'renderer',
    x=0, y=CANVAS_BASE,
    width=CANVAS_WIDTH, height=CANVAS_HEIGHT,
    r=1, g=1, b=1
))

# Start Screen
start_screen = create_field(
    'start_screen',
    x=0, y=0,
    width=CANVAS_WIDTH, height=CANVAS_HEIGHT,
    r=1, g=1, b=1, opaque=True,
    value=""
)
start_screen.Ff = 1  # Makes the field read-only
fields.append(start_screen)

# New Game Button
newGameButton = create_button(
    "newGameButton",
    x=CANVAS_WIDTH/2 - 60, y=PAGE_HEIGHT/1.5 - 20,
    width=120, height=45,
    r=0.8, g=0.8, b=0.8,
    label="New Game",
    js_action="onNewGameClick()"
)
newGameButton.DA = "/Cour 18 Tf 0 0 0 rg" # Font Text
fields.append(newGameButton)

# Instruction (fixed visual field)
instruction = PdfDict()
instruction.Type = PdfName.Annot
instruction.Subtype = PdfName.Widget
instruction.FT = PdfName.Tx
instruction.T = PdfString.encode("instruction")
instruction.Rect = PdfArray([10, CANVAS_HEIGHT / 1.25, 450, CANVAS_HEIGHT / 1.25 + 20])
instruction.Ff = 1  # ReadOnly
instruction.MK = PdfDict(BG=PdfArray([1, 1, 1]))  # white background

# Appearance (drawn text)
instruction.AP = PdfDict()
appearance = instruction.AP.N = PdfDict()
appearance.Type = PdfName.XObject
appearance.Subtype = PdfName.Form
appearance.FormType = 1
appearance.BBox = PdfArray([0, 0, 400, 20])
appearance.stream = f"""
q
1 1 1 rg
0 0 400 20 re f
BT
/Helv-BoldOblique 12 Tf
0 0 0 rg
10 5 Td
(*Version 1.0 - Tested and functional in Chrome or Opera!) Tj
ET
Q
"""

fields.append(instruction)

#### Read the main JavaScript ####
with open('game_demo.js', 'r') as js_file:
    script_js = js_file.read()


#### Embed JavaScript and global variables into the PDF page ####
page = create_page(fields, """

var PAGE_HEIGHT = %(PAGE_HEIGHT)s;

var CANVAS_WIDTH = %(CANVAS_WIDTH)s;
var CANVAS_HEIGHT = %(CANVAS_HEIGHT)s;
var CANVAS_BASE = %(CANVAS_BASE)s;

var BAR_WIDTH = %(BAR_WIDTH)s;
var BAR_HEIGHT = %(BAR_HEIGHT)s;
var BAR_BASE_DISTANCE = %(BAR_BASE_DISTANCE)s;

var BALL_WIDTH = %(BALL_WIDTH)s;
var BALL_HEIGHT = %(BALL_HEIGHT)s;

%(script_js)s

""" % locals())

page.Contents.stream = f"""
q
0.4 0.94 0.4 rg
0 0 {CANVAS_WIDTH} {CANVAS_HEIGHT - 5} re f
Q

BT
/F1 16 Tf
0.5 0.5 0.5 rg
234 {CANVAS_HEIGHT/1.25 - 12} Td (Move the mouse here!) Tj
ET
"""


#### PDF generation steps and automatic opening in Opera ####
output = PdfWriter()
output.addpage(page)
output.write('game_demo.pdf')

# Absolute path of the generated PDF
pdf_path = os.path.abspath("game_demo.pdf")

# Opera browser path
opera_path = r"C:\Users\Wilson\AppData\Local\Programs\Opera GX\opera.exe"

try:
    # Register Opera as the browser
    webbrowser.register(
        "opera",
        None,
        webbrowser.BackgroundBrowser(opera_path)
    )

    # Open PDF in Opera GX
    webbrowser.get("opera").open_new(pdf_path)
    print("Demo game opened in Opera!")

except Exception as e:
    # If it fails, open in the default browser
    print("Could not open in Opera. Opening in default browser instead...")
    webbrowser.open_new(pdf_path)
