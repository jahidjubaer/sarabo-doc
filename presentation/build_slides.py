"""Builds Sarabo_Presentation.pptx: 10 slides for a 5-minute talk, then a thank-you slide that opens the 5-minute live demo.

Short points only, large text and zoomed-in screenshots, so everything can be read
from the back of a classroom. Everything is placed on one grid (left margin 0.7 in,
content width 11.93 in) so edges line up from slide to slide.

Run:  python make_crops.py   (cuts the screenshots from the report)
      python build_slides.py
Needs: python-pptx (pip install python-pptx==1.0.2), Pillow
"""
from pathlib import Path
from PIL import Image
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.oxml.ns import qn

HERE = Path(__file__).parent
ROOT = HERE.parent.parent
ASSETS = ROOT / "sarabo-client" / "src" / "assets"
SCREENS = HERE / "screens"
UNI_LOGO = HERE.parent / "report" / "img" / "metrologo.png"

INK = RGBColor(0x0F, 0x24, 0x30)
MARIGOLD = RGBColor(0xF2, 0xB1, 0x38)
VERDIGRIS = RGBColor(0x1E, 0x6F, 0x63)
PAPER = RGBColor(0xF6, 0xF7, 0xF5)
LINE = RGBColor(0xC9, 0xCF, 0xCB)
MUTED = RGBColor(0x45, 0x55, 0x5D)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
SOFT = RGBColor(0xC9, 0xD4, 0xD8)
FONT = "Segoe UI"

prs = Presentation()
prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
W, H = prs.slide_width, prs.slide_height
BLANK = prs.slide_layouts[6]
TOTAL = 11
LEFT, CONTENT_W, TOP = Inches(0.7), Inches(11.93), Inches(2.0)   # the grid


def bg(slide, color):
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = color


def _runs(p, line, size, color, bold):
    runs = line if isinstance(line, list) else [(line, {})]
    for chunk, fmt in runs:
        r = p.add_run()
        r.text = chunk
        r.font.name = FONT
        r.font.size = Pt(fmt.get("size", size))
        r.font.bold = fmt.get("bold", bold)
        r.font.color.rgb = fmt.get("color", color)


def _textbox(slide, x, y, w, h, anchor):
    tb = slide.shapes.add_textbox(int(x), int(y), int(w), int(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = anchor
    return tb, tf


def text(slide, x, y, w, h, s, size=22, color=INK, bold=False, align=PP_ALIGN.LEFT,
         anchor=MSO_ANCHOR.TOP, spacing=1.1):
    tb, tf = _textbox(slide, x, y, w, h, anchor)
    for i, line in enumerate(s if isinstance(s, list) else [s]):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        p.line_spacing = spacing
        _runs(p, line, size, color, bold)
    return tb


def bullets(slide, x, y, w, h, items, size=22, color=INK, mark=MARIGOLD, gap=10):
    """Real bullets with a hanging indent, so wrapped lines line up under the text."""
    tb, tf = _textbox(slide, x, y, w, h, MSO_ANCHOR.TOP)
    indent = Emu(int(size * 12700 * 1.15))
    for i, it in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.line_spacing = 1.05
        p.space_after = Pt(gap)
        pPr = p._p.get_or_add_pPr()
        pPr.set("marL", str(indent))
        pPr.set("indent", str(-indent))
        clr = pPr.makeelement(qn("a:buClr"), {})
        clr.append(clr.makeelement(qn("a:srgbClr"), {"val": str(mark)}))
        pPr.append(clr)
        pPr.append(pPr.makeelement(qn("a:buSzPct"), {"val": "100000"}))
        pPr.append(pPr.makeelement(qn("a:buFont"), {"typeface": "Arial"}))
        pPr.append(pPr.makeelement(qn("a:buChar"), {"char": "•"}))
        _runs(p, it, size, color, False)
    return tb


def box(slide, x, y, w, h, fill=WHITE, line=LINE, radius=True):
    shp = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE if radius else MSO_SHAPE.RECTANGLE, int(x), int(y), int(w), int(h))
    if radius:
        shp.adjustments[0] = 0.06
    shp.fill.solid()
    shp.fill.fore_color.rgb = fill
    if line is None:
        shp.line.fill.background()
    else:
        shp.line.color.rgb = line
        shp.line.width = Pt(1.25)
    shp.shadow.inherit = False
    return shp


def kicker(slide, s):
    text(slide, LEFT, Inches(0.45), Inches(9), Inches(0.4), s.upper(), size=16, color=VERDIGRIS, bold=True)


def title(slide, s, size=38):
    text(slide, LEFT, Inches(0.85), CONTENT_W, Inches(0.9), s, size=size, bold=True)


def footer(slide, n, dark=False):
    c = SOFT if dark else MUTED
    text(slide, LEFT + CONTENT_W - Inches(1), H - Inches(0.45), Inches(1), Inches(0.3), f"{n}/{TOTAL}", size=12, color=c, align=PP_ALIGN.RIGHT)


def fit(slide, name, x, y, max_w, max_h, align="left"):
    """Screenshot as large as possible inside the box, keeping its shape; left-aligned to the grid."""
    iw, ih = Image.open(SCREENS / name).size
    scale = min(max_w / iw, max_h / ih)
    w, h = int(iw * scale), int(ih * scale)
    left = x + (max_w - w) // 2 if align == "center" else x
    pic = slide.shapes.add_picture(str(SCREENS / name), int(left), int(y), int(w), int(h))
    pic.line.color.rgb = LINE
    pic.line.width = Pt(1.25)
    return pic


def picture(slide, path, x, y, w=None, h=None):
    return slide.shapes.add_picture(str(path), x, y, w, h)


def line(slide, x1, y1, x2, y2, color=MUTED, width=2.25):
    c = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, int(x1), int(y1), int(x2), int(y2))
    c.line.color.rgb = color
    c.line.width = Pt(width)
    return c


def arrow(slide, x1, y1, x2, y2, color=MUTED, width=2.0):
    c = line(slide, x1, y1, x2, y2, color, width)
    ln = c.line._get_or_add_ln()
    ln.append(ln.makeelement(qn("a:tailEnd"), {"type": "triangle"}))
    return c


def notes(slide, s):
    slide.notes_slide.notes_text_frame.text = s


def new_slide(kick, head, n):
    s = prs.slides.add_slide(BLANK)
    bg(s, PAPER)
    kicker(s, kick)
    title(s, head)
    footer(s, n)
    return s


# ======================================================== 1. Title  (0:00-0:15)
s = prs.slides.add_slide(BLANK)
bg(s, PAPER)
box(s, 0, 0, Inches(0.22), H, fill=MARIGOLD, line=None, radius=False)
picture(s, ASSETS / "logo.png", Inches(0.9), Inches(0.8), h=Inches(0.9))
text(s, Inches(0.9), Inches(2.1), Inches(12.0), Inches(1.0), "Repair your device with confidence.", size=44, color=INK, bold=True)
text(s, Inches(0.9), Inches(3.2), Inches(11.5), Inches(0.6), "Sarabo: An Electronics Repair Service Management Platform", size=26, color=VERDIGRIS)
text(s, Inches(0.9), Inches(4.5), Inches(7.4), Inches(2.2), [
    [("Jahid Hasan", {"bold": True, "color": INK, "size": 26})],
    [("ID 222-115-116  ·  Batch 57 (C)", {"color": MUTED})],
    [("Supervisor: Shrabanti Chowdhury, Senior Lecturer", {"color": MUTED})],
    [("Dept. of CSE, Metropolitan University, Sylhet", {"color": MUTED})],
], size=20, spacing=1.25)
box(s, W - Inches(3.9), H - Inches(2.05), Inches(3.1), Inches(1.6), fill=WHITE)
picture(s, UNI_LOGO, W - Inches(3.75), H - Inches(1.95), w=Inches(2.8))
notes(s, "[0:00-0:15] Assalamu alaikum. I am Jahid Hasan. My project, supervised by Shrabanti Chowdhury, is Sarabo, "
         "an electronics repair service platform.")

# ======================================================== 2. Problem  (0:15-0:40)
s = new_slide("The problem", "Getting a device repaired is a leap of faith", 2)
cw = (CONTENT_W - Inches(0.5)) / 3
cards = [("Customers", ["No price before hand-over", "No idea where the device is"]),
         ("Technicians", ["Work only by word of mouth", "Payment is uncertain"]),
         ("The business", ["Stuck jobs are invisible", "Refunds done by hand"])]
for i, (h, items) in enumerate(cards):
    x = LEFT + i * (cw + Inches(0.25))
    box(s, x, TOP, cw, Inches(3.55))
    box(s, x, TOP, cw, Inches(0.14), fill=MARIGOLD, line=None, radius=False)
    text(s, x + Inches(0.35), TOP + Inches(0.4), cw - Inches(0.7), Inches(0.6), h, size=28, bold=True)
    bullets(s, x + Inches(0.35), TOP + Inches(1.25), cw - Inches(0.6), Inches(2.2), items, size=22, color=MUTED)
box(s, LEFT, Inches(5.85), CONTENT_W, Inches(0.85), fill=INK, line=None)
text(s, LEFT + Inches(0.35), Inches(5.85), CONTENT_W - Inches(0.7), Inches(0.85),
     "Result: low trust on both sides, and many repairs never happen.", size=22, color=WHITE, bold=True, anchor=MSO_ANCHOR.MIDDLE)
notes(s, "[0:15-0:40] Customers hand over a phone without knowing the price or where it is. Technicians find work only "
         "by word of mouth. Whoever runs the service cannot see stuck jobs, and refunds are done by hand.")

# ======================================================== 3. Solution  (0:40-1:05)
s = new_slide("The solution", "One tracked, priced workflow for three roles", 3)
roles = [("Customer", "Request · compare · pay · track"),
         ("Technician", "Find jobs · quote · repair · get paid"),
         ("Admin", "Approve · prices · problems · reports")]
rw = Inches(5.6)
for i, (r, d) in enumerate(roles):
    y = TOP + i * Inches(1.32)
    box(s, LEFT, y, rw, Inches(1.15))
    box(s, LEFT, y, Inches(0.14), Inches(1.15), fill=VERDIGRIS, line=None, radius=False)
    text(s, LEFT + Inches(0.4), y + Inches(0.12), rw - Inches(0.6), Inches(0.5), r, size=26, bold=True)
    text(s, LEFT + Inches(0.4), y + Inches(0.62), rw - Inches(0.6), Inches(0.45), d, size=19, color=MUTED)
pic = fit(s, "home.png", LEFT + rw + Inches(0.35), TOP, CONTENT_W - rw - Inches(0.35), Inches(3.75))
text(s, pic.left, TOP + Inches(4.05), pic.width, Inches(0.7), [
    [("45", {"bold": True, "size": 32}), ("  services    ", {"color": MUTED}),
     ("8", {"bold": True, "size": 32}), ("  devices    ", {"color": MUTED}),
     ("Live", {"bold": True, "size": 32, "color": VERDIGRIS}), ("  on Vercel", {"color": MUTED})]], size=20)
notes(s, "[0:40-1:05] Sarabo turns this into one tracked, priced workflow for customers, technicians and admins. "
         "45 repair services across 8 device types, priced in taka, and it is live.")

# ======================================================== 4. How it works  (1:05-1:45)
s = new_slide("How it works", "From broken device to paid technician", 4)
steps = [("1", "Request", "AI fills the form"), ("2", "Offers", "Local technicians bid"),
         ("3", "Book", "Pay inspection fee"), ("4", "Quote", "Itemised price"),
         ("5", "Pay & repair", "Fee already counted"), ("6", "Hand-over", "Warranty starts")]
gap = Inches(0.13)
cw = (CONTENT_W - gap * 5) / 6
for i, (n, h, d) in enumerate(steps):
    x = LEFT + i * (cw + gap)
    box(s, x, TOP, cw, Inches(3.4))
    hot = i in (2, 4)
    d0 = Inches(0.78)
    circ = s.shapes.add_shape(MSO_SHAPE.OVAL, int(x + (cw - d0) / 2), int(TOP + Inches(0.3)), int(d0), int(d0))
    circ.fill.solid(); circ.fill.fore_color.rgb = MARIGOLD if hot else INK
    circ.line.fill.background(); circ.shadow.inherit = False
    text(s, x + (cw - d0) / 2, TOP + Inches(0.3), d0, d0, n, size=26, bold=True,
         color=INK if hot else WHITE, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    text(s, x + Inches(0.1), TOP + Inches(1.3), cw - Inches(0.2), Inches(0.85), h, size=22, bold=True,
         align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    text(s, x + Inches(0.15), TOP + Inches(2.2), cw - Inches(0.3), Inches(1.0), d, size=19, color=MUTED, align=PP_ALIGN.CENTER)
box(s, LEFT, Inches(5.75), CONTENT_W, Inches(0.95), fill=INK, line=None)
text(s, LEFT + Inches(0.35), Inches(5.75), CONTENT_W - Inches(0.7), Inches(0.95), [
    [("Fair by design:  ", {"bold": True, "color": MARIGOLD}),
     ("no-show or early cancel = full refund, otherwise fee split 90/10", {"color": WHITE})]],
     size=21, anchor=MSO_ANCHOR.MIDDLE)
notes(s, "[1:05-1:45] One: the customer describes the problem, even in Banglish, and AI fills the form. Two: local "
         "technicians with the right skill send offers. Three: the customer pays a small inspection fee to book. "
         "Four: an itemised quote after inspection. Five: the customer pays only the rest. Six: hand-over, the "
         "technician gets 90 percent, and a 30-day warranty starts.")

# ======================================================== 5. ER diagram  (1:45-2:20)
s = new_slide("How it works: the data", "Entity-relationship diagram", 5)
HEAD = Inches(0.5)
ROW = Inches(0.33)


def entity(x, y, w, name, fields, head=INK):
    """ER entity card: coloured header with the name, key fields underneath (PK/FK)."""
    h = HEAD + Inches(0.14) + len(fields) * ROW
    box(s, x, y, w, h, fill=WHITE, radius=False)
    box(s, x, y, w, HEAD, fill=head, line=None, radius=False)
    text(s, x, y, w, HEAD, name, size=19, bold=True, color=INK if head == MARIGOLD else WHITE,
         align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    text(s, x + Inches(0.15), y + HEAD + Inches(0.07), w - Inches(0.25), h - HEAD, [
        [(k + "  ", {"bold": True, "color": VERDIGRIS, "size": 12}), (v, {})] if k else [(v, {})]
        for k, v in fields], size=15, spacing=1.0)
    return x, y, w, h


def edge(x1, y1, x2, y2):
    line(s, x1, y1, x2, y2, color=INK, width=2.0)


def one(x, y, side):
    """Crow's-foot 'one': two short bars across the line, just outside the entity edge."""
    t = Inches(0.13)
    for d in (Inches(0.12), Inches(0.22)):
        if side == "right":
            line(s, x + d, y - t, x + d, y + t, color=INK, width=2.0)
        elif side == "left":
            line(s, x - d, y - t, x - d, y + t, color=INK, width=2.0)
        elif side == "down":
            line(s, x - t, y + d, x + t, y + d, color=INK, width=2.0)
        else:  # up
            line(s, x - t, y - d, x + t, y - d, color=INK, width=2.0)


def many(x, y, side):
    """Crow's foot 'many' touching the entity edge at (x, y); side = where the line comes from."""
    L, t = Inches(0.3), Inches(0.16)
    if side in ("left", "right"):
        sx = x - L if side == "left" else x + L
        for dy in (-t, 0, t):
            line(s, sx, y, x, y + dy, color=INK, width=2.0)
    else:
        sy = y - L if side == "up" else y + L
        for dx in (-t, 0, t):
            line(s, x, sy, x + dx, y, color=INK, width=2.0)


def lab(x, y, s_, w=Inches(1.3)):
    text(s, x, y, w, Inches(0.35), s_, size=14, bold=True, color=VERDIGRIS)


EW = Inches(2.75)
xr = LEFT + CONTENT_W - EW
u = entity(LEFT, Inches(1.9), EW, "User", [("PK", "email"), ("", "role")])
t = entity(LEFT, Inches(4.55), EW, "Technician", [("PK", "id"), ("FK", "user email"), ("", "region, skills")])
sv = entity(Inches(5.12), Inches(1.9), Inches(3.0), "Service", [("PK", "id"), ("", "price, inspection fee")])
rr = entity(Inches(4.92), Inches(3.75), Inches(3.4), "Repair Request",
            [("PK", "id"), ("FK", "customer, technician, service"), ("", "status, quote")], head=MARIGOLD)
of = entity(Inches(4.92), Inches(5.85), Inches(3.4), "Offer", [("FK", "request, technician, estimate")])
py = entity(xr, Inches(1.9), EW, "Payment", [("FK", "request"), ("", "amount, refund")])
rv = entity(xr, Inches(3.75), EW, "Review", [("FK", "request (unique)"), ("", "rating")])
wc = entity(xr, Inches(5.55), EW, "Warranty Claim", [("FK", "request"), ("", "status")])

ux, uy, uw, uh = u
tx, ty, tw, th = t
sx_, sy_, sw_, sh_ = sv
rx, ry, rw_, rh = rr
ox, oy, ow, oh = of
px_, py_, pw_, ph_ = py
vx, vy, vw, vh = rv
wx, wy, ww, wh = wc
ex = rx + rw_

# User 1 -- 0..1 Technician (left, vertical)
cx = ux + Inches(0.6)
edge(cx, uy + uh, cx, ty)
one(cx, uy + uh, "down"); one(cx, ty, "up")
lab(cx + Inches(0.15), uy + uh + Inches(0.35), "becomes")
# User 1 -- N Repair Request (elbow)
y1, ymid = uy + Inches(0.95), ry + Inches(0.8)
bend = ux + uw + Inches(0.65)
edge(ux + uw, y1, bend, y1); edge(bend, y1, bend, ymid); edge(bend, ymid, rx, ymid)
one(ux + uw, y1, "right"); many(rx, ymid, "left")
lab(ux + uw + Inches(0.12), y1 - Inches(0.42), "creates")
# Technician 1 -- N Repair Request (straight)
y2 = ty + Inches(0.4)
edge(tx + tw, y2, rx, y2)
one(tx + tw, y2, "right"); many(rx, y2, "left")
lab(tx + tw + Inches(0.4), y2 - Inches(0.42), "repairs")
# Technician 1 -- N Offer (elbow under)
bx = tx + tw - Inches(0.6)
y3 = oy + Inches(0.75)
edge(bx, ty + th, bx, y3); edge(bx, y3, ox, y3)
one(bx, ty + th, "down"); many(ox, y3, "left")
lab(bx + Inches(0.15), y3 - Inches(0.42), "sends")
# Service 1 -- N Repair Request (vertical)
c3 = sx_ + sw_ / 2
edge(c3, sy_ + sh_, c3, ry); one(c3, sy_ + sh_, "down"); many(c3, ry, "up")
lab(c3 + Inches(0.3), sy_ + sh_ + Inches(0.1), "priced by")
# Repair Request 1 -- N Offer (vertical)
c2 = rx + rw_ / 2
edge(c2, ry + rh, c2, oy); one(c2, ry + rh, "down"); many(c2, oy, "up")
lab(c2 + Inches(0.3), ry + rh + Inches(0.06), "gets")
# Repair Request 1 -- N Payment (elbow up)
bend2 = xr - Inches(0.6)
yp = py_ + ph_ / 2
ya = ry + Inches(0.3)
edge(ex, ya, bend2, ya); edge(bend2, ya, bend2, yp); edge(bend2, yp, xr, yp)
one(ex, ya, "right"); many(xr, yp, "left")
# Repair Request 1 -- 0..1 Review (straight)
yv = vy + vh / 2
edge(ex, yv, xr, yv); one(ex, yv, "right"); one(xr, yv, "left")
# Repair Request 1 -- 0..2 Warranty Claim (elbow down)
yw = wy + wh / 2
yb = ry + rh - Inches(0.3)
edge(ex, yb, bend2, yb); edge(bend2, yb, bend2, yw); edge(bend2, yw, xr, yw)
one(ex, yb, "right"); many(xr, yw, "left")
lab(ex + Inches(0.35), yb + Inches(0.06), "max 2", w=Inches(0.95))

text(s, LEFT + CONTENT_W - Inches(6.5), Inches(1.05), Inches(6.5), Inches(0.4), [
    [("||", {"bold": True}), ("  one     ", {"color": MUTED}), ("crow's foot", {"bold": True}),
     ("  many     ·     MongoDB", {"color": MUTED})]], size=16, align=PP_ALIGN.RIGHT)
notes(s, "[1:45-2:20] This is the data model in MongoDB. A user creates many repair requests and can become a technician. "
         "Each request is priced by one service, gets many offers, and has its payments, one review and at most two "
         "warranty claims. The quote and inspection are stored inside the request. The crow's foot marks the 'many' side.")

# ======================================================== 6. Key screens  (2:20-3:00)
s = new_slide("Customer", "Compare ranked offers, pay only what is left", 6)
p = fit(s, "offer.png", LEFT, TOP, CONTENT_W, Inches(2.75))
y = p.top + p.height + Inches(0.35)
box(s, LEFT, y, Inches(5.6), Inches(1.6), fill=INK, line=None)
text(s, LEFT + Inches(0.35), y + Inches(0.12), Inches(5.0), Inches(1.45), [
    [("Quote  ", {"color": SOFT}), ("৳4,000", {"bold": True, "color": WHITE})],
    [("Inspection fee paid  ", {"color": SOFT}), ("− ৳200", {"bold": True, "color": WHITE})],
    [("Left to pay  ", {"color": MARIGOLD}), ("৳3,800", {"bold": True, "color": MARIGOLD})]], size=21, spacing=1.12)
bullets(s, LEFT + Inches(6.0), y + Inches(0.05), CONTENT_W - Inches(6.0), Inches(2.0),
        ["Ranked by rating, reliability, price, district, reply time", "Approve and pay in one step"], size=22)
notes(s, "[2:20-3:00] Offers are ranked using five things Sarabo already stores, and the reasons show as tags. The "
         "customer pays the inspection fee to book; after inspection the quote shows exactly what is left to pay.")

# ======================================================== 7. Warranty + no stuck repairs  (3:00-3:35)
s = new_slide("New in the final phase", "30-day warranty, and no repair can get stuck", 7)
p = fit(s, "warranty.png", LEFT, TOP, CONTENT_W, Inches(2.85))
y = p.top + p.height + Inches(0.35)
bullets(s, LEFT, y, Inches(5.4), Inches(1.9), ["Free re-inspection", "Covered: re-repair or refund"], size=22)
box(s, LEFT + Inches(5.7), y - Inches(0.05), CONTENT_W - Inches(5.7), Inches(1.75), fill=INK, line=None)
text(s, LEFT + Inches(6.05), y + Inches(0.1), Inches(5.8), Inches(0.45), "Every wait has a deadline", size=22, bold=True, color=MARIGOLD)
bullets(s, LEFT + Inches(6.05), y + Inches(0.65), Inches(2.9), Inches(1.0), ["Unpaid quote: 3 days", "Receipt: auto, 3 days"],
        size=18, color=WHITE, gap=4)
bullets(s, LEFT + Inches(9.0), y + Inches(0.65), Inches(2.8), Inches(1.0), ["Can't finish: refund", "Stalled: admin alert"],
        size=18, color=WHITE, gap=4)
notes(s, "[3:00-3:35] Every repair has a 30-day warranty: the same technician re-inspects free, and a covered fault is "
         "repaired again or refunded. I also made sure no request can wait forever: every waiting state has a "
         "deadline, an automatic step or an admin alert.")

# ======================================================== 8. AI  (3:35-4:05)
s = new_slide("Applied AI (Google Gemini)", "AI suggests, people decide", 8)
p = fit(s, "chat.png", LEFT, TOP - Inches(0.05), Inches(4.4), Inches(4.85))
x = p.left + p.width + Inches(0.4)
bullets(s, x, TOP + Inches(0.1), Inches(3.2), Inches(4.6), ["Request helper", "Offer note", "Support chat", "Report summary"], size=22)
bx = LEFT + CONTENT_W - Inches(3.9)
box(s, bx, TOP - Inches(0.05), Inches(3.9), Inches(4.85), fill=INK, line=None)
text(s, bx + Inches(0.35), TOP + Inches(0.2), Inches(3.3), Inches(0.5), "Guardrails", size=22, bold=True, color=MARIGOLD)
bullets(s, bx + Inches(0.35), TOP + Inches(0.85), Inches(3.3), Inches(3.8),
        ["Never sets a price", "Checked against live data", "No personal data sent", "Daily usage limits"],
        size=20, color=WHITE, gap=12)
notes(s, "[3:35-4:05] Gemini helps in four places, but AI only suggests and people decide. It never sets a price, every "
         "answer is checked against live data, no personal data is sent, and usage is limited.")

# ======================================================== 9. Built for trust  (4:05-4:35)
s = new_slide("Architecture", "Built so money and state never get out of sync", 9)
nw = (CONTENT_W - Inches(0.8)) / 3


def node(x, y, w, t1, t2, fill):
    box(s, x, y, w, Inches(1.2), fill=fill, line=None)
    text(s, x, y + Inches(0.14), w, Inches(0.5), t1, size=22, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    text(s, x, y + Inches(0.68), w, Inches(0.45), t2, size=17, color=SOFT, align=PP_ALIGN.CENTER)


node(LEFT, TOP, nw, "React 19", "web client", INK)
node(LEFT + nw + Inches(0.4), TOP, nw, "Express 5 API", "Vercel, Mumbai", INK)
node(LEFT + 2 * (nw + Inches(0.4)), TOP, nw, "MongoDB Atlas", "21 collections", VERDIGRIS)
arrow(s, LEFT + nw, TOP + Inches(0.6), LEFT + nw + Inches(0.4), TOP + Inches(0.6))
arrow(s, LEFT + 2 * nw + Inches(0.4), TOP + Inches(0.6), LEFT + 2 * nw + Inches(0.8), TOP + Inches(0.6))
text(s, LEFT, TOP + Inches(1.4), CONTENT_W, Inches(0.45),
     "Firebase sign-in  ·  Stripe payments  ·  Supabase photos  ·  Gemini AI  ·  Gmail", size=19, color=MUTED, align=PP_ALIGN.CENTER)
pts = [("Server decides", "role and state checked on every action"),
       ("All-or-nothing", "booking, payment, refunds in transactions"),
       ("Exactly once", "no double payment, no double booking")]
for i, (h, d) in enumerate(pts):
    x = LEFT + i * (nw + Inches(0.4))
    box(s, x, TOP + Inches(2.15), nw, Inches(2.4))
    box(s, x, TOP + Inches(2.15), nw, Inches(0.12), fill=MARIGOLD, line=None, radius=False)
    text(s, x + Inches(0.3), TOP + Inches(2.5), nw - Inches(0.6), Inches(0.5), h, size=24, bold=True, color=VERDIGRIS)
    text(s, x + Inches(0.3), TOP + Inches(3.15), nw - Inches(0.6), Inches(1.3), d, size=20)
notes(s, "[4:05-4:35] A React app talks to an Express API on Vercel, next to the MongoDB database. Because it handles "
         "money, the server checks role and state for every action, money steps run in database transactions, and "
         "payments and bookings happen exactly once, even under races.")

# ======================================================== 10. Results + thanks  (4:35-5:00)
s = new_slide("Results", "Verified, deployed, and ready to grow", 10)
stats = [("2,761", "server tests pass"), ("58", "browser tests pass"), ("12 / 12", "objectives met"), ("Live", "on Vercel")]
sw = (CONTENT_W - Inches(0.75)) / 4
for i, (n, l) in enumerate(stats):
    x = LEFT + i * (sw + Inches(0.25))
    box(s, x, TOP, sw, Inches(1.7))
    text(s, x, TOP + Inches(0.15), sw, Inches(0.85), n, size=42, bold=True, align=PP_ALIGN.CENTER)
    text(s, x, TOP + Inches(1.05), sw, Inches(0.5), l, size=19, color=MUTED, align=PP_ALIGN.CENTER)
half = (CONTENT_W - Inches(0.4)) / 2
text(s, LEFT, TOP + Inches(2.0), half, Inches(0.5), "Limitations", size=24, bold=True)
bullets(s, LEFT, TOP + Inches(2.55), half, Inches(1.5), ["Stripe test mode, manual bKash payouts", "No real customers yet"],
        size=21, color=MUTED, gap=6)
text(s, LEFT + half + Inches(0.4), TOP + Inches(2.0), half, Inches(0.5), "Next", size=24, bold=True)
bullets(s, LEFT + half + Inches(0.4), TOP + Inches(2.55), half, Inches(1.5),
        ["Local gateway (SSLCOMMERZ / bKash)", "Mobile app, full Bangla interface"], size=21, color=MUTED, gap=6)
notes(s, "[4:35-4:55] All server tests and all 58 browser tests pass, and the system is live; all twelve objectives were "
         "met. Limits: Stripe is in test mode, payouts are manual, and there are no real users yet. Next: a local "
         "payment gateway and a mobile app.")

# ======================================================== 11. Thank you + live demo  (4:55-5:00)
s = prs.slides.add_slide(BLANK)
bg(s, PAPER)
box(s, 0, 0, Inches(0.22), H, fill=MARIGOLD, line=None, radius=False)
picture(s, ASSETS / "logo.png", Inches(0.9), Inches(0.8), h=Inches(0.9))
text(s, Inches(0.9), Inches(2.3), Inches(11.5), Inches(1.3), "Thank you.", size=66, color=INK, bold=True)
text(s, Inches(0.9), Inches(3.75), Inches(11.5), Inches(0.6), "Now, the live demo", size=30, color=VERDIGRIS, bold=True)
box(s, Inches(0.9), Inches(4.75), Inches(7.6), Inches(0.95), fill=INK, line=None)
text(s, Inches(1.25), Inches(4.75), Inches(7.0), Inches(0.95), [
    [("Live  ", {"bold": True, "color": MARIGOLD}), ("sarabo-client-six.vercel.app", {"color": WHITE})]],
    size=24, anchor=MSO_ANCHOR.MIDDLE)
box(s, W - Inches(3.9), H - Inches(2.35), Inches(3.1), Inches(1.6), fill=WHITE)
picture(s, UNI_LOGO, W - Inches(3.75), H - Inches(2.25), w=Inches(2.8))
footer(s, 11)
notes(s, "[4:55-5:00] Thank you. Now let me show you Rahim's repair, live.")

assert len(prs.slides) == TOTAL, len(prs.slides)
out = HERE / "Sarabo_Presentation.pptx"
prs.save(out)
print("saved", out)
