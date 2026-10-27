# Sarabo — Presentation Script (5 minutes)

10 slides · about 700 spoken words · written to be said, not read.
The long version is [script-full.md](script-full.md).

The time after each slide title is when that slide should start. If you're more than 10 seconds behind at slide 6, drop the lines marked *(cut if late)*. Cues in *[square brackets]* are for you, not for the audience: *[pause]* means one breath, *[point]* means point at the slide.

---

**Slide 1 · Title · 0:00**

Assalamu alaikum. I'm Jahid Hasan, ID 222-115-116, and my project, supervised by Shrabanti Chowdhury, is called **Sarabo**. In one line: it helps people get their devices repaired *without the fear*.

**Slide 2 · The problem · 0:15**

Let me start with a small story. *[pause]* Rahim cracks his phone screen. The shop says "around 2,500 taka", keeps the phone for a week, and then asks for 4,500. No written quote, no receipt. Ten days later the touch stops working again, and the shop says, "You must have dropped it."

I think most of us have been Rahim at some point. And the technician isn't happy either: he finds work only by word of mouth, and he's never sure he'll get paid. So nobody trusts anybody.

**Slide 3 · The solution · 0:40**

Sarabo puts the whole repair into **one clear, tracked process** for three people. The customer asks for a repair, compares offers, pays and follows the device. The technician finds jobs, quotes and gets paid. And the admin keeps everything moving. There are 45 services across 8 device types, all in taka, and it's live on the internet today.

**Slide 4 · How it works · 1:05**

So how does Rahim's repair look on Sarabo? *[point]* Six steps.

He describes the problem, even in Banglish, and AI fills the form for him. Local technicians with the right skill send offers. He picks one and pays a small inspection fee to book. After checking the phone, the technician sends a written quote: parts, labour, total. Rahim pays only what's left, because the fee is already counted. And when he gets his phone back, the technician gets 90 percent and a 30-day warranty starts.

And it's fair both ways: if the technician doesn't turn up, Rahim gets every taka back.

**Slide 5 · ER diagram · 1:45**

Here's how the data fits together. *[point]* A user can make many repair requests, and a user can also become a technician. Each request is priced by one service, gets many offers, and has its payments, one review and up to two warranty claims. The quote and the inspection live inside the request itself, because they belong only to that repair.

**Slide 6 · Ranked offers · 2:20**

When offers come in, Rahim doesn't have to guess. Sarabo ranks them by rating, reliability, price, distance and how fast the technician replies, and the little tags tell him *why*. But the choice is still his.

*(cut if late)* Then the quote: 4,000 taka, minus the 200 he already paid, so 3,800. One button to approve and pay.

**Slide 7 · Warranty · 3:00**

Remember Rahim's touch failing after ten days? On Sarabo, that's covered. Every repair has a **30-day warranty**: the same technician checks it again for free, and fixes it or refunds it.

*(cut if late)* I also made sure nothing can get stuck. Every waiting step has a deadline, and if something stalls, the admin is told.

**Slide 8 · Applied AI · 3:35**

AI helps in four places: filling the request, writing the technician's note, the support chat, and the admin's weekly summary. But my rule was simple: **AI suggests, people decide.**

*(cut if late)* AI never sets a price, everything it says is checked against real data, and no personal details are sent to it.

**Slide 9 · Architecture · 4:05**

Under the hood, it's React on the front, Express on Vercel, and MongoDB, all in the same region so it's fast. Because real money moves here, the **server always decides**. Booking, payment and refunds are all-or-nothing.

*(cut if late)* So even if two people click at the same second, nobody pays twice.

**Slide 10 · Results · 4:35**

All 2,761 server tests and 58 browser tests pass, and all twelve objectives are met. To be honest about the limits: payments are in test mode, bKash payouts are manual, and there are no real customers yet. Next, I'd like to add a local payment gateway and a Bangla mobile app.

Thank you. *[pause]* Now let me show you Rahim's repair, live.

**[5:00]**

---

## Making it sound like you

- **Rehearse three times with a timer.** Check you're at slide 6 by 2:20 and slide 10 by 4:35.
- **Learn the story, not the lines.** If you remember Rahim, the cracked screen, the 4,500 bill and the warranty, the rest follows naturally.
- **Slow down on the numbers.** Say these clearly: 45 services, 8 device types, 90 percent, 30 days, 2,761 and 58 tests.
- **Look at the board, not the slide.** Glance at the slide only when you *[point]*.
- **Pause after each slide title.** One breath gives the board time to look, and it's already counted in the timing.
- **Say Rahim's name in the demo too.** The script ends with "let me show you Rahim's repair", so the demo continues the same story ([demo-plan-5min.md](demo-plan-5min.md)).
- **If you forget a line, skip it.** Nobody knows the script but you; just go to the next point.
