"""Builds Sarabo_Presentation.pptx (5-minute talk; live demo follows separately).

Run:  python build_slides.py
Needs: python-pptx (pip install python-pptx==1.0.2)
"""
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR

HERE = Path(__file__).parent
ROOT = HERE.parent.parent
ASSETS = ROOT / "sarabo-client" / "src" / "assets"
SCREENS = HERE / "screens"
UNI_LOGO = HERE.parent / "report" / "img" / "metrologo.png"

INK = RGBColor(0x0F, 0x24, 0x30)
INK2 = RGBColor(0x1A, 0x36, 0x45)
MARIGOLD = RGBColor(0xF2, 0xB1, 0x38)
VERDIGRIS = RGBColor(0x1E, 0x6F, 0x63)
PAPER = RGBColor(0xF6, 0xF7, 0xF5)
LINE = RGBColor(0xE2, 0xE5, 0xE1)
MUTED = RGBColor(0x5B, 0x6B, 0x73)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
SOFT = RGBColor(0xC9, 0xD4, 0xD8)
FONT = "Segoe UI"

prs = Presentation()
prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
W, H = prs.slide_width, prs.slide_height
BLANK = prs.slide_layouts[6]


def bg(slide, color):
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = color


def text(slide, x, y, w, h, s, size=18, color=INK, bold=False, align=PP_ALIGN.LEFT,
         anchor=MSO_ANCHOR.TOP, font=FONT, spacing=1.1):
    tb = slide.shapes.add_textbox(x, y, w, h)
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = anchor
    lines = s if isinstance(s, list) else [s]
    for i, line in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        p.line_spacing = spacing
        runs = line if isinstance(line, list) else [(line, {})]
        for chunk, fmt in runs:
            r = p.add_run()
            r.text = chunk
            r.font.name = font
            r.font.size = Pt(fmt.get("size", size))
            r.font.bold = fmt.get("bold", bold)
            r.font.color.rgb = fmt.get("color", color)
    return tb


def box(slide, x, y, w, h, fill=WHITE, line=LINE, radius=True, shadow=False):
    shp = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE if radius else MSO_SHAPE.RECTANGLE, x, y, w, h)
    if radius:
        shp.adjustments[0] = 0.08
    shp.fill.solid()
    shp.fill.fore_color.rgb = fill
    if line is None:
        shp.line.fill.background()
    else:
        shp.line.color.rgb = line
        shp.line.width = Pt(1)
    if not shadow:
        shp.shadow.inherit = False
    return shp


def kicker(slide, s, x=Inches(0.8), y=Inches(0.55), color=VERDIGRIS):
    text(slide, x, y, Inches(8), Inches(0.35), s.upper(), size=13, color=color, bold=True)


def title(slide, s, x=Inches(0.8), y=Inches(0.9), color=INK, size=34, w=Inches(11.7)):
    text(slide, x, y, w, Inches(0.9), s, size=size, color=color, bold=True)


def footer(slide, n, dark=False):
    c = SOFT if dark else MUTED
    text(slide, Inches(0.8), H - Inches(0.5), Inches(6), Inches(0.3), "Sarabo  ·  Jahid Hasan  ·  Metropolitan University", size=10, color=c)
    text(slide, W - Inches(1.6), H - Inches(0.5), Inches(0.8), Inches(0.3), f"{n}/10", size=10, color=c, align=PP_ALIGN.RIGHT)


def picture(slide, path, x, y, w=None, h=None, border=True):
    pic = slide.shapes.add_picture(str(path), x, y, w, h)
    if border:
        pic.line.color.rgb = LINE
        pic.line.width = Pt(1)
    return pic


def notes(slide, s):
    slide.notes_slide.notes_text_frame.text = s


def arrow(slide, x1, y1, x2, y2, color=MUTED, width=1.75):
    c = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, x1, y1, x2, y2)
    c.line.color.rgb = color
    c.line.width = Pt(width)
    ln = c.line._get_or_add_ln()
    tail = ln.makeelement("{http://schemas.openxmlformats.org/drawingml/2006/main}tailEnd", {"type": "triangle"})
    ln.append(tail)
    return c


# ---------------------------------------------------------------- 1. Title
s = prs.slides.add_slide(BLANK)
bg(s, INK)
band = box(s, 0, 0, Inches(0.22), H, fill=MARIGOLD, line=None, radius=False)
picture(s, ASSETS / "logo-on-ink.png", Inches(0.9), Inches(0.8), h=Inches(0.9), border=False)
text(s, Inches(0.9), Inches(2.2), Inches(11), Inches(1.4), "Repair your device with confidence.", size=46, color=WHITE, bold=True)
text(s, Inches(0.9), Inches(3.25), Inches(10.5), Inches(1),
     "Sarabo: An Electronics Repair Service Management Platform", size=24, color=MARIGOLD)
text(s, Inches(0.9), Inches(4.6), Inches(7), Inches(1.6), [
    [("Jahid Hasan", {"bold": True, "color": WHITE, "size": 20})],
    [("ID 222-115-116  ·  Batch 57 (C)", {"color": SOFT})],
    [("Supervisor: Shrabanti Chowdhury, Senior Lecturer", {"color": SOFT})],
    [("Department of CSE, Metropolitan University, Sylhet", {"color": SOFT})],
], size=16, spacing=1.25)
uni = box(s, W - Inches(3.9), H - Inches(2.05), Inches(3.1), Inches(1.6), fill=WHITE, line=None)
picture(s, UNI_LOGO, W - Inches(3.75), H - Inches(1.95), w=Inches(2.8), border=False)
notes(s, "[0:00-0:20]\nAssalamu alaikum. I am Jahid Hasan, ID 222-115-116. My final year project, supervised by "
         "Shrabanti Chowdhury, is Sarabo, an electronics repair service management platform. In the next five "
         "minutes I will show the problem, how Sarabo solves it, how it is built, and how I verified it. Then I "
         "will give a live demo.")

# ---------------------------------------------------------------- 2. Problem
s = prs.slides.add_slide(BLANK)
bg(s, PAPER)
kicker(s, "The problem")
title(s, "Getting a device repaired is a leap of faith")
cards = [
    ("Customers", ["No price before hand-over", "No idea where the device is", "No record if something goes wrong"]),
    ("Technicians", ["Work comes by word of mouth", "Inspection and quote on paper", "Payment is uncertain"]),
    ("The business", ["No view of stuck or late jobs", "Refunds handled by hand", "Demand turned away is invisible"]),
]
for i, (h, items) in enumerate(cards):
    x = Inches(0.8 + i * 4.0)
    box(s, x, Inches(2.2), Inches(3.7), Inches(3.9))
    box(s, x, Inches(2.2), Inches(3.7), Inches(0.12), fill=MARIGOLD, line=None, radius=False)
    text(s, x + Inches(0.35), Inches(2.6), Inches(3.1), Inches(0.5), h, size=22, bold=True)
    text(s, x + Inches(0.35), Inches(3.35), Inches(3.1), Inches(2.6),
         [[("—  " + it, {})] for it in items], size=16, color=MUTED, spacing=1.3)
text(s, Inches(0.8), Inches(6.35), Inches(11.7), Inches(0.5),
     "Result: low trust on both sides, and many repairs never happen.", size=17, color=VERDIGRIS, bold=True)
footer(s, 2)
notes(s, "[0:20-0:50]\nToday, getting a phone or AC repaired is a leap of faith. The customer hands over the device "
         "without knowing the price, cannot see where it is, and has no record if something goes wrong. "
         "Technicians find work only by word of mouth and write quotes on paper. And whoever runs the service "
         "cannot see which jobs are stuck or how much demand is lost.")

# ---------------------------------------------------------------- 3. Solution
s = prs.slides.add_slide(BLANK)
bg(s, PAPER)
kicker(s, "The solution")
title(s, "One tracked, priced workflow for three roles", w=Inches(6.2), size=30)
roles = [
    ("Customer", "Requests a repair, compares offers, approves the price, pays and tracks every step"),
    ("Technician", "Finds nearby matching jobs, sends offers, inspects, quotes, repairs, gets paid via bKash"),
    ("Admin", "Approves technicians, manages prices, handles refunds and late pickups, reads reports"),
]
for i, (r, d) in enumerate(roles):
    y = Inches(2.35 + i * 1.35)
    box(s, Inches(0.8), y, Inches(5.7), Inches(1.15))
    box(s, Inches(0.8), y, Inches(0.12), Inches(1.15), fill=VERDIGRIS, line=None, radius=False)
    text(s, Inches(1.15), y + Inches(0.15), Inches(5.2), Inches(0.4), r, size=19, bold=True)
    text(s, Inches(1.15), y + Inches(0.52), Inches(5.2), Inches(0.6), d, size=13.5, color=MUTED)
picture(s, SCREENS / "home.png", Inches(6.9), Inches(1.0), w=Inches(5.65))
text(s, Inches(6.9), Inches(4.65), Inches(5.65), Inches(0.3), "Live at sarabo-jahid.web.app", size=12, color=MUTED, align=PP_ALIGN.CENTER)
text(s, Inches(6.9), Inches(5.2), Inches(5.65), Inches(1.2), [
    [("45", {"bold": True, "color": INK, "size": 30}), ("  services   ", {"color": MUTED}),
     ("8", {"bold": True, "color": INK, "size": 30}), ("  device types   ", {"color": MUTED}),
     ("BDT", {"bold": True, "color": INK, "size": 30}), ("  prices", {"color": MUTED})],
], size=15, align=PP_ALIGN.CENTER)
footer(s, 3)
notes(s, "[0:50-1:20]\nSarabo turns this into one tracked, priced workflow. Customers request a repair, compare "
         "offers and pay online. Technicians get matching jobs near them and a wallet. Admins see everything that "
         "needs attention. It covers 45 repair services across 8 device types, priced in taka, and it is deployed "
         "and live.")

# ---------------------------------------------------------------- 4. How it works
s = prs.slides.add_slide(BLANK)
bg(s, PAPER)
kicker(s, "How it works")
title(s, "From broken device to paid technician")
steps = [
    ("1", "Request", "Describe the problem (AI can fill the form), add photos, pick a pickup slot"),
    ("2", "Offers", "Matching technicians in the region send estimate + inspection fee"),
    ("3", "Book", "Customer chooses one and pays the fee — technician booked atomically"),
    ("4", "Quote", "Technician inspects, then sends an itemised quote: labour, parts, extras. Approve or reject"),
    ("5", "Pay & repair", "Pay the rest (quote − fee already paid); progress tracked"),
    ("6", "Hand-over", "Customer confirms receipt; technician's 90% becomes withdrawable"),
]
cw, gap = Inches(1.85), Inches(0.12)
for i, (n, h, d) in enumerate(steps):
    x = Inches(0.8) + i * (cw + gap)
    box(s, x, Inches(2.3), cw, Inches(3.3))
    circ = s.shapes.add_shape(MSO_SHAPE.OVAL, x + Inches(0.25), Inches(2.55), Inches(0.62), Inches(0.62))
    circ.fill.solid(); circ.fill.fore_color.rgb = MARIGOLD if i in (2, 4) else INK
    circ.line.fill.background(); circ.shadow.inherit = False
    text(s, x + Inches(0.25), Inches(2.55), Inches(0.62), Inches(0.62), n, size=18, bold=True,
         color=INK if i in (2, 4) else WHITE, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    text(s, x + Inches(0.25), Inches(3.35), cw - Inches(0.4), Inches(0.5), h, size=17, bold=True)
    text(s, x + Inches(0.25), Inches(3.85), cw - Inches(0.45), Inches(1.7), d, size=12.5, color=MUTED, spacing=1.15)
box(s, Inches(0.8), Inches(5.85), Inches(11.7), Inches(0.8), fill=INK, line=None)
text(s, Inches(1.1), Inches(5.85), Inches(11.2), Inches(0.8), [
    [("Fair by design:  ", {"bold": True, "color": MARIGOLD}),
     ("fee refunded if the technician doesn't come or the customer cancels ≥ 2 h before; "
      "otherwise kept and split 90/10", {"color": WHITE})]], size=15, anchor=MSO_ANCHOR.MIDDLE)
footer(s, 4)
notes(s, "[1:20-2:05]\nHere is the journey. One: the customer describes the problem, even in Banglish, adds photos "
         "and picks a pickup slot. Two: approved technicians in that region who have the right skill send offers. "
         "Three: the customer chooses one and pays a small inspection fee, which books the technician. Four: the "
         "technician inspects and sends an itemised quote. Five: the customer approves and pays only the rest, "
         "because the fee already counts. Six: after hand-over, the technician's 90 percent becomes withdrawable. "
         "The fee rules are fair: refunded if the technician doesn't come or the customer cancels in time.")

# ---------------------------------------------------------------- 5. Marketplace screens
s = prs.slides.add_slide(BLANK)
bg(s, PAPER)
kicker(s, "Key features")
title(s, "An open job portal and transparent tracking")
picture(s, SCREENS / "jobs.png", Inches(0.8), Inches(2.0), w=Inches(5.75))
picture(s, SCREENS / "tracking.png", Inches(6.78), Inches(2.0), w=Inches(5.75))
text(s, Inches(0.8), Inches(5.7), Inches(5.75), Inches(1.0), [
    [("Jobs board  ", {"bold": True}), ("safe public summary; matching technicians notified; "
                                         "rejected offer → job reposted", {"color": MUTED})]], size=14)
text(s, Inches(6.78), Inches(5.7), Inches(5.75), Inches(1.0), [
    [("Public tracking  ", {"bold": True}), ("128-bit code, status timeline only — "
                                             "no names, addresses or payment data", {"color": MUTED})]], size=14)
footer(s, 5)
notes(s, "[2:05-2:30]\nTwo things make it a marketplace. The open jobs board shows a safe summary of every waiting "
         "repair; matching technicians are notified and send offers, and if the customer rejects an offer the job "
         "is reposted. And anyone with the tracking code can follow the repair on the service spine: Request, "
         "Inspect, Approve, Repaired, without seeing any personal data.")

# ---------------------------------------------------------------- 6. AI
s = prs.slides.add_slide(BLANK)
bg(s, PAPER)
kicker(s, "Applied AI (Google Gemini)")
title(s, "AI suggests, people decide")
ai = [
    ("Request helper", "Bangla / English / Banglish text or a damage photo → filled request form"),
    ("Offer note", "Writes the technician's offer message; a price guide from real past offers"),
    ("Support chat", "Answers questions from the live service catalogue"),
    ("Report summary", "Headline + actions for admins from the period's figures"),
]
for i, (h, d) in enumerate(ai):
    y = Inches(2.15 + i * 1.08)
    box(s, Inches(0.8), y, Inches(6.0), Inches(0.92))
    text(s, Inches(1.1), y + Inches(0.12), Inches(5.5), Inches(0.35), h, size=17, bold=True)
    text(s, Inches(1.1), y + Inches(0.48), Inches(5.6), Inches(0.4), d, size=12.5, color=MUTED)
box(s, Inches(7.2), Inches(2.15), Inches(5.3), Inches(4.16), fill=INK, line=None)
text(s, Inches(7.55), Inches(2.4), Inches(4.7), Inches(0.4), "Guardrails", size=19, bold=True, color=MARIGOLD)
text(s, Inches(7.55), Inches(2.95), Inches(4.7), Inches(3.3), [
    [("✓  ", {"color": MARIGOLD}), ("Never sets a price", {"color": WHITE})],
    [("✓  ", {"color": MARIGOLD}), ("Output locked to the live catalogue, re-checked on server", {"color": WHITE})],
    [("✓  ", {"color": MARIGOLD}), ("Every number in a summary verified against real data", {"color": WHITE})],
    [("✓  ", {"color": MARIGOLD}), ("No names, emails or card numbers sent to the model", {"color": WHITE})],
    [("✓  ", {"color": MARIGOLD}), ("Per-user and daily site-wide limits", {"color": WHITE})],
], size=14.5, spacing=1.45)
footer(s, 6)
notes(s, "[2:30-3:05]\nI used Google Gemini in four places: a request helper that understands Bangla and Banglish "
         "and even a photo; an offer-note writer and price guide for technicians; a support chat; and a summary "
         "for admin reports. The rule is: AI suggests, people decide. It never sets a price, its answers are "
         "checked against live data, any number in a summary must exist in the real figures, no personal data is "
         "sent, and usage is capped.")

# ---------------------------------------------------------------- 7. Architecture
s = prs.slides.add_slide(BLANK)
bg(s, PAPER)
kicker(s, "Architecture")
title(s, "How it is built")


def node(x, y, w, h, t1, t2, fill=WHITE, c1=INK, c2=MUTED):
    box(s, x, y, w, h, fill=fill, line=LINE if fill == WHITE else None)
    text(s, x, y + Inches(0.12), w, Inches(0.4), t1, size=15, bold=True, color=c1, align=PP_ALIGN.CENTER)
    text(s, x, y + Inches(0.5), w, Inches(0.5), t2, size=11.5, color=c2, align=PP_ALIGN.CENTER)


node(Inches(0.8), Inches(2.6), Inches(2.9), Inches(1.1), "React 19 client", "Vite · Tailwind · TanStack Query", fill=INK, c1=WHITE, c2=SOFT)
node(Inches(5.2), Inches(2.6), Inches(2.9), Inches(1.1), "Express 5 API", "Node.js on Vercel · ~100 endpoints", fill=INK, c1=WHITE, c2=SOFT)
node(Inches(9.6), Inches(2.6), Inches(2.9), Inches(1.1), "MongoDB Atlas", "19 collections · transactions", fill=VERDIGRIS, c1=WHITE, c2=SOFT)
arrow(s, Inches(3.7), Inches(3.15), Inches(5.2), Inches(3.15))
arrow(s, Inches(8.1), Inches(3.15), Inches(9.6), Inches(3.15))
ext = [("Firebase", "Sign-in"), ("Stripe", "Payments, refunds"), ("Supabase", "Private photos"),
       ("Gemini", "AI features"), ("Gmail", "Email"), ("Vercel Cron", "Daily reminders")]
for i, (a, b) in enumerate(ext):
    x = Inches(0.8 + i * 1.98)
    node(x, Inches(4.75), Inches(1.78), Inches(1.0), a, b)
    arrow(s, Inches(6.65), Inches(3.7), x + Inches(0.89), Inches(4.75), color=SOFT, width=1.25)
text(s, Inches(0.8), Inches(6.15), Inches(11.7), Inches(0.5),
     "Client on Firebase Hosting  ·  API on Vercel  ·  CI on GitHub Actions  ·  263 commits, ~75k lines of code",
     size=14, color=MUTED, align=PP_ALIGN.CENTER)
footer(s, 7)
notes(s, "[3:05-3:30]\nTechnically, it is a React single-page app talking to an Express API on Vercel, with MongoDB "
         "Atlas as the database. Around it: Firebase for sign-in, Stripe for payments and refunds, Supabase for "
         "private photos, Gemini for AI, Gmail for email, and a daily scheduled job. About 263 commits and "
         "75 thousand lines across the two repositories.")

# ---------------------------------------------------------------- 8. Correctness
s = prs.slides.add_slide(BLANK)
bg(s, PAPER)
kicker(s, "Engineering for trust")
title(s, "Money and state can never get out of sync")
pts = [
    ("Server decides", "Role + current state checked on every action; the browser never sets a price"),
    ("All-or-nothing", "Booking, payment, settlement and refunds run as database transactions"),
    ("Exactly once", "Signed Stripe webhook; idempotent payments and refunds; no double booking"),
    ("Honest wallet", "90/10 split frozen at payment; balance computed, never stored"),
    ("Private by default", "Signed short-lived photo links; public pages show no personal data"),
]
for i, (h, d) in enumerate(pts):
    y = Inches(2.15 + i * 0.85)
    text(s, Inches(0.8), y, Inches(2.6), Inches(0.4), h, size=17, bold=True, color=VERDIGRIS)
    text(s, Inches(3.4), y + Inches(0.03), Inches(4.5), Inches(0.75), d, size=14, color=INK)
box(s, Inches(8.4), Inches(2.15), Inches(4.1), Inches(2.9), fill=WHITE)
text(s, Inches(8.4), Inches(2.4), Inches(4.1), Inches(0.4), "Concurrency tests", size=14, color=MUTED, align=PP_ALIGN.CENTER)
text(s, Inches(8.6), Inches(2.9), Inches(3.7), Inches(3.1), [
    "Two admins assign at once → one winner",
    "Cancel races payment → one winner",
    "Same webhook ×3 in parallel → one payment",
], size=14, color=INK, spacing=1.9)
footer(s, 8)
notes(s, "[3:30-4:05]\nBecause this handles money, correctness was my main focus. The server checks the role and "
         "the current state for every action. Booking, payment, settlement and refunds are database transactions, "
         "so nothing half-happens. The Stripe webhook is verified and processed exactly once, refunds can't be "
         "issued twice, and the wallet balance is calculated, never stored, so it can't drift. I tested races "
         "directly, like two admins assigning at the same moment.")

# ---------------------------------------------------------------- 9. Results
s = prs.slides.add_slide(BLANK)
bg(s, PAPER)
kicker(s, "Results")
title(s, "Verified, deployed, and ready to grow")
stats = [("2,595", "server checks passed"), ("58", "browser tests passed"), ("11 / 11", "objectives met"), ("Live", "Vercel + Firebase")]
for i, (n, l) in enumerate(stats):
    x = Inches(0.8 + i * 2.98)
    box(s, x, Inches(2.15), Inches(2.75), Inches(1.75))
    text(s, x, Inches(2.35), Inches(2.75), Inches(0.8), n, size=40, bold=True, color=INK, align=PP_ALIGN.CENTER)
    text(s, x, Inches(3.2), Inches(2.75), Inches(0.5), l, size=14, color=MUTED, align=PP_ALIGN.CENTER)
text(s, Inches(0.8), Inches(4.3), Inches(5.6), Inches(0.4), "Limitations", size=18, bold=True)
text(s, Inches(0.8), Inches(4.8), Inches(5.6), Inches(1.6), [
    "—  Stripe in test mode (not available in Bangladesh)",
    "—  Technician payouts sent manually via bKash",
    "—  Not yet used by real customers",
], size=14.5, color=MUTED, spacing=1.5)
text(s, Inches(6.8), Inches(4.3), Inches(5.7), Inches(0.4), "Next", size=18, bold=True)
text(s, Inches(6.8), Inches(4.8), Inches(5.7), Inches(1.6), [
    "—  SSLCOMMERZ / bKash gateway and automated payouts",
    "—  Mobile app, SMS alerts, live technician location",
    "—  Full Bangla interface, warranty claims",
], size=14.5, color=MUTED, spacing=1.5)
footer(s, 9)
notes(s, "[4:05-4:40]\nResults: on 11 October I re-ran everything on an isolated database. All 2,595 server checks "
         "and all 58 browser tests pass, lint and build pass, and the system is deployed. All eleven objectives "
         "were met. Limitations: Stripe is in test mode because it isn't available in Bangladesh, payouts are "
         "manual, and it hasn't had real users yet. Next steps are a local gateway like SSLCOMMERZ or bKash, a "
         "mobile app, SMS, and a full Bangla interface.")

# ---------------------------------------------------------------- 10. Thanks
s = prs.slides.add_slide(BLANK)
bg(s, INK)
box(s, 0, 0, Inches(0.22), H, fill=MARIGOLD, line=None, radius=False)
picture(s, ASSETS / "logo-mark-on-ink.png", Inches(0.9), Inches(1.0), h=Inches(1.1), border=False)
text(s, Inches(0.9), Inches(2.5), Inches(11), Inches(1.2), "Thank you", size=54, bold=True, color=WHITE)
text(s, Inches(0.9), Inches(3.6), Inches(11), Inches(0.8), "Next: live demo — a repair from request to payout", size=24, color=MARIGOLD)
text(s, Inches(0.9), Inches(5.0), Inches(11), Inches(1.2), [
    [("sarabo-jahid.web.app", {"color": WHITE, "bold": True})],
    [("github.com/jahidjubaer/sarabo-client  ·  github.com/jahidjubaer/sarabo-server", {"color": SOFT})],
], size=16, spacing=1.4)
notes(s, "[4:40-5:00]\nSarabo shows that a repair service can be modelled as a controlled, trustworthy workflow, with "
         "AI used safely to help people. Thank you. I will now show it live, from a customer's request all the "
         "way to the technician's payout.")

out = HERE / "Sarabo_Presentation.pptx"
prs.save(out)
print("saved", out)
