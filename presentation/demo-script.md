# Live Demo Script (5 minutes)

Shown right after the 10 slides. Goal: one repair from request to payout, across all three roles,
told as one real-life story. A longer version is in [demo-script-detailed.md](demo-script-detailed.md).

## The story (use it to open the demo, 30 seconds)

> *This is a typical situation, not a real customer.*

**Problem.** Rahim lives in Ambarkhana, Sylhet. His Samsung Galaxy A54 falls and the screen
cracks: a green line, and touch stops working. He takes it to a shop. They say "about 2,500
taka", keep the phone for a week, then ask for 4,500. There is no written quote and no receipt.
Ten days later the touch fails again. The shop says it is new damage, and Rahim cannot prove
otherwise.

**Solution with Sarabo.** Rahim describes the problem in Banglish on his phone. A verified local
technician offers a price before collecting the phone. Rahim pays a 200 taka visit fee. After
inspection he sees an itemised quote of 4,000 taka, and the 200 he already paid is deducted.
He tracks every step. When the touch fails again, the warranty covers a free re-repair.

Say: *"Let me show you exactly that, live."*

## Before the session (do not skip)

- [ ] Use the **local** app (`npm run dev` in both repos, `http://localhost:5173`); it has the prepared data.
  On the live site, set the PC's DNS to 1.1.1.1 first (this ISP sometimes cannot reach Vercel).
- [ ] Sign in to **three accounts in three separate browser windows** (normal window plus two private windows):
  Customer, Technician (approved, Sylhet, smartphone skills), Admin.
- [ ] Prepare one request that is already at **"Quote ready"**. A full repair takes too long to do live.
- [ ] Keep the finished **Samsung Galaxy A54** request (from the report screenshots) open in a tab, to show the warranty.
- [ ] Stripe test card: `4242 4242 4242 4242`, any future date (12/34), any CVC (123).
- [ ] Zoom the browser to 125 % so the room can read it. Close other tabs and notifications.
- [ ] Backup: the report's Chapter 7 screenshots, in case the internet fails.

## Run of show

| Time | Window | Do | Say |
|---|---|---|---|
| 0:00-0:30 | — | Tell the story above | "This is Rahim's problem. Here is how Sarabo solves it." |
| 0:30-1:20 | Customer | **Create Request**: type *"Amar Samsung A54 er screen fete geche, touch kaj korche na"*, press **Fill the form for me**; pick Sylhet, a pickup slot; **Create request** | "He writes in Banglish. AI fills the device and the repair. The price range comes from our catalogue, never from AI. If no technician covers his area, the request is refused instead of waiting forever." |
| 1:20-2:00 | Technician | **Find jobs**: open the new job; show the price guide; type a few words, press **Write it for me**; **Send application** | "Technicians see the problem but not Rahim's name or address. The price guide comes from real past offers." |
| 2:00-2:40 | Customer | Open the request: the offer with tags (*In your district*, *Usually replies in 2 min*); **Choose**, pay ৳200 with the test card | "Offers are ranked by rating, reliability, price, distance and reply time. Paying the fee books the technician; if he doesn't come, it's refunded." |
| 2:40-3:30 | Customer | Switch to the **prepared request**: itemised quote, *Fee already paid − ৳200*, **Approve and pay**; pay with the test card | "Labour, parts, total, all in writing before any work. He pays only what is left. A PDF receipt is ready." |
| 3:30-4:00 | Technician | On that request: **Start repair**, add one update, **Mark repair complete**, **Mark device returned** | "Every step is tracked. The technician's 90 % unlocks only after Rahim confirms he got the phone back." |
| 4:00-4:30 | Customer | Open the finished **Galaxy A54**: scroll to **Warranty**, show the resolved claim | "Ten days later the touch failed again, exactly like Rahim's story. Here the same technician re-inspected free and fixed it. If he couldn't, an admin refunds." |
| 4:30-5:00 | Admin | **Overview** (*Needs you* list), then **Reports** with the AI summary | "The admin sees missed pickups and stuck repairs first. Nothing can wait forever. Thank you." |

## If something fails

- **AI helper slow or off:** fill the form by hand. Say "AI is optional, the form works without it."
- **Stripe page does not open:** show **Payment History** of a paid request and download its PDF receipt.
- **Running late:** skip the technician repair steps (3:30-4:00) and go straight to the warranty.
- **No internet:** use the Chapter 7 screenshots in the report PDF; tell the same story over them.
