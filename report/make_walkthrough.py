"""Builds Chapter 7 (tex/walkthrough.tex) and its cropped screenshots (img/wt/).

About 20 key screens, one per row at full text width, each cropped tightly to the
part that matters so that the text inside prints at roughly 7-8 pt on A4.
Run:  python make_walkthrough.py   (needs Pillow), then compile myThesis.tex
"""
from pathlib import Path
from PIL import Image

HERE = Path(__file__).parent
SRC = HERE / "img" / "screens"      # 1800 px wide originals (emails already blurred)
OUT = HERE / "img" / "wt"
TEX = HERE / "tex" / "walkthrough.tex"

TEXTWIDTH_CM = 15.9
MAX_H_CM = 8.6      # tall, narrow screens (dialogs, the chat) are limited by height instead

# name: (source file, crop box in source pixels, caption)
S = {
    "p03": ("p03-areas-search", (0, 330, 1100, 1125), "Service areas: searching ``Ambarkhana'' zooms the map to that part of Sylhet (Section~\\ref{sec:areamap})."),
    "p05": ("p05-ai-chat", (1240, 0, 1800, 700), "AI support chat: the price and the 200\\,BDT fee come from the live catalogue (Chapter~\\ref{ch:ai})."),
    "p04": ("p04-jobs", (180, 520, 1180, 1125), "Public jobs board: a safe summary of each open job, with no customer details."),
    "c02": ("c02-ai-helper", (360, 234, 1340, 774), "AI request helper: the Banglish text became the device, the catalogue service and an English description."),
    "c03": ("c03-location-pickup", (200, 140, 1220, 1050), "Address and a two-hour pickup window (Friday closed)."),
    "t03": ("t03-offer", (1106, 90, 1800, 760), "Technician's offer: price guide, minimum fee, and a note written by AI from a few words."),
    "c06": ("c06-offers", (250, 640, 1290, 895), "The offer as the customer sees it, with its ranking reasons (Section~\\ref{sec:ranking})."),
    "c07": ("c07-choose", (600, 320, 1200, 800), "Choosing the offer: the inspection fee is paid by Stripe (test mode) to book the visit."),
    "t05": ("t05-pickup-condition", (600, 260, 1200, 865), "The device's condition and accessories recorded at pickup."),
    "t06": ("t06-inspection", (350, 470, 1340, 1110), "Inspection: findings, issues and a repairability decision."),
    "t07": ("t07-quote", (350, 430, 1340, 1110), "Itemised quote (800 + 3,200 = 4,000\\,BDT), with the 10\\% commission shown."),
    "c10": ("c10-quote", (250, 600, 1290, 1125), "The customer's view of the quote: nothing is charged before approval."),
    "c12": ("c12-payment-success", (620, 190, 1260, 830), "Payment successful (3,800\\,BDT after the 200\\,BDT fee), with a PDF receipt."),
    "t09": ("t09-complete", (350, 60, 1320, 960), "Completing the repair; ``Can't finish this repair'' would send it to an admin."),
    "c14": ("c14-confirm-receipt", (130, 470, 1300, 1000), "Confirm receipt, or ``I haven't received it''; confirmed automatically after 3 days."),
    "c16": ("c16-warranty-claim", (560, 130, 1240, 1000), "Reporting a problem under the 30-day warranty."),
    "c17": ("c17-warranty-resolved", (171, 693, 1283, 1022), "The resolved claim: free re-inspection, ``Covered'', re-repair and the customer's ``Working now''."),
    "t13": ("t13-wallet", (360, 229, 1764, 1003), "Technician wallet: the 3,600\\,BDT earning requested as a bKash withdrawal."),
    "a01": ("a01-overview", (360, 300, 1764, 700), "Admin overview: missed pickups, requests without offers and stalled repairs come first."),
    "a08": ("a08-reports", (360, 330, 1500, 800), "Admin reports with the AI summary; sentences with numbers not in the data are removed."),
    "a10": ("a10-mark-paid", (600, 180, 1200, 950), "Recording a bKash payout with its TrxID (a test value)."),
}

SECTIONS = [
    ("Public Website", "Anyone can browse services, prices, service areas, open jobs and tracking without an account.",
     ["p03", "p05", "p04"]),
    ("Request and Offer", "Rahim describes the problem in Banglish and books a pickup; a local technician sends an offer.",
     ["c02", "c03", "t03"]),
    ("Choosing and Booking", "He compares offers and pays the inspection fee to book the visit.",
     ["c06", "c07"]),
    ("Pickup, Inspection and Quote", "The technician records the condition, inspects the phone and sends an itemised quote.",
     ["t05", "t06", "t07", "c10"]),
    ("Payment, Repair and Hand-Over", "Rahim pays the rest; the technician repairs and returns the phone.",
     ["c12", "t09", "c14"]),
    ("Warranty", "Ten days later the touch fails again, and the warranty covers it.",
     ["c16", "c17"]),
    ("Technician and Admin", "The technician withdraws the earning; the admin sees what needs attention and records the payout.",
     ["t13", "a01", "a08", "a10"]),
]


def crop_all():
    OUT.mkdir(exist_ok=True)
    for old in OUT.glob("*.jpg"):
        old.unlink()
    aspect = {}
    for key, (src, box, _) in S.items():
        im = Image.open(SRC / f"{src}.jpg").convert("RGB")
        if box:
            im = im.crop(box)
        im.save(OUT / f"{key}.jpg", quality=88, optimize=True, progressive=True)
        aspect[key] = im.width / im.height
    return aspect


def figure_tex(key, aspect):
    w = min(1.0, MAX_H_CM * aspect[key] / TEXTWIDTH_CM)   # share of \linewidth
    return (f"\\begin{{figure}}[!htbp]\\centering"
            f"{{\\setlength{{\\fboxsep}}{{0pt}}\\fbox{{\\includegraphics[width={w:.3f}\\linewidth]{{img/wt/{key}}}}}}}"
            f"\\caption{{{S[key][2]}}}\\label{{fig:wt-{key}}}\\end{{figure}}\n")


def main():
    aspect = crop_all()
    out = [r"""\documentclass{standalone}
\usepackage{standalone}

\begin{document}
\chapter{System Walkthrough}
\label{ch:walkthrough}

The screenshots below were taken on 14 October 2026 from the final code, with real Firebase sign-in, real Gemini answers and Stripe in test mode. From Section~\ref{sec:wt-request} they follow \emph{one} repair, the cracked Samsung Galaxy A54 used throughout this report, through every state in Figure~\ref{fig:e2e}. Each picture shows only the part of the screen that matters; personal email addresses are blurred.
"""]
    for title, intro, keys in SECTIONS:
        label = {"Request and Offer": r"\label{sec:wt-request}", "Warranty": r"\label{sec:wt-warranty}"}.get(title, "")
        # finish the previous section's pictures first, and keep each heading with room below it
        out.append(f"\n\\FloatBarrier\n\\needspace{{9\\baselineskip}}\n\\section{{{title}}}{label}\n{intro}\n\n")
        for k in keys:
            out.append(figure_tex(k, aspect))
    out.append("\n\\FloatBarrier\n\\end{document}\n")
    TEX.write_text("".join(out), encoding="utf-8")
    print("figures:", sum(len(k) for _, _, k in SECTIONS))


if __name__ == "__main__":
    main()
