# Live Demo Script: Detailed Version (about 12-15 minutes)

Use this when there is more time, for a rehearsal, or as a source of extra points.
The 5-minute version is [demo-script.md](demo-script.md). Button names below are exactly
as they appear on screen.

---

## 1. The real-life story (1 minute)

> *This is a typical situation, not a real customer.*

### The problem: Rahim's phone

Rahim, a student in Ambarkhana, Sylhet, drops his Samsung Galaxy A54. The screen cracks, a
green line appears, and touch stops working.

1. **No price up front.** The nearest shop says "around 2,500 taka" without opening the phone.
2. **No visibility.** They keep the phone for a week. Rahim calls three times to ask where it is.
3. **Surprise bill.** When he collects it, the price is 4,500 taka. There is no itemised quote, so he
   cannot see what was labour and what was parts.
4. **No proof, no warranty.** Ten days later touch fails again at the top of the screen. The shop
   says he must have dropped it again. Rahim has no receipt and no record of the condition.

The technician has problems too. **Karim**, a skilled independent technician, gets work only
by word of mouth, writes quotes on paper, and sometimes isn't paid after a customer changes
their mind.

### The solution: the same repair on Sarabo

| Rahim's problem | What Sarabo does |
|---|---|
| No price up front | Catalogue estimate (1,500-6,000 taka for this repair) shown before anything is booked; technicians send offers with their own estimate |
| No visibility | A tracking code and a 4-step timeline (Request, Inspect, Approve, Repaired), plus notifications at every step |
| Surprise bill | An itemised quote (labour 800 + parts 3,200 = 4,000) that he approves before any work; the 200 taka visit fee is deducted |
| No proof | The technician records the phone's condition at pickup; the customer sees it and can dispute it |
| No warranty | 30 days: the same technician re-inspects free; a covered fault is re-repaired free or refunded by an admin |
| Karim isn't paid | The customer pays online before the repair starts; Karim's 90 % is held, then released when Rahim confirms he got the phone back |

---

## 2. Before the session

**Setup**
- [ ] Prefer the **local** app: start the server (`npm run dev` in `sarabo-server`, port 3000) and
  the client (`npm run dev` in `sarabo-client`, `http://localhost:5173`). It has all the prepared data.
- [ ] On the live site (`https://sarabo-client-six.vercel.app`): set the PC's DNS to 1.1.1.1 or
  8.8.8.8 and run `ipconfig /flushdns`. This ISP sometimes cannot reach Vercel.
- [ ] Three browser windows, one per account (normal window plus two private windows, or
  separate Chrome profiles): **Customer**, **Technician** (approved, Sylhet, smartphone skills),
  **Admin**.
- [ ] Browser zoom 125 %. Close other tabs, turn off notifications, charge the laptop.

**Data to prepare**
- [ ] One request already at **Quote ready** (for the approve-and-pay step).
- [ ] The finished **Samsung Galaxy A54** request with a resolved warranty claim (made for the
  report) open in a tab.
- [ ] A photo of a cracked phone screen on the desktop (optional, for the AI photo check).
- [ ] Stripe test card `4242 4242 4242 4242`, expiry 12/34, CVC 123.

**Limits to remember**
- AI support chat: 8 questions per 10 minutes for a signed-out visitor, so don't test it repeatedly before the demo.
- Gemini free tier: if AI is slow, fill the form by hand. Everything works without AI.

---

## 3. Run of show

### Part A: Public site (1 minute)

| Do | Say |
|---|---|
| Home page | "Anyone can see services and prices without an account." |
| **Services** | "45 services across 8 device types. Every price is in taka and is an estimate; the final price comes after inspection." |
| **Service areas**: search *Ambarkhana* | "Rahim's area. The map zooms to the exact neighbourhood, not just the district." |
| **Ask Sarabo**: *"My phone screen is cracked, how much will it cost?"* | "The AI answer comes from our live catalogue: 1,500 to 6,000 taka, inspection fee 200. It never invents a price." |

### Part B: Customer creates the request (1.5 minutes)

| Do | Say |
|---|---|
| **Create Request** → type *"Amar Samsung Galaxy A54 phone hat theke pore giye screen fete geche. Display e green line ashe ar touch kaj korche na."* → **Fill the form for me** | "Rahim writes in Banglish. Gemini fills in the device, brand, model and the right repair, and writes a clear English description. He can change anything, or press Undo." |
| Region **Sylhet**, district **Sylhet**, address, then a pickup slot | "He chooses a 2-hour pickup window. Friday is closed; each slot has limited capacity." |
| **Create request** | "If no approved technician in Sylhet can do this repair, the request is refused with an explanation instead of waiting forever. Admins see that refused demand, so they know where to recruit." |
| Optional: **Choose photos** → **Upload** | "Photos are private. Only Rahim, the admin and the booked technician can see them, through short-lived links." |

### Part C: Technician sends an offer (1.5 minutes)

| Do | Say |
|---|---|
| Technician window → **Find jobs** → search *Galaxy A54* | "Karim sees jobs in his region that match his skills. He sees the problem, but not Rahim's name or address." |
| **Send offer** | "The price guide shows what technicians really offered for this repair recently. The inspection fee has a minimum: 100 taka for small repairs, 200 for bigger ones." |
| Estimate 3,500-5,000; type *"likely display panel and touch, original screen available"* → **Write it for me** → **Send application** | "Karim types a few words and AI writes a polite note. It removes phone numbers, so contact stays on the platform." |

### Part D: Customer chooses and books (1.5 minutes)

| Do | Say |
|---|---|
| Customer window → **My Requests** → open the request | "Rahim sees offers side by side." |
| Point at the tags | "They are ranked by five things Sarabo already knows: rating, reliability, price, district and reply time. The tags say why: 12 repairs, no missed pickups; in your district; usually replies in 2 minutes." |
| **Choose** → **Pay ৳200 and book** → test card → **Pay** | "Paying the visit fee books Karim, all in one database step. If Karim doesn't come, it's a full refund. If Rahim cancels at least 2 hours before, it's also a full refund." |

### Part E: Pickup, inspection and quote (1.5 minutes)

| Do | Say |
|---|---|
| Technician → **Assigned jobs** → **Start pickup** → **Device received**; fill the condition | "Karim records the phone's condition with Rahim: cracked screen, small scratch on the back, no SIM. This is what Rahim lacked at the shop: proof." |
| Inspection form: findings, issue, **Repairable with parts** → **Submit inspection** | "If the phone can't be repaired, either side can close the request. It never gets stuck." |
| Quote: labour 800, parts 3,200 → **Send quote** | "Karim sees the 10 % commission and what he receives, 3,600." |

### Part F: Approve and pay (1 minute)

| Do | Say |
|---|---|
| Customer → the request (or the prepared one) | "Labour, parts, total, all in writing. Nothing is charged until Rahim approves." |
| Point at *Inspection fee you already paid − ৳200* | "He pays only what is left: 3,800." |
| **Approve and pay** → test card → payment success → **Download receipt (PDF)** | "Stripe's signed webhook is the single source of truth, so a payment is recorded exactly once, even if the page reloads." |

### Part G: Repair and hand-over (1 minute)

| Do | Say |
|---|---|
| Technician → **Start repair** → add an update → **Mark repair complete** | "Rahim sees each update." |
| **Mark device returned** | "If Rahim doesn't answer within 3 days, receipt is confirmed automatically. If he says he hasn't received it, an admin decides." |
| Customer → **Confirm device received** → **Rate your technician** (5 stars) | "Karim's money unlocks only now. The review is one per repair and can't be faked." |

### Part H: Warranty (1 minute)

| Do | Say |
|---|---|
| Customer → the finished Galaxy A54 → **Warranty** | "This is the end of Rahim's story. Ten days later touch failed again." |
| Show the claim: *A replaced part stopped working* → re-inspection → *Covered* → re-repair → *Working now* | "He reported it; Karim had 3 days to book a free visit; he agreed it was the part he fitted and replaced it free. If he hadn't, an admin could take over and refund. Every step has a deadline." |

### Part I: Technician wallet and Admin (1.5 minutes)

| Do | Say |
|---|---|
| Technician → **Wallet** → request a withdrawal to bKash | "The balance is calculated from records, never stored as a number, so it can't drift." |
| Admin → **Overview** | "The admin sees what needs action first: missed pickups, requests with no offers, stalled repairs, refunds, disputes." |
| **Withdrawals** → **Mark paid** with a TrxID | "The admin sends money with bKash Send Money, then records the TrxID. Sarabo has no bKash API, so this step is manual." |
| **Reports** → AI summary | "The AI summary only sees totals. Any sentence with a number that isn't in the real data is removed." |
| **Services & prices** → **Edit** a service | "Changing a price creates a new version; requests already made keep their old price." |

**Close:** "So Rahim gets a fair, written price, tracking and a warranty, and Karim gets steady work and
guaranteed payment. Thank you."

---

## 4. If something fails

| Problem | What to do |
|---|---|
| AI helper slow or says unavailable | Fill the form by hand: "AI is optional; the form works without it." |
| Stripe page does not open | Show **Payment History** of a paid request and download its PDF receipt |
| "No technician available" when creating | Check the technician is approved, in Sylhet, with smartphone skills and not busy; or use the prepared request |
| Site does not load | Switch to the local app, or show the Chapter 7 screenshots in the report |
| Running late | Skip Part A and Part I; always keep Part H (warranty), because it ends the story |

---

## 5. Likely questions, with short answers

**Why is this more than a CRUD app?**
A repair is a case with 14 states. The server checks the user's role and the current state for every action,
and money steps run in database transactions, so nothing half-happens.

**How do you stop double payments or double booking?**
Stripe's signed webhook is the single source of truth, and processing is idempotent, so the same event is recorded once.
A technician's availability and the request state change in one transaction, and we tested races directly,
for example two admins assigning at the same moment.

**Stripe doesn't work in Bangladesh. Why use it?**
It runs in test mode for the project. The payment code sits behind one service, so a local gateway such as
SSLCOMMERZ or the bKash Payment Gateway can replace it. That is listed as future work.

**What if the technician never comes?**
The admin records a missed pickup, the visit fee is refunded in full, and the job opens for other offers.

**What if the customer never pays the quote, or never confirms receipt?**
Every waiting state has a deadline. An unpaid quote closes after 3 days. Receipt is confirmed automatically after 3 days.
Stalled work shows up on the admin overview.

**Is the AI safe? Can it make up prices?**
No AI feature sets a price. Answers must use IDs from the live catalogue and are checked again on the server.
No names, emails or card numbers are sent to the model, and there are daily limits.

**How does offer ranking work?**
It uses five factors from stored data: rating 30 %, reliability 25 %, price 20 %, same district 15 %, reply time 10 %.
A new technician gets a neutral score, not a penalty. The customer still chooses.

**How is the money split?**
The technician gets 90 % and Sarabo 10 %, frozen when the customer pays. A kept visit fee (late cancellation or
declined quote) is split the same way.

**Explain the ER diagram.**
A user creates many repair requests and can become a technician. Each request is priced by one service, gets many offers,
and has its payments, one review and at most two warranty claims. The quote and inspection are stored inside the request.

**Why MongoDB?**
A repair request is one document that holds its own quote, inspection and history, which fits a document database.
MongoDB transactions keep related collections consistent.

**How did you test it?**
2,761 automated server tests run over real HTTP against a real MongoDB replica set, with fake Stripe, AI and storage.
There are also 58 browser tests on desktop and mobile, and CI on every push.

**What are the limitations?**
Payments are in test mode, bKash payouts are manual, there are no real customers yet, and there has been no load test.
