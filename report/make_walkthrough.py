"""Builds Chapter 7 (tex/walkthrough.tex) and its screenshots (img/wt/).

21 key screens, each shown whole (the full browser window, no cropping) at the full
text width, with a caption of two or three sentences that explains the screen. The
List of Figures uses the short title before the colon-free long caption.
Run:  py make_walkthrough.py   (needs Pillow), then compile myThesis.tex
"""
from pathlib import Path
from PIL import Image

HERE = Path(__file__).parent
SRC = HERE / "img" / "screens"      # 1800 x 1125 originals (emails already blurred)
OUT = HERE / "img" / "wt"
TEX = HERE / "tex" / "walkthrough.tex"

# name: (source file, short title for the List of Figures, full caption)
S = {
    "p03": ("p03-areas-search", "Service areas map",
            "Service areas page, open to everyone. Searching ``Ambarkhana'' moves the OpenStreetMap map to that part of Sylhet, and the card at the bottom left lists the other covered sub-areas of the city with a direct ``Request a repair'' button. A visitor can check that Sarabo serves their address before creating an account (Section~\\ref{sec:areamap})."),
    "p05": ("p05-ai-chat", "AI support chat",
            "The AI support chat (``Ask Sarabo''), opened over the home page. A visitor asks what a cracked phone screen costs; the answer quotes the 1,500--6,000\\,BDT estimate and the 200\\,BDT inspection fee taken from the live catalogue and explains the steps. The two buttons under the answer come from a fixed list, and a notice warns users not to share passwords or card details (Chapter~\\ref{ch:ai})."),
    "p04": ("p04-jobs", "Public jobs board",
            "The public jobs board lists every open repair job, with search, region, device and repair filters and a ``No offers yet'' shortcut. Each card shows only a safe summary (device, repair, district, pickup day, usual price and number of offers) and never the customer's name, address or contact details. Technicians sign in from the banner to see the full job and send an offer."),
    "c02": ("c02-ai-helper", "AI request helper",
            "Step one of the customer's request form with the AI request helper. Rahim typed the problem in Banglish (``the phone fell from my hand, the screen cracked, a green line, touch not working''); ``Fill the form for me'' set the device, the catalogue service ``Screen Replacement -- Mobile Phone'', the brand, the model and an English description. The summary on the right already shows the 1,500--6,000\\,BDT estimate, and ``Undo'' restores the previous values."),
    "c03": ("c03-location-pickup", "Pickup address and time",
            "Steps three and four of the request form: the pickup address (region, district and street address) and a two-hour pickup window. Friday is shown as closed, and each window shows whether it is still available. The summary on the right now holds every detail of the request, and no payment is needed to submit it."),
    "t03": ("t03-offer", "Technician sends an offer",
            "A technician applying for Rahim's job from the jobs board. The grey box is the price guide, built from 7 recent offers for the same repair, next to Sarabo's listed price; the technician enters an estimate of 3,500--5,000\\,BDT and a 200\\,BDT inspection fee within the allowed range. The note was written by AI (``Write it for me'') from a few words, and can be edited before it is sent."),
    "c06": ("c06-offers", "Offer seen by the customer",
            "Rahim's request page after the offer arrives. The progress bar at the top shows the request is still at the first stage, and the ``Your next step'' panel asks him to choose a technician. The offer shows its ranking reasons (12 repairs with no missed pickups, in the same district, usually replies in 2 minutes), the rating, level, experience, estimate, fee and note, with ``Choose'' and ``Reject'' buttons (Section~\\ref{sec:ranking})."),
    "c07": ("c07-choose", "Choosing an offer",
            "The confirmation shown when Rahim chooses the offer. It repeats the estimate and the 200\\,BDT inspection fee and explains that paying the fee books the visit and closes the other offers. ``Pay 200\\,BDT and book'' opens Stripe Checkout (test mode); if the booking fails after payment the fee is refunded automatically."),
    "t05": ("t05-pickup-condition", "Device condition at pickup",
            "The technician's view at pickup. Before taking the phone, the technician writes down its condition (a cracked screen, a green line, touch not responding, a small scratch on the back) and the accessories taken (phone only). The customer sees this record on his request and can dispute it, which protects both sides if there is a disagreement later."),
    "t06": ("t06-inspection", "Inspection report",
            "The inspection step on the technician's job page, after the device was collected. The technician records what was found (a cracked AMOLED panel and a damaged touch layer, with the battery, charging port and mainboard working) and lists each issue with a severity. The customer sees these findings next to the quote."),
    "t07": ("t07-quote", "Writing the quote",
            "The technician writes an itemised quote: 800\\,BDT labour and 3,200\\,BDT parts, 4,000\\,BDT in total. The box below shows the 10\\% platform commission (400\\,BDT) and the 3,600\\,BDT the technician will receive, and the note tells the customer what the price includes. Sarabo checks the final amounts from these line items on the server."),
    "c10": ("c10-quote", "Customer reviews the quote",
            "Rahim's view of the quote. The progress bar has moved to ``Approve'', and the panel lists labour, parts and extra charges with the 4,000\\,BDT total and the technician's notes. Below, the 200\\,BDT inspection fee he already paid is taken off the final price; nothing is charged until he approves."),
    "c12": ("c12-payment-success", "Payment successful",
            "The page shown after Rahim pays the remaining 3,800\\,BDT (4,000\\,BDT minus the 200\\,BDT fee) through Stripe. It shows the Stripe transaction ID and the request's tracking code, and ``Download receipt (PDF)'' gives a receipt created by the server. The buttons lead to his repairs, his payment history or the dashboard."),
    "t09": ("t09-complete", "Completing the repair",
            "The technician's job page while the repair is in progress. Progress updates (top) are shown to the customer as they are added; ``Ready to finish?'' takes a description of the work done and up to three optional photos before ``Mark repair complete''. The condition recorded at pickup stays visible at the bottom, and the right-hand panel shows the request is paid."),
    "c14": ("c14-confirm-receipt", "Confirming receipt",
            "Rahim's request page after the technician marked the phone as returned. All four stages are complete, and he is asked to confirm he has the device; if he does nothing it is confirmed automatically after 3 days (17 October). ``That's not right'' and ``I haven't received it'' send the case to an admin, and the technician's earning only becomes available after confirmation."),
    "c16": ("c16-warranty-claim", "Warranty claim",
            "Ten days later the touch fails again, so Rahim reports a problem under the 30-day warranty. The dialog states what is covered (the same fault coming back or a fitted part failing) and what is not (new damage, water or a drop); he chooses ``A replaced part stopped working'', describes the problem and can add up to four photos. The warranty card behind it shows the cover lasts until 13 November."),
    "c17": ("c17-warranty-resolved", "Resolved warranty claim",
            "The warranty claim after it was resolved, as Rahim sees it. It records each step in order: the free re-inspection appointment, the technician's decision (``Covered'', because the faulty part was the one he fitted), the re-repair, and Rahim's answer ``Working now''. Each step had a deadline, and an admin could have taken the claim over if one was missed."),
    "t13": ("t13-wallet", "Technician wallet",
            "The technician's wallet. The large number is the money available to withdraw (earnings from repairs the customer confirmed, plus inspection fees kept); the cards below show pending money, the withdrawal in progress and the total paid out. The 3,600\\,BDT from this repair has been requested as a bKash withdrawal and waits for an admin."),
    "a01": ("a01-overview", "Admin operations overview",
            "The admin's home page, ``Operations''. The yellow ``Needs you'' box counts the urgent problems first (missed pickups, overdue pickups, requests with no offers, stalled repairs and requests no local technician can take); each count opens its list, already filtered. Below are the counts of work waiting and the most urgent items, with the oldest first. (Most numbers come from the seeded development data.)"),
    "a08": ("a08-reports", "Admin reports with AI summary",
            "The admin Reports page for the last 30 days. The AI summary at the top (a headline, highlights and ``What to do'') is written by Google Gemini only from the numbers on the page, and any sentence with a number that is not in the data is removed. Below it, the overview compares this period with the previous one; charts for regions, devices and pickups follow further down."),
    "a10": ("a10-mark-paid", "Recording a bKash payout",
            "An admin recording the technician's withdrawal as paid. Sarabo does not send money itself: the admin sends 3,600\\,BDT to the technician's bKash number with the bKash app, then enters the TrxID from the bKash confirmation (here a test value). A TrxID can be used only once, and the record cannot be undone."),
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


def copy_all():
    OUT.mkdir(exist_ok=True)
    for old in OUT.glob("*.jpg"):
        old.unlink()
    for key, (src, _, _) in S.items():
        im = Image.open(SRC / f"{src}.jpg").convert("RGB")   # the whole screen, not cropped
        im.save(OUT / f"{key}.jpg", quality=88, optimize=True, progressive=True)


def figure_tex(key):
    _, short, caption = S[key]
    # single-spaced caption, like the tables, so two screenshots fit on a page
    return (f"\\begin{{figure}}[!htbp]\\renewcommand{{\\baselinestretch}}{{1.0}}\\selectfont\\centering"
            f"{{\\setlength{{\\fboxsep}}{{0pt}}\\fbox{{\\includegraphics[width=\\dimexpr\\linewidth-0.6pt\\relax]{{img/wt/{key}}}}}}}"
            f"\\caption[{short}]{{{caption}}}\\label{{fig:wt-{key}}}\\end{{figure}}\n")


def main():
    copy_all()
    out = [r"""\documentclass{standalone}
\usepackage{standalone}

\begin{document}
\chapter{System Walkthrough}
\label{ch:walkthrough}

The screenshots below were taken on 14 October 2026 from the final code, with real Firebase sign-in, real Gemini answers and Stripe in test mode. From Section~\ref{sec:wt-request} they follow \emph{one} repair, the cracked Samsung Galaxy A54 used throughout this report, through every state in Figure~\ref{fig:e2e}. Each picture shows the whole browser window as the user saw it, at the full width of the page; personal email addresses are blurred.

% a page holding only a screenshot starts it at the top of the page, not in the middle
\makeatletter\setlength{\@fptop}{0pt}\setlength{\@fpbot}{0pt plus 1fil}\makeatother
"""]
    for title, intro, keys in SECTIONS:
        label = {"Request and Offer": r"\label{sec:wt-request}", "Warranty": r"\label{sec:wt-warranty}"}.get(title, "")
        # finish the previous section's pictures first, and keep each heading with room below it
        out.append(f"\n\\FloatBarrier\n\\needspace{{9\\baselineskip}}\n\\section{{{title}}}{label}\n{intro}\n\n")
        for k in keys:
            out.append(figure_tex(k))
    out.append("\n\\FloatBarrier\n"
               "\\makeatletter\\setlength{\\@fptop}{0pt plus 1fil}\\setlength{\\@fpbot}{0pt plus 1fil}\\makeatother\n"
               "\\end{document}\n")
    TEX.write_text("".join(out), encoding="utf-8")
    print("figures:", sum(len(k) for _, _, k in SECTIONS))


if __name__ == "__main__":
    main()
