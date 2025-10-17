#### Read Me ####
# -------------------------------------------------------------------------------------------
# File responsible for:
#       Creating form fields
#       Creating buttons
#       Linking JavaScripts to widgets
#       Creating a page with widgets associated with their respective JavaScripts
# -------------------------------------------------------------------------------------------


#### Imports ####

from pdfrw import PdfDict, PdfName, PdfArray
from pdfrw.objects.pdfname import PdfName
from pdfrw.objects.pdfstring import PdfString
from pdfrw.objects.pdfdict import PdfDict
from pdfrw.objects.pdfarray import PdfArray


#### Functions ####

# Creates an interactive text field (widget) in the PDF
def create_field(name, x, y, width, height, r, g, b, opaque=True, value=""):
    field = PdfDict()
    field.Type = PdfName.Annot
    field.Subtype = PdfName.Widget
    field.FT = PdfName.Tx
    field.Ff = 2
    field.Rect = PdfArray([x, y, x + width, y + height])
    field.MaxLen = 160
    field.T = PdfString.encode(name)
    field.V = PdfString.encode(value)

    # Section used for manual appearance modification of fields
    field.AP = PdfDict()
    appearance = field.AP.N = PdfDict()
    appearance.Type = PdfName.XObject
    appearance.Subtype = PdfName.Form
    appearance.FormType = 1
    appearance.BBox = PdfArray([0, 0, width, height])
    appearance.Matrix = PdfArray([1.0, 0.0, 0.0, 1.0, 0.0, 0.0])
    appearance.stream = """
    %f %f %f rg
    0.0 0.0 %f %f re f
    """ % (r, g, b, width, height)

    # Section used for automatic appearance configuration of fields
    field.MK = PdfDict()
    field.MK.BG = PdfArray([r, g, b]) if opaque else PdfArray([])  # Opaque or transparent field

    return field

# Creates an interactive button (widget) in the PDF
def create_button(name, x, y, width, height, r, g, b, label="Button", js_action=""):
    button = PdfDict()
    button.Type = PdfName.Annot
    button.Subtype = PdfName.Widget
    button.FT = PdfName.Btn
    button.Ff = 65536  # PushButton
    button.T = PdfString.encode(name)
    button.Rect = PdfArray([x, y, x + width, y + height])

    # Button background color and native label
    button.MK = PdfDict()
    button.MK.BG = PdfArray([r, g, b])
    # button.MK.BG = None  # no background color
    # button.MK.BC = None  # no border
    button.MK.CA = PdfString.encode(label)

    # JavaScript action
    if js_action:
        button.A = PdfDict()
        button.A.S = PdfName.JavaScript
        button.A.JS = PdfString.encode(js_action)

    return button

# Creates a PDF page containing the fields/buttons and the associated JavaScript code
def create_page(fields, js_script):
    page = PdfDict()
    page.Type = PdfName.Page

    # Font resource definition
    page.Resources = PdfDict()
    page.Resources.Font = PdfDict()
    page.Resources.Font.F1 = PdfDict()
    page.Resources.Font.F1.Type = PdfName.Font
    page.Resources.Font.F1.Subtype = PdfName.Type1
    page.Resources.Font.F1.BaseFont = PdfName.Helvetica

    # Page size
    page.MediaBox = PdfArray([0, 0, 612, 792])

    page.Contents = PdfDict()
    page.Contents.stream = """
        BT
        /F1 24 Tf
        ET
        """

    # Binds JavaScripts to be executed when the PDF document is opened
    page.AA = PdfDict()
    page.AA.O = create_js_action("""
    try {
    %s
    } catch (e) {
    app.alert(e.message);
    }
        """ % (js_script))

    page.Annots = PdfArray(fields)

    return page

# Binds a JavaScript action to a created field, button or page
def create_js_action(js_code):    
    action = PdfDict()
    action.S = PdfName.JavaScript
    action.JS = js_code
    return action
