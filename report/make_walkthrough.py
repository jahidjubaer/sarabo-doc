"""Builds Chapter 7 (tex/walkthrough.tex) and its cropped screenshots (img/wt/).

Each screenshot in img/screens is cropped to the part of the screen that matters,
then placed two per row at the same height, so the chapter stays short but every
step of the walkthrough repair keeps its own picture.
Run:  python make_walkthrough.py   (needs Pillow), then compile myThesis.tex
"""
from pathlib import Path
from PIL import Image

HERE = Path(__file__).parent
SRC = HERE / "img" / "screens"      # 1800 px wide originals (emails already blurred)
OUT = HERE / "img" / "wt"
TEX = HERE / "tex" / "walkthrough.tex"

GAP = 0.03          # gap between the two pictures in a row, as a share of the line width
MAX_H_CM = 6.4      # tallest a row may be
PHONE_H_CM = 5.2    # the two phone screenshots are tall and narrow, so cap them lower
TEXTWIDTH_CM = 15.9

# name: (source file, crop box in source pixels, caption)
S = {
    "p01": ("p01-home", None, "Home page; ``Ask Sarabo'' opens the AI support chat."),
    "p02": ("p02-services", (150, 150, 1650, 950), "Services and prices: the live catalogue of 45 services."),
    "p03": ("p03-areas-search", None, "Service areas: searching ``Ambarkhana'' zooms to that part of Sylhet (Section~\\ref{sec:areamap})."),
    "p05": ("p05-ai-chat", (1240, 0, 1800, 700), "AI support chat: price and 200\\,BDT fee taken from the live catalogue (Chapter~\\ref{ch:ai})."),
    "p04": ("p04-jobs", (180, 160, 1620, 1125), "Public jobs board: a safe summary of each open job, no customer details."),
    "p06": ("p06-tracking", (180, 100, 1620, 1125), "Public tracking of the walkthrough repair: stages and times only."),
    "p08": ("p08-mob-home", None, "Home page on a phone (393\\,px wide)."),
    "p09": ("p09-mob-jobs", None, "Jobs board on a phone."),
    "c02": ("c02-ai-helper", (360, 234, 1764, 774), "AI request helper: Banglish text turned into device, service and an English description; \\emph{Undo} restores the form."),
    "c03": ("c03-location-pickup", (200, 140, 1680, 1050), "Address and a two-hour pickup window (Friday closed)."),
    "c04": ("c04-created", (140, 117, 1740, 1026), "Request created; photos are sent only when the customer presses ``Upload''."),
    "t03": ("t03-offer", (1106, 0, 1800, 1000), "Technician's offer: price guide, minimum fee, and an AI-written note from a few words."),
    "c06": ("c06-offers", (140, 480, 1320, 905), "The offer with its ranking reasons (Section~\\ref{sec:ranking})."),
    "c07": ("c07-choose", (600, 320, 1200, 800), "Choosing the offer: pay the inspection fee to book."),
    "c08": ("c08-stripe", (250, 30, 1500, 1080), "Stripe Checkout in test mode for the 200\\,BDT fee."),
    "c09": ("c09-booked", (130, 170, 1760, 760), "Technician booked; the fee counts toward the final price."),
    "t05": ("t05-pickup-condition", (600, 260, 1200, 865), "Device condition and accessories recorded at pickup."),
    "t06": ("t06-inspection", (350, 470, 1340, 1110), "Inspection: findings, issues and a repairability decision."),
    "t07": ("t07-quote", (350, 430, 1340, 1110), "Itemised quote: 800 + 3,200 = 4,000\\,BDT, with the 10\\% commission shown."),
    "c10": ("c10-quote", (140, 480, 1320, 1125), "The customer's view: 200\\,BDT already paid, 3,800 left to pay."),
    "c12": ("c12-payment-success", (620, 190, 1260, 830), "Payment successful, with a PDF receipt."),
    "c13": ("c13-payment-history", (130, 100, 1760, 900), "Payment history: the repair payment and the inspection fee."),
    "t08": ("t08-progress", (350, 470, 1340, 1000), "Repair in progress, with updates the customer sees."),
    "t09": ("t09-complete", (350, 60, 1320, 960), "Completing the repair; ``Can't finish'' would go to an admin."),
    "c14": ("c14-confirm-receipt", (130, 470, 1310, 1000), "Confirm receipt, or ``I haven't received it''; auto-confirmed after 3 days."),
    "c15": ("c15-review", (560, 190, 1240, 935), "Rating the technician."),
    "c16": ("c16-warranty-claim", (560, 130, 1240, 1000), "Reporting a problem under the 30-day warranty."),
    "t11": ("t11-warranty-book", (600, 295, 1205, 835), "Technician books the free re-inspection (within 3 days)."),
    "c17": ("c17-warranty-resolved", (140, 500, 1320, 1100), "The resolved claim: re-inspection, ``Covered'', re-repair and the customer's ``Working now''."),
    "t13": ("t13-wallet", (360, 229, 1764, 1003), "Wallet: the 3,600\\,BDT earning requested as a bKash withdrawal."),
    "t14": ("t14-profile-edit", (1080, 0, 1800, 1125), "Technician edits own details; the area is locked during a repair."),
    "a01": ("a01-overview", (360, 234, 1764, 1000), "Admin overview: missed pickups, no offers, stalled repairs first."),
    "a05": ("a05-technicians", (350, 100, 1770, 1000), "Technician applications and approved technicians."),
    "a06": ("a06-catalogue", (350, 100, 1770, 1000), "Services and prices editor."),
    "a07": ("a07-service-editor", (1060, 0, 1800, 1125), "Editing a service: a price change creates a new version."),
    "a08": ("a08-reports", (350, 100, 1700, 880), "Reports with the AI summary; unverifiable numbers are removed."),
    "a09": ("a09-reports-charts", None, "Report charts: requests over time and demand by region."),
    "a10": ("a10-mark-paid", (600, 180, 1200, 950), "Recording a bKash payout with its TrxID (test value)."),
    "a11": ("a11-reviews", (350, 100, 1770, 1000), "Technician reviews, which admins can hide or restore."),
}

SECTIONS = [
    ("Public Website", "Anyone can see services, prices, areas, open jobs and tracking without an account.",
     [["p01", "p02"], ["p03", "p05"], ["p04", "p06"], ["p08", "p09"]]),
    ("Request and Offer", "Rahim describes the problem in Banglish; a local technician sends an offer.",
     [["c02", "c03"], ["c04", "t03"]]),
    ("Choosing and Booking", "The customer compares offers and pays the inspection fee to book the visit.",
     [["c06", "c07"], ["c08", "c09"]]),
    ("Pickup, Inspection and Quote", "The technician records the condition, inspects the phone and sends an itemised quote.",
     [["t05", "t06"], ["t07", "c10"]]),
    ("Payment, Repair and Hand-Over", "The customer pays the rest; the technician repairs and returns the phone.",
     [["c12", "c13"], ["t08", "t09"], ["c14", "c15"]]),
    ("Warranty", "Ten days later the touch fails again, and the warranty covers it.",
     [["c16", "t11"], ["c17"]]),
    ("Technician Wallet and Profile", None, [["t13", "t14"]]),
    ("Admin", "Admins see what needs attention, manage technicians and prices, and read reports.",
     [["a01", "a05"], ["a06", "a07"], ["a08", "a09"], ["a10", "a11"]]),
]


def crop_all():
    OUT.mkdir(exist_ok=True)
    aspect = {}
    for key, (src, box, _) in S.items():
        im = Image.open(SRC / f"{src}.jpg").convert("RGB")
        if box:
            im = im.crop(box)
        im.save(OUT / f"{key}.jpg", quality=85, optimize=True, progressive=True)
        aspect[key] = im.width / im.height
    return aspect


def row_tex(keys, aspect):
    n = len(keys)
    usable = 1 - GAP * (n - 1)
    total = sum(aspect[k] for k in keys)
    phones = all(aspect[k] < 0.8 for k in keys)
    h_cm = min(usable * TEXTWIDTH_CM / total, PHONE_H_CM if phones else MAX_H_CM)
    parts = []
    for k in keys:
        w = h_cm * aspect[k] / TEXTWIDTH_CM  # picture width as a share of \linewidth
        box = max(w, 0.36) if phones else w  # the narrow phone pictures get a wider caption box
        cap = S[k][2]
        parts.append(
            f"\\begin{{minipage}}[t]{{{box:.3f}\\linewidth}}\\centering"
            f"{{\\setlength{{\\fboxsep}}{{0pt}}\\fbox{{\\includegraphics[width={w / box:.3f}\\linewidth]{{img/wt/{k}}}}}}}"
            f"\\caption{{{cap}}}\\label{{fig:wt-{k}}}\\end{{minipage}}")
    # normal floats (not [H]) so LaTeX can fill each page; their order is kept
    return "\\begin{figure}[!htbp]\\centering\n" + "\\hfill\n".join(parts) + "\n\\end{figure}\n"


def main():
    aspect = crop_all()
    out = [r"""\documentclass{standalone}
\usepackage{standalone}

\begin{document}
\chapter{System Walkthrough}
\label{ch:walkthrough}

These screenshots were taken on 14 October 2026 from the final code, running locally with real Firebase sign-in, real Gemini answers and Stripe in test mode. From Section~\ref{sec:wt-request} on they follow \emph{one} repair from start to finish, the cracked Samsung Galaxy A54 used throughout this report, switching between the customer's and the technician's screens, so every state in Figure~\ref{fig:e2e} appears in order. Each picture is cropped to the part that matters; other rows in lists come from the seeded development data, and personal email addresses are blurred.
"""]
    for title, intro, rows in SECTIONS:
        label = {"Request and Offer": r"\label{sec:wt-request}", "Warranty": r"\label{sec:wt-warranty}"}.get(title, "")
        # finish the previous section's pictures before the next heading
        # and never leave a heading at the foot of a page without room for a row of pictures
        out.append(f"\n\\FloatBarrier\n\\needspace{{9\\baselineskip}}\n\\section{{{title}}}{label}\n")
        if intro:
            out.append(intro + "\n\n")
        for keys in rows:
            out.append(row_tex(keys, aspect))
    out.append("\n\\FloatBarrier\n\\end{document}\n")
    TEX.write_text("".join(out), encoding="utf-8")
    print("figures:", sum(len(r) for _, _, rows in SECTIONS for r in rows))


if __name__ == "__main__":
    main()
