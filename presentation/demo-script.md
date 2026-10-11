# Live Demo Script (5 minutes)

Shown right after the slides. Goal: one repair from request to payout, across all three roles.

## Before the session (do not skip)

- [ ] Open the app (live site or local) and sign in to **three accounts in three separate browser windows** (normal window plus two private windows, or separate profiles):
  Customer, Technician (approved, same region as the customer, with expertise for the chosen repair), Admin.
- [ ] Prepare one request that is already **at "quote submitted"**. A full repair takes too long to do live.
- [ ] Have a damage photo (a cracked phone screen) on the desktop for the AI helper.
- [ ] Stripe test card ready: `4242 4242 4242 4242`, any future date, any CVC.
- [ ] Zoom the browser to 110-125 % so the room can read it.
- [ ] Backup: screenshots in `screens/`, in case the internet fails.

## Run of show

| Time | Window | What to do | What to say |
|---|---|---|---|
| 0:00-1:00 | Customer | Create Request: type *"amar phone er screen fete geche, touch kaj kore na"*, add the photo, press the AI helper | "The customer writes in Banglish. AI fills device, service and description. The price is the catalogue estimate, not AI." |
| 1:00-1:30 | Customer | Pick a pickup slot and submit; show the tracking code | "Refused if no technician in the region can do it. Every request gets a tracking code." |
| 1:30-2:15 | Technician | Find jobs: open the new job, show the price guide, press "Write with AI", send the offer | "Technicians see a safe summary and a price guide from real offers. AI only drafts the message." |
| 2:15-2:45 | Customer | My Requests: "1 offer waiting", choose it, pay the inspection fee with the test card | "Paying the fee books the technician in one transaction." |
| 2:45-3:45 | Customer | Switch to the **prepared request**: show the itemised quote, the fee credit and "Approve and pay BDT X", then pay | "The customer pays only the rest; the fee already counts." |
| 3:45-4:15 | Technician | Start, then complete the repair; then the Customer confirms receipt | "Only the customer's confirmation releases the technician's money." |
| 4:15-4:40 | Technician | Wallet: 90 % available, request a bKash withdrawal | "Balance is calculated from records, never stored." |
| 4:40-5:00 | Admin | Overview attention list, Reports with the AI summary, Withdrawals: mark paid with TrxID | "Admins see what needs action, and every AI number is checked against real data." |

## If something fails

- AI helper is off or slow: fill the form by hand and say "AI is optional; the form works without it".
- Stripe page does not open: show the Payment History of an already-paid request and download its PDF receipt.
- Out of time: skip the Admin reports and go straight to marking the withdrawal paid.
