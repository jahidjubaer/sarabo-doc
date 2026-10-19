"""Builds Chapter 7 (tex/walkthrough.tex) and its screenshots (img/wt/).

All 52 screenshots taken on 14 October 2026, each shown whole (the full browser window,
no cropping) at the full text width, with a caption of two or three sentences. The two
phone screenshots share one figure, side by side. The List of Figures uses the short
title of each figure.
Run:  py make_walkthrough.py   (needs Pillow), then compile myThesis.tex
"""
from pathlib import Path
from PIL import Image, ImageFilter

HERE = Path(__file__).parent
SRC = HERE / "img" / "screens"      # originals (most emails already blurred)
OUT = HERE / "img" / "wt"
TEX = HERE / "tex" / "walkthrough.tex"

FIG_H = 0.38     # screenshot height as a share of the text height: two per page

# personal email addresses still readable at the edge of a screenshot: (left, top, right, bottom)
BLUR = {
    "c13": [(930, 1095, 1180, 1125)],
    "a02": [(1235, 1095, 1440, 1125)],
    "t14": [(1010, 920, 1082, 960)],
}

# key: (source file, short title for the List of Figures, full caption)
S = {
    # --- public website
    "p01": ("p01-home", "Home page",
            "The public home page, which is the first screen a visitor sees. The banner sums up what the service promises (approved technicians, an itemised quote before any work starts, and every step tracked) and offers the two main actions, ``Find a repair service'' and ``Track a repair''. The top bar links to services, service areas, tracking and the about page. On every page, the ``Ask Sarabo'' button in the corner opens the AI support chat."),
    "p02": ("p02-services", "Services and prices",
            "The Services page, which anyone can open without an account. Repairs are grouped by device (laptop, other electronics, smartphone, television and more below), and each card shows the lowest catalogue price and how many repairs are listed for that device. The prices come from the live catalogue of 45 services that admins maintain, and the exact price is always confirmed in an itemised quote after inspection."),
    "p03": ("p03-areas-search", "Service areas map",
            "The Service areas page. Searching ``Ambarkhana'' moves the OpenStreetMap map to that part of Sylhet, and the card at the bottom left lists the other covered sub-areas of the city with a direct ``Request a repair'' button. A visitor can check that Sarabo serves their address before creating an account (Section~\\ref{sec:areamap})."),
    "p05": ("p05-ai-chat", "AI support chat",
            "The AI support chat (``Ask Sarabo''), opened over the home page. A visitor asks what it costs to fix a cracked phone screen. The answer gives the 1,500--6,000\\,BDT estimate and the 200\\,BDT inspection fee from the live catalogue and explains the steps. The two buttons under the answer come from a fixed list, and a notice warns users not to share passwords or card details (Chapter~\\ref{ch:ai})."),
    "p04": ("p04-jobs", "Public jobs board",
            "The public jobs board lists every open repair job, with search, region, device and repair filters and a ``No offers yet'' shortcut. Each card shows only a summary with nothing private in it (device, repair, district, pickup day, usual price and number of offers), never the customer's name, address or contact details. Technicians sign in from the banner to see the whole job and send an offer."),
    "p06": ("p06-tracking", "Public tracking page",
            "The public tracking page for the walkthrough repair, opened with just its tracking code and no account. It shows only the four stages (all complete here), the current status, the last update time and a time-stamped list of updates. Personal and payment details are hidden, and the owner can sign in from the button on the right to see the full record."),
    "mob": (None, "Home page and jobs board on a phone",
            "The same public pages on a phone, 393 pixels wide: the home page (left) and the jobs board (right). The layout changes for small screens: the menu folds into the button at the top left, the main actions become full-width buttons, and the job filters move behind a ``Filters'' button. Every page in this chapter works the same way on a phone."),
    # --- creating the request
    "c01": ("c01-overview", "Customer overview",
            "The customer's dashboard after signing in. ``Needs you'' comes first and lists the requests that are waiting on the customer (here, two requests with an offer waiting), each with a button for the next action. Below it, ``In progress'' shows every other open request with the four-stage progress bar. ``New request'' at the top right starts the request form."),
    "c02": ("c02-ai-helper", "AI request helper",
            "Step one of the request form with the AI request helper. Rahim typed the problem in Banglish (``the phone fell from my hand, the screen cracked, a green line, touch not working''). Pressing ``Fill the form for me'' set the device, the catalogue service ``Screen Replacement -- Mobile Phone'', the brand, the model and an English description. The summary on the right already shows the 1,500--6,000\\,BDT estimate, and ``Undo'' restores the previous values."),
    "c03": ("c03-location-pickup", "Pickup address and time",
            "Steps three and four of the request form: the pickup address (region, district and street address) and a two-hour pickup window. Friday is shown as closed, and each window shows whether it is still available. The summary on the right now holds every detail of the request, and no payment is needed to submit it."),
    "c04": ("c04-created", "Request created",
            "The confirmation after the request is submitted. It repeats the device, repair and estimate, the service address, the pickup window and the problem description, and offers to add up to three damage photos now or later. The request goes out to matching technicians straight away. Photos are optional, and they are sent only when the customer presses ``Upload''."),
    # --- offers
    "t02": ("t02-jobs", "Jobs board for a technician",
            "The jobs board as a signed-in technician sees it. Beside the search and the region, device and repair filters, the shortcuts ``No offers yet'', ``Not applied'' and ``My offers'' help the technician find work. Jobs they have already made an offer on carry an ``Offer sent'' badge and show that offer. Rahim's new Samsung job is first, posted ``Just now'', with its pickup window and usual price."),
    "t03": ("t03-offer", "Technician sends an offer",
            "A technician applying for Rahim's job. The grey box is the price guide, built from 7 recent offers for the same repair and shown next to Sarabo's listed price. The technician enters an estimate of 3,500--5,000\\,BDT and a 200\\,BDT inspection fee, which is within the allowed range. The AI wrote the note from a few words (``Write it for me''), and the technician can edit it before sending."),
    "c05": ("c05-my-requests", "My repairs list",
            "The customer's ``My repairs'' page, with search, sorting and status tabs (All, Needs you, In progress, Completed, Cancelled) and a count on each. Rahim's Samsung Galaxy A54 is at the top, marked ``1 offer waiting'' and with a ``Choose a technician'' button. Completed repairs show the agreed price instead."),
    "c06": ("c06-offers", "Offer seen by the customer",
            "Rahim's request page after the offer arrives. The progress bar at the top shows the request is still at the first stage, and the ``Your next step'' panel asks him to choose a technician. The offer shows why it is ranked where it is (12 repairs with no missed pickups, in the same district, usually replies in 2 minutes), along with the rating, level, experience, estimate, fee and note, and ``Choose'' and ``Reject'' buttons (Section~\\ref{sec:ranking})."),
    # --- choosing and booking
    "c07": ("c07-choose", "Choosing an offer",
            "The confirmation Rahim sees when he chooses the offer. It repeats the estimate and the 200\\,BDT inspection fee and explains that paying the fee books the visit and closes the other offers. ``Pay 200\\,BDT and book'' opens Stripe Checkout. If the booking fails after he has paid, the fee is refunded automatically."),
    "c08": ("c08-stripe", "Stripe Checkout for the inspection fee",
            "Stripe's hosted checkout page for the 200\\,BDT inspection fee, in test mode (the ``Sandbox'' badge). The left side names the item (``Inspection visit: Samsung Galaxy A54'') and says the fee counts toward the final price. The card shown is Stripe's public test card. Card details are typed only on Stripe's page and never reach Sarabo's server."),
    "c09": ("c09-booked", "Technician booked",
            "Rahim's request after the fee is paid. The progress bar has moved to ``Inspect'' with the status ``Technician assigned'', and the panel says nothing is needed from him while the technician arranges the pickup. It also confirms that the 200\\,BDT fee counts toward the final price. ``Cancel visit'' follows the cancellation rules in Table~\\ref{tab:feeoutcomes}, and ``Change'' on the right moves the pickup window."),
    # --- pickup, inspection and quote
    "t04": ("t04-assigned", "Technician's assigned jobs",
            "The technician's ``Assigned jobs'' list, with search, ``Most urgent first'' sorting and tabs for jobs that need the technician, are in repair, are waiting or are completed. Rahim's job shows the pickup window and the tracking code, and the next action sits on the job itself. ``Start pickup'' tells the customer that the technician is on the way."),
    "t05": ("t05-pickup-condition", "Device condition at pickup",
            "The technician's view at pickup. Before taking the phone, the technician writes down its condition (a cracked screen, a green line, touch not responding, a small scratch on the back) and the accessories taken (phone only). The customer sees this record on his request and can dispute it, which protects both sides if there is a disagreement later (Section~\\ref{sec:nostuck})."),
    "t06": ("t06-inspection", "Inspection report",
            "The inspection step on the technician's job page, after the device was collected. The technician records what was found (a cracked AMOLED panel and a damaged touch layer, with the battery, charging port and mainboard working) and lists each issue with a severity. The customer sees these findings next to the quote. If the result had been ``not repairable'' or ``not economical'', either side could have closed the request."),
    "t07": ("t07-quote", "Writing the quote",
            "The technician writes an itemised quote: 800\\,BDT labour and 3,200\\,BDT parts, 4,000\\,BDT in total. The box below shows the 10\\% platform commission (400\\,BDT) and the 3,600\\,BDT the technician will receive, and the note tells the customer what the price includes. The server works out the final amounts from these line items itself."),
    "c10": ("c10-quote", "Customer reviews the quote",
            "Rahim's view of the quote. The progress bar has moved to ``Approve'', and the panel lists labour, parts and extra charges with the 4,000\\,BDT total and the technician's notes. Below that, the 200\\,BDT inspection fee he already paid is taken off the final price. Nothing is charged until he approves."),
    # --- payment
    "c11": ("c11-approve-pay", "Approving and paying the quote",
            "Rahim approves the quote. Behind the dialog, the price summary shows the 4,000\\,BDT final price minus the 200\\,BDT already paid, which leaves 3,800\\,BDT. The dialog repeats that amount and says the repair will start once it is paid. ``Approve and pay'' goes straight to a Stripe card payment, and ``That's not right'' on the page lets him dispute the pickup record instead."),
    "c12": ("c12-payment-success", "Payment successful",
            "The page shown after Rahim pays the remaining 3,800\\,BDT through Stripe. It shows the Stripe transaction ID and the request's tracking code, and ``Download receipt (PDF)'' gives him a receipt generated by the server. The buttons take him to his repairs, his payment history or the dashboard."),
    "c13": ("c13-payment-history", "Payment history",
            "The customer's Payment History, newest first. The walkthrough repair has two rows: the 3,800\\,BDT repair payment and, below it, the 200\\,BDT inspection fee, each with the tracking code, the Stripe transaction ID, the time and a PDF receipt. The other rows are from earlier test repairs."),
    # --- repair and hand-over
    "t08": ("t08-progress", "Repair in progress",
            "The technician's job page once the customer has paid. The progress bar is at the last stage, ``Repaired -- repair in progress'', and the panel asks the technician to post updates and finish the repair. Rahim can already see the first update (old display removed, new original display fitted and tested) with its time."),
    "t09": ("t09-complete", "Completing the repair",
            "The same page further down, when the work is done. Under ``Ready to finish?'' the technician describes the work done and can add up to three completion photos before pressing ``Mark repair complete''. The condition recorded at pickup stays visible at the bottom, and the right-hand panel shows the request is paid."),
    "t10": ("t10-returned", "Marking the device returned",
            "After returning the phone, the technician marks it returned. The dialog explains that the customer is asked to confirm, and that if he does not answer within 3 days it is confirmed automatically, which also makes the technician's money available. This way, no step of the repair can be left stuck waiting for one person."),
    "c14": ("c14-confirm-receipt", "Confirming receipt",
            "Rahim's request page after the technician marked the phone as returned. All four stages are complete, and he is asked to confirm that he has the device. If he does nothing, it is confirmed automatically after 3 days (17 October). ``That's not right'' and ``I haven't received it'' send the case to an admin. The technician's earning only becomes available after confirmation."),
    "c15": ("c15-review", "Rating the technician",
            "Once the device is back, Rahim rates the technician from 1 to 5 and can add a comment (here 5, ``Excellent''). The dialog warns that a review is final and cannot be edited or deleted, which keeps ratings honest. Sending the admins a private report about the technician is a separate action, visible behind the dialog."),
    # --- warranty
    "c16": ("c16-warranty-claim", "Warranty claim",
            "Ten days later the touch fails again, so Rahim reports a problem under the 30-day warranty. The dialog explains what is covered (the same fault coming back or a fitted part failing) and what is not (new damage, water or a drop). He chooses ``A replaced part stopped working'', describes the problem and can add up to four photos. The warranty card behind the dialog shows that the cover lasts until 13 November."),
    "t11": ("t11-warranty-book", "Booking the free re-inspection",
            "The technician's Warranty claims page. The header lists the deadlines: book the free re-inspection within 3 days, decide within 3 days of the visit, and finish a covered repair within 7 days. If a deadline is missed, an admin can take the claim over. Here the technician books a visit for 16 October at 11:00 with a note for Rahim (the other claims in the list are test data)."),
    "t12": ("t12-warranty-card", "The technician's record of the claim",
            "The claim card on the technician's side after the visit. It records the free re-inspection appointment, the decision ``Covered'' with its reason (the faulty touch layer is in the part he fitted) and the re-repair. The status ``Repaired -- waiting for confirmation'' means it is now up to Rahim to say whether it works."),
    "c17": ("c17-warranty-resolved", "Resolved warranty claim",
            "The warranty claim after it was resolved, as Rahim sees it. It records each step in order: the free re-inspection appointment, the technician's decision (``Covered''), the re-repair, and Rahim's answer ``Working now''. If the re-repair had not worked, an admin would have refunded the repair."),
    "c18": ("c18-notifications", "Customer notifications",
            "Rahim's notifications page. He got a notification at every step of the repair, listed newest first: here the warranty repair, the accepted claim and the booked re-inspection, then ``Your device is back'' and ``Repair completed''. Each one names the tracking code, and ``Mark all as read'' clears the unread count."),
    # --- technician account
    "t01": ("t01-overview", "Technician overview",
            "The technician's ``Work queue'', the first page after signing in. Three figures summarise the account: the money available to withdraw, the number of active jobs and the average rating (4.2). The queue below is empty because the walkthrough job is finished. New jobs that need an action will appear here."),
    "t13": ("t13-wallet", "Technician wallet",
            "The technician's wallet. The large number is the money available to withdraw, made up of earnings from repairs the customer has confirmed plus kept inspection fees. The cards below show pending money, the withdrawal in progress and the total paid out so far. The 3,600\\,BDT from this repair has been requested as a bKash withdrawal. Balances are always calculated from settlements and withdrawals and are never stored."),
    "t14": ("t14-profile-edit", "Editing the technician's details",
            "A technician editing their own details: name, phone, region, district and service address. The area decides which repairs the technician is offered, so it cannot be changed while a repair is active. The email and NID were checked at approval, so only an admin can change them. Behind the panel, the profile lists the technician's expertise by device, level and experience."),
    "t15": ("t15-completed-jobs", "Completed jobs",
            "The technician's completed jobs, newest first. Each job shows the device, the area, the tracking code and ``You receive'', the amount after the 10\\% commission (3,600\\,BDT for the walkthrough repair), with ``In your balance'' once the customer has confirmed receipt."),
    # --- admin
    "a01": ("a01-overview", "Admin operations overview",
            "The admin's home page, ``Operations''. The yellow ``Needs you'' box comes first and counts the urgent problems: missed pickups, overdue pickups, requests with no offers, stalled repairs and requests no local technician can take. Each count opens its own list, already filtered. Below are the counts of waiting work and the most urgent items, oldest first. Most of the numbers come from the seeded development data."),
    "a02": ("a02-requests", "All repair requests",
            "The admin's list of all 345 repair requests, with search by tracking code, customer or device, status and payment filters, and selectable columns. Each row shows the status, device, technician, tracking code, payment state and creation time, and the icons open the request or find a technician for it. Customer emails are blurred in this report."),
    "a03": ("a03-request-detail", "A request seen by the admin",
            "The walkthrough repair from the admin's side, with the same layout as the customer's and technician's pages. The admin sees the full record: the pickup condition, the customer's request, the inspection, the quote and payment, and the device and service details. ``More'' holds the admin actions, such as reassigning the technician or handling a dispute."),
    "a04": ("a04-assign", "Assigning technicians",
            "``Assign technicians'' lists the 111 requests still waiting for a technician. Flags such as ``Pickup time passed'' and ``No offers in 24h'' mark the ones that need help, and ``Find technicians'' suggests only the technicians that the matching rules allow. The admin can invite one of them to apply, or step in and assign one directly."),
    "a05": ("a05-technicians", "Technicians and applications",
            "The Technicians page lists all 122 technicians and the 9 applications waiting for review. Each row shows the district, the expertise (device and level), the application status (approved, awaiting review or not approved) and whether the technician is free or on a repair. ``Review'' opens an application with its documents for approval."),
    "a06": ("a06-catalogue", "Services and prices catalogue",
            "The catalogue editor, ``Services \\& prices''. Each service has a device, a name, a price estimate, an inspection fee, a status and the number of open and waiting requests that use it. The note at the top says price changes apply only to new requests."),
    "a07": ("a07-service-editor", "Editing a service",
            "Editing the ``Screen Replacement -- Mobile Phone'' service used in the walkthrough. The admin sets the description shown to customers, the 1,500--6,000\\,BDT estimate, the 200\\,BDT inspection fee (not below the minimum), the technician level needed, the typical time and how many photos customers may add. Saving creates a new pricing version, so existing requests keep their old price."),
    "a08": ("a08-reports", "Admin reports with AI summary",
            "The admin Reports page for the last 30 days. The AI summary at the top (a headline, highlights and ``What to do'') is written by Google Gemini only from the numbers on the page, and any sentence with a number that is not in the data is removed. Below it, the overview compares this period with the previous one."),
    "a09": ("a09-reports-charts", "Requests over time and demand by region",
            "Further down the Reports page. The line chart compares requests made with repairs finished each day, and ``Show as a table'' gives the same numbers as text. The region table shows, for each division, the requests, how many are waiting, how many no local technician can take, how many were turned away, and how many technicians there are and are free."),
    "a09b": ("a09b-reports-charts2", "Devices, repairs and pickup times",
            "The last part of the Reports page. The bars rank the most requested devices and repairs. The heat map shows how many pickups are booked in each two-hour window of each day, with darker cells for busier slots and Friday closed. Admins can use it to see where and when more technicians are needed."),
    "a10": ("a10-mark-paid", "Recording a bKash payout",
            "An admin recording the technician's withdrawal as paid. Sarabo does not send the money itself. Instead, the admin sends 3,600\\,BDT to the technician's bKash number with the bKash app, then enters the TrxID from the bKash confirmation (here a test value). A TrxID can be used only once, and the record cannot be undone."),
    "a11": ("a11-reviews", "Technician reviews",
            "The admin's list of technician reviews, filtered by visibility and technician, with Rahim's 5/5 review at the top. An admin can hide or restore a review with a reason, but the rating and comment themselves never change, and every change is kept. Technician emails are blurred in this report."),
    "a12": ("a12-users", "User management",
            "The Users page lists all 186 accounts with their role (Customer, Technician or Admin). Only an admin can give or remove admin access, using ``Make admin'', and customers can only become technicians through an approved application. Personal emails are blurred, and the addresses that are still visible belong to seeded test accounts."),
}

SECTIONS = [
    ("Public Website",
     "Anyone can use these pages without an account. A visitor can see what Sarabo repairs and what it usually costs, check that their area is covered, ask the AI chat a question, browse the open jobs that technicians can take, and follow a repair with its tracking code. Every page also works on a phone.",
     ["p01", "p02", "p03", "p05", "p04", "p06", "mob"]),
    ("Creating the Request",
     "From here the chapter follows one repair. Rahim, a customer in Sylhet, dropped his Samsung Galaxy A54: the screen cracked, a green line appeared and the touch stopped working. He signs in, describes the problem in his own words and lets the AI fill in the form, then chooses where and when the phone should be collected.",
     ["c01", "c02", "c03", "c04"]),
    ("Receiving an Offer",
     "The request is posted on the jobs board, and technicians in the same region who can do the repair are notified. One of them sends an offer with an estimate, an inspection fee and a note, and Rahim sees it on his request with the reasons it is ranked where it is.",
     ["t02", "t03", "c05", "c06"]),
    ("Choosing and Booking",
     "Rahim chooses the offer. Paying the inspection fee through Stripe books the technician for the pickup window and closes the other offers. The fee is taken off the final price later.",
     ["c07", "c08", "c09"]),
    ("Pickup, Inspection and Quote",
     "The technician collects the phone, records its condition, inspects it and writes an itemised quote. Nothing is charged until Rahim has seen the findings and the price and approved them.",
     ["t04", "t05", "t06", "t07", "c10"]),
    ("Payment",
     "Rahim approves the quote and pays the rest by card. Each payment gets a PDF receipt and appears in his payment history.",
     ["c11", "c12", "c13"]),
    ("Repair and Hand-Over",
     "The technician repairs the phone, posting updates that Rahim can see, then returns it. Rahim confirms he has it back, which releases the technician's earning and starts the warranty, and rates the technician.",
     ["t08", "t09", "t10", "c14", "c15"]),
    ("Warranty",
     "Ten days later the touch fails again. Rahim reports it, the technician books a free re-inspection, finds that the part he fitted is faulty and repairs it again for free. Rahim then confirms that it works. Every step has a deadline, and Rahim is notified each time.",
     ["c16", "t11", "t12", "c17", "c18"]),
    ("The Technician's Account",
     "Besides the job pages, a technician has an overview, a wallet for withdrawing earnings, a profile and a list of completed jobs.",
     ["t01", "t13", "t14", "t15"]),
    ("Administration",
     "Admins run the platform. Their overview shows the problems that need a person first, and from there they manage requests and technicians, the service catalogue, reports, payouts, reviews and user roles. Most of the numbers in these screens come from the seeded development data.",
     ["a01", "a02", "a03", "a04", "a05", "a06", "a07", "a08", "a09", "a09b", "a10", "a11", "a12"]),
]

LABELS = {"Creating the Request": r"\label{sec:wt-request}", "Warranty": r"\label{sec:wt-warranty}"}


def copy_all():
    OUT.mkdir(exist_ok=True)
    for old in OUT.glob("*.jpg"):
        old.unlink()
    for key, (src, _, _) in S.items():
        srcs = ["p08-mob-home", "p09-mob-jobs"] if key == "mob" else [src]
        for i, name in enumerate(srcs):
            im = Image.open(SRC / f"{name}.jpg").convert("RGB")   # the whole screen, not cropped
            for box in BLUR.get(key, []):
                im.paste(im.crop(box).filter(ImageFilter.GaussianBlur(9)), box[:2])
            out = f"{key}{'ab'[i]}" if key == "mob" else key
            im.save(OUT / f"{out}.jpg", quality=88, optimize=True, progressive=True)


def figure_tex(key):
    _, short, caption = S[key]
    box = "{\\setlength{\\fboxsep}{0pt}\\fbox{\\includegraphics[%s]{img/wt/%s}}}"
    if key == "mob":   # two tall phone screens side by side
        body = box % ("height=0.5\\textheight", "moba") + "\\hspace{10mm}" + box % ("height=0.5\\textheight", "mobb")
    else:
        # the whole screen, sized so that two figures with their captions share a page
        body = box % (f"width=\\dimexpr\\linewidth-0.6pt\\relax,height={FIG_H}\\textheight,keepaspectratio", key)
    # single-spaced caption, like the tables
    return (f"\\begin{{figure}}[!htbp]\\renewcommand{{\\baselinestretch}}{{1.0}}\\selectfont\\centering"
            f"{body}\\caption[{short}]{{{caption}}}\\label{{fig:wt-{key}}}\\end{{figure}}\n")


def main():
    copy_all()
    n = sum(len(k) for _, _, k in SECTIONS)
    out = [r"""\documentclass{standalone}
\usepackage{standalone}

\begin{document}
\chapter{System Walkthrough}
\label{ch:walkthrough}

This chapter shows the finished system in """ + str(n) + r""" figures (54 screenshots). I took them on 14 October 2026 from the final code, with real Firebase sign-in, real Gemini answers and Stripe in test mode. Section~\ref{sec:wt-public} shows the public pages. From Section~\ref{sec:wt-request} onwards, the screenshots follow \emph{one} repair, the cracked Samsung Galaxy A54 used as the example throughout this report, through every state in Figure~\ref{fig:e2e}. They switch between the customer's and the technician's screens as the case moves along. The last two sections show the technician's own account and the admin pages. Each picture shows the whole browser window exactly as the user saw it, without cropping, two to a page. Personal email addresses are blurred, and any other requests, people and figures that appear in lists come from the seeded development data.

% a page holding only a screenshot starts it at the top of the page, not in the middle
\makeatletter\setlength{\@fptop}{0pt}\setlength{\@fpbot}{0pt plus 1fil}\makeatother
"""]
    for title, intro, keys in SECTIONS:
        label = LABELS.get(title, r"\label{sec:wt-public}" if title == "Public Website" else "")
        # finish the previous section's pictures first, and keep each heading with room below it
        out.append(f"\n\\FloatBarrier\n\\needspace{{9\\baselineskip}}\n\\section{{{title}}}{label}\n{intro}\n\n")
        for k in keys:
            out.append(figure_tex(k))
    out.append("\n\\FloatBarrier\n"
               "\\makeatletter\\setlength{\\@fptop}{0pt plus 1fil}\\setlength{\\@fpbot}{0pt plus 1fil}\\makeatother\n"
               "\\end{document}\n")
    TEX.write_text("".join(out), encoding="utf-8")
    print("figures:", n)


if __name__ == "__main__":
    main()
