# Work Log — Fixes and Improvements

Every change made during the final-year-project phase is recorded here: what the
problem was, what was changed, which files, and how it was checked. This log feeds
the "Implementation" and "Testing" chapters of the report.

## Entry format

```
### <number>. <short title> — <date>
- Type: fix | improvement | feature | docs | test
- Problem / goal:
- What was changed:
- Files:
- How it was tested:
- Result / screenshot:
```

---

### 0. Project review and documentation setup — 2026-10-11
- Type: docs
- Problem / goal: Understand the existing Sarabo codebase before making changes, and
  set up a place to record all work for the final report.
- What was changed: Read the client and server docs and git history; wrote the
  project overview and development history; created this work log.
- Files: `fyp-docs/README.md`, `01-project-overview.md`, `02-development-history.md`, `03-work-log.md`
- How it was tested: n/a
- Result: Baseline documented. Note: `sarabo-server/package-lock.json` already had an
  uncommitted change before this phase began.

### 1. Full verification run — 2026-10-11
- Type: test
- Goal: Get current, real test numbers for the final report. The earlier report's
  figure (1,890) was from August.
- What was done:
  - Server: exported a clean copy of committed code (`git archive`, no `.env`) and ran all
    four suites against a temporary in-memory MongoDB 8 replica set. Used a fake Firebase key
    and placeholder Stripe keys, with AI and email off, the same setup as CI. No real database
    or external service was touched.
  - Client: `npm run lint`, a production build (placeholder `https` API URL, as in CI), and
    Playwright browser tests (`npm run test:e2e`).
  - Checked the latest GitHub Actions runs for both repositories.
- Results:
  - Server `npm test`: **2,578 / 2,578 passed**. Re-run on their own: support 160/160,
    migrations 63/63, feedback 177/177 (already included in the full suite).
  - Client: lint passed; build passed; Playwright **54 / 54 passed** (27 scenarios × desktop and mobile).
  - CI: latest `main` runs (4 Oct 2026) succeeded for both repositories.
  - Note: `npm run build` with the local `.env` stops because `VITE_API_BASE_URL` is `http://`.
    This is an intended production guard, not a bug.
- Code commits at test time: client `0412ac4`, server `0d779aa`. No code was changed and
  nothing was committed.

### 2. Final report and presentation — 2026-10-11
- Type: docs
- What was done: Wrote the final report in the Metropolitan University LaTeX template
  (`report/`, 11 chapters + 5 appendices, 75 pages), compiled it to
  `Sarabo_Final_Report.pdf`, and built a 10-slide PPTX with speaker notes plus a live-demo script.
  Screenshots in `presentation/screens/` come from the production build with a faked API
  (sample data, no real users).
- Template change: in the report's copy of `myStyle.sty`, `inputenc` is now loaded only
  under pdfLaTeX. It breaks XeTeX and has no effect elsewhere.

### 3. Service-area map: search goes to the exact sub-area — 2026-10-11
- Type: improvement
- Problem / goal: Searching a sub-area such as "Ambarkhana" only moved the map to the
  Sylhet district centre. `serviceAreas.json` held one coordinate per district; its
  covered sub-areas (Ambarkhana, Zindabazar, ...) were only names.
- What was changed:
  - Looked up coordinates for all 236 covered sub-areas once, offline, with OpenStreetMap
    Nominatim (one-off script, 1 request/second). A result was kept only if it lies inside
    the same district: within 35 km of the district centre, or up to 120 km when the OSM
    address names that district (for far upazilas like Teknaf). Two wrong matches were
    removed by hand ("Kushtia Sadar" landed in Rajbari; "Bera" landed on a village in Santhia).
    Result: **226 of 236** sub-areas have a point. The other 10 are not in OSM under those
    names and fall back to their district pin, as before.
  - Stored as a new `covered_area_points` list on each district in `public/serviceAreas.json`.
    The field is new, so the request form and the server seed script are unaffected.
    No geocoding happens in the browser.
  - Search lists matching sub-areas first ("Ambarkhana · Sylhet"), then districts.
    Choosing a sub-area zooms to street level on that spot with a labelled pin.
    A district name ("Sylhet") still opens the district.
  - A selected district shows its sub-areas as small labelled pins and frames all of them.
    The area chips in the panel are now buttons that move the map to that sub-area.
  - `?q=Ambarkhana` links work the same way.
- Files (client): `public/serviceAreas.json`, `src/utils/serviceAreaPresentation.js`
  (`getAreaPoints`, `findPlaceMatches`, `resolveSearch`),
  `src/components/public/ServiceAreaMap.jsx`, `src/pages/ServiceAreas/ServiceAreas.jsx`,
  `e2e/public-pages.spec.js`
- How it was tested: two new Playwright tests (search "Ambarkhana" opens Ambarkhana and
  the chip moves the map; `?q=Sylhet` still opens the district), on desktop and mobile.
  Also checked visually with screenshots. Full client run: lint passed, production build
  passed, Playwright **58 / 58** passed.

### 4. Removing a technician pays out their wallet to bKash — 2026-10-11
- Type: feature
- Problem / goal: When an admin removed (revoked) a technician, any money in their wallet
  was left stranded: they lost access to the wallet page and could not request a withdrawal.
- Important limit: Sarabo has no bKash API. All payouts are manual: the admin sends money
  with bKash "Send Money" and records the TrxID. So "auto withdraw" means the system
  **automatically creates the final withdrawal**; an admin still sends the money and records the TrxID.
- What was changed:
  - Server (`services/technicianRemovalPayout.js`, new): when an approved technician is
    removed, their whole *available* balance is queued as a withdrawal to their bKash
    number, **in the same database transaction** as the removal. Both happen or neither does.
    The balance comes from the same `calculateWallet()` the wallet page uses.
  - bKash number, in order: the number the admin typed; the number on an already-open
    request; the number from their last withdrawal; their application phone, if it is a
    valid bKash number. If money is owed and there is no number, removal is refused
    (`BKASH_NUMBER_REQUIRED`) and nothing changes.
  - If the technician already has an open request, it is topped up to the full balance.
    No second request is opened (the one-open-request database rule still holds).
  - Pending money (repairs not yet confirmed) is not available yet, so it is not included.
    The dialog shows this amount.
  - Withdrawals now carry `reason: 'technician_removed'` and `createdBy` (the admin).
  - New endpoint `GET /technicians/:id/final-payout` (admin only) previews the amount and number.
  - New notification `technician_removed_final_payout` tells the person the amount and number.
    `withdrawal_paid` / `withdrawal_rejected` can now also go to a removed technician (role
    `user`), with a link to Notifications instead of the wallet page they can no longer open.
  - Client: "Revoke approval" now opens a "Remove … ?" dialog showing the balance to pay,
    the bKash number (pre-filled and editable) and any pending amount. The confirm button
    reads "Remove and pay out". The Withdrawal Requests queue marks these rows
    "Final payout · technician removed".
- Files (server): `services/technicianRemovalPayout.js` (new),
  `controllers/technicianController.js`, `routes/technicians.js`,
  `controllers/walletController.js`, `utils/settlement.js`, `utils/notificationEvents.js`,
  `tests/technicianRemovalPayoutTests.js` (new), `test-all.js`
- Files (client): `src/pages/Dashboard/ApproveTechnicians/ApproveTechnicians.jsx`,
  `src/pages/Dashboard/WithdrawalRequests/WithdrawalRequests.jsx`,
  `src/utils/technicianApprovalErrorMessage.js`
- How it was tested: 15 new server tests (7 rule tests + 8 end-to-end against the database):
  balance queued on removal, notification sent, final payout paid through the normal
  queue, refused when there is no number, invalid number refused, admin-entered number
  accepted, open request topped up, no-balance removal unchanged. Three existing tests were
  updated on purpose: the event count (40 → 41), the list of multi-role events, and the
  withdrawal link test. Full server suite on a temporary in-memory MongoDB 8 replica set
  (working-tree copy without `.env`, fake keys, as in entry 1): **2,595 / 2,595 passed**.
  The admin dialog was lint- and build-checked but not clicked through in a browser.
- Not covered: changing a technician's role to "user" from the Users page does not
  trigger a payout. Only "Revoke approval" on the Technicians page does.

Nothing in entries 3–4 was committed, pushed or deployed.

### 5. Homepage hero: text no longer sits on top of the photo — 2026-10-11
- Type: fix
- Problem / goal: The hero photos filled the whole section behind the headline. In all three
  slides the busiest part of the photo (the circuit board, the opened laptop, the technician's arm)
  sat directly under the text, so the headline was hard to read even with the dark overlay.
- What was changed: The photo never sits behind the text now.
  - Desktop: the photo fills only the right ~60% (~54% on very wide screens), and its left edge
    fades into the dark brand colour. The text sits on that solid dark area.
  - Phone: the photo is a band across the top that fades into dark, and the text is below it.
  - The same three photos are kept, and more of each photo is now visible. The slider,
    pause button and reduced-motion behaviour are unchanged.
- Files (client): `src/pages/Home/Hero/Hero.jsx`
- How it was tested: screenshots of all three slides at 1440 px, 900 px and 390 px wide
  (before and after); lint; full Playwright run (see entry 6).

### 6. Final audit, report/slides update, commit and push — 2026-10-11
- Type: docs + release
- Report changes (`report/`): Reviewer 2 is now **Md. Fahmidur Rahman Sakib** (Senior
  Lecturer), replacing Abu Jafar Md. Jakaria. Submission date is now **26 October 2026**.
  Test totals are updated (server 2,595, browser 58). New report text: a Service-Area Map
  section (6.9), the final payout on technician removal (in 6.7), scenarios T-25/T-26,
  four new rows in Table 5.3, new commit hashes/counts and code size in Appendix D, and the
  CI date. Recompiled with Tectonic (76 pages, no undefined references) and copied to
  `Sarabo_Final_Report.pdf`. The acknowledgement no longer says the reviewers commented
  on the earlier report, since the reviewer has changed.
- Slides: results slide and notes updated to 2,595 / 58; slide 7 to 263 commits and ~75k lines. `screens/home.png` was
  re-captured, because the old one showed the hero text over the photo.
- Final verification on the exact committed code (clean `git archive`, no `.env`,
  in-memory MongoDB 8 replica set): server **2,595 / 2,595**; support **160 / 160**;
  migrations **63 / 63**; feedback **177 / 177**. Client: lint passed, build passed,
  Playwright **58 / 58**. (The support suite needs the catalogue that the full suite seeds;
  on an empty database it stops early. That is not a test failure.)
- Commits (author and committer: Jahid Hasan <jahidjubaer17@gmail.com>, no co-author):
  - client `e405467` feat: service-area search zooms to the exact sub-area;
    `d529725` feat: final bKash payout when an admin removes a technician;
    `428ee11` fix: hero text no longer sits over the photo
  - server `0d1e758` feat: pay out a removed technician's wallet to bKash
  - `sarabo-server/package-lock.json` was left uncommitted: its change came before this phase.
- Pushed to `github.com/jahidjubaer/sarabo-client` and `sarabo-server` (`main`), signed in
  as jahidjubaer. GitHub Actions CI passed on both new commits.
- This folder was pushed to `github.com/jahidjubaer/sarabo-doc`.

### 7. Site does not load on mobile data: investigation — 2026-10-14
- Type: investigation (no code change)
- Problem: After deploying the website and the API to Vercel, the site loaded on Wi-Fi but
  not on Robi mobile data ("This site can't be reached").
- What was checked, on the phone with Robi data:
  - `sarabo-client-six.vercel.app` (website) and `sarabo-server.vercel.app/health` (API): both failed.
  - A test Cloudflare Worker (`*.workers.dev`) set up as a proxy to the API: worked on Wi-Fi,
    failed on Robi data.
  - `sarabo-jahid.web.app` (the old Firebase address, confirmed up from the PC): also failed.
  - `cloudflare.com` and `vercel.com`: loaded normally.
  - After setting the phone's Private DNS to `dns.google`: the website and the API both loaded,
    and `/health` answered `status: ok`, `database: connected`.
- Finding: the failure is in DNS lookup on that phone/network, not in the Sarabo code or in
  Vercel. Three unrelated hosts failed, all on `.app` / `.dev` addresses, while `.com` sites
  loaded. The phone also had another DNS configured earlier, so it may be a fault of that
  phone only. This was not confirmed on a second phone or operator.
- Decision: no change for now. If other Robi users report the same problem, the next test is
  `sarabo-jahid.firebaseapp.com` (a free `.com` address for the same Firebase site) with the
  phone's DNS on Automatic; the lasting fix would be an own domain name.

### 8. Slow loading: API moved next to the database — 2026-10-14
- Type: fix (performance)
- Problem: The site felt slow and sometimes looked broken. Measured on the live API: the
  first request after the server had been idle took 4.2 s for `/health` and 10.7 s for
  `/service-definitions`; later requests took 0.6–0.75 s.
- Cause: The MongoDB Atlas cluster is in Mumbai, but the Vercel function ran in
  Washington, US (`iad1`). Every database call crossed the world and back (about 0.2 s).
  On a cold start the server also runs about 45 `createIndex` calls one after another
  (`config/database.js`) before the first query, which made up most of the 10 seconds.
- What was changed: one line in `vercel.json`, `"regions": ["bom1"]`, so the function runs
  in Mumbai, next to the database.
- Files (server): `vercel.json`
- How it was tested: config only, so no test run. After the deploy the live API was timed
  again from the same PC (single measurements).
- Result: the response header now shows `bom1::bom1`.

  | Request | Before | After |
  |---|---|---|
  | `/service-definitions`, first request after wake-up | 10.7 s | 2.9 s |
  | `/service-definitions`, normal request | 0.75 s | about 0.2 s |
  | `/health`, normal request | 0.6 s | about 0.2 s |

- Not done: CDN caching of the public services list. The API sends the CORS header only
  when the request has an `Origin` header, so a wrongly shared cached copy could block the
  list in browsers. A free uptime monitor on `/health` would reduce cold starts further.
- Commit: server `7889296` perf: run the API in Mumbai, next to the database. Pushed to
  `main`; Vercel deployed it.

### 9. AI support sometimes failed: faster model and a fallback model — 2026-10-14
- Type: fix
- Problem: AI support sometimes answered "took too long" or "temporarily unavailable".
- How the cause was found:
  - Six test questions on the live site: five were answered in 4.7–8.4 s and one failed
    with `504 SUPPORT_TIMEOUT` at the server's 12-second limit.
  - Timing Gemini directly with the real support prompt (about 2,700 input tokens):
    `gemini-3.1-flash-lite` took 6–16 s per answer on the free tier and sometimes returned
    `503` (high demand). `gemini-3.5-flash-lite` answered the same questions in 1.2–2.6 s.
  - After a burst of about 30–40 calls in a few minutes the free tier returned `429`
    (rate limit), and the retry went to the same model, so it failed again.
  - With the old "LOW" thinking setting, `gemini-3.5-flash-lite` returned cut-off JSON in
    3 of 4 tries; with "MINIMAL" every answer was valid.
- What was changed:
  - Default model is now `gemini-3.5-flash-lite`. `AI_SUPPORT_MODEL` may name either
    `gemini-3.5-flash-lite` or `gemini-3.1-flash-lite`; the other one becomes the fallback.
  - The second attempt goes to the fallback model, with no waiting, when the first model
    fails, is overloaded or is rate-limited.
  - AI support gives up on the first model after 5 seconds
    (`AI_SUPPORT_FIRST_ATTEMPT_TIMEOUT_MS`), so the fallback still fits inside the
    12-second limit.
  - The request helper, offer-note helper and weekly summary share the model, so they get
    the same fallback (`callGeminiJson`) and the "MINIMAL" thinking setting.
- Files (server): `config/aiSupport.js`, `services/aiProviders/geminiSupportProvider.js`,
  `geminiJsonCall.js`, `geminiRequestDraftProvider.js`, `geminiOfferNoteProvider.js`,
  `geminiReportSummaryProvider.js`, `tests/geminiSupportProviderTests.js`,
  `tests/aiRequestDraftTests.js`
- How it was tested: four new tests (fallback after a failure, fallback after a slow first
  model, either supported model accepted, helper fallback after a rate limit). Support
  suite **164 / 164**; full server suite **2,599 / 2,599**. Against real Gemini with the
  local database: 8 support questions (English, Bangla, Banglish) answered in 1.2–2.6 s,
  and the three helpers returned valid results in 1.4–2.4 s.
- Result on the live site after the deploy: 6 of 6 questions answered, in 3.0–9.6 s.
  These times match the slow model still being tried first: the Vercel variable
  `AI_SUPPORT_MODEL` was still `gemini-3.1-flash-lite` at the time of the test.
- Follow-up, same day: `AI_SUPPORT_MODEL` was changed to `gemini-3.5-flash-lite` in Vercel
  and the server redeployed. Live check: 8 of 8 questions answered. The first one after the
  redeploy took 4.9 s (cold start); the other seven took 1.4–1.9 s. During the check the
  per-visitor limit (8 anonymous questions per 10 minutes) correctly refused five extra
  test questions with `429 SUPPORT_RATE_LIMITED`.
- Still to do: update the model line in `.env.example` and the local `.env`.
- Known limit: the Gemini free tier has per-minute and daily quotas. If both models are
  refused at the same moment the user still sees "temporarily unavailable".
- Commit: server `5c6aab5` fix: faster AI model with a fallback model for slow or
  rate-limited answers (author Jahid Hasan, no co-author). Pushed to `main`; Vercel
  deployed it.

### 10. Smarter matching: ranking technicians' offers — 2026-10-14
- Type: feature
- Goal: Help the customer choose between technicians' offers. Before this, offers were
  listed in the order they arrived, with no guidance.
- Plan agreed with the user: smarter matching first, warranty and returns next (the
  warranty policy is to be confirmed with the user before that work starts). Live
  technician location and a full Bangla interface were skipped.
- What was changed:
  - New pure scoring module that ranks the waiting offers on a request using five factors,
    all from data Sarabo already stores (no paid service, no maps API, no AI):
    rating 30% (reviews smoothed toward 3★, so one 5★ review does not beat forty 4.8★
    ones), reliability 25% (repairs completed vs. missed pickups), price 20% (estimate
    against the other offers), district 15% (same district as the customer; there are no
    map coordinates, so nothing finer), reply time 10% (median minutes from a job being
    posted or reposted to the technician's offer, over their last 20 offers, at least 3).
  - A technician with no history gets a neutral score for that factor, neither a penalty
    nor a bonus.
  - Each waiting offer now carries `match: { score, rank, recommended, reasons }`.
    "Recommended" is only given when there are two or more offers. Reasons are shown only
    when true: rated ≥ 4.5★ from ≥ 3 reviews, ≥ 5 repairs with no missed pickup, lowest
    estimate, in your district, usually replies within an hour.
  - Customer offers page: offers sorted "Best match" first with a "Best match" badge and
    reason tags; sort switch (Best match / Lowest price / Newest); a short "How offers are
    ranked" explanation. The customer still chooses; nothing is booked automatically.
- Files (server): `services/offerRanking.js` (new), `controllers/jobPortalController.js`
  (`listForRequest`, new `matchHistory`), `tests/offerRankingTests.js` (new),
  `test-all.js`, `docs/smarter-matching.md` (new)
- Files (client): `src/utils/offerMatch.js` (new),
  `src/components/customer/TechnicianApplications.jsx`
- How it was tested: 22 new tests: 16 on the scoring rules, and 6 through the real endpoint
  with a database scenario (a nearby, quick, reliable technician is recommended over a
  cheaper one with a missed pickup; reply time counted from a repost; rejected offers not
  ranked; no private details in the response). Full server suite on a temporary in-memory
  MongoDB 7 replica set (working-tree copy without `.env`, fake keys, as in entry 1):
  **2,621 / 2,621 passed**. Client: `npm run lint` clean, production build OK (placeholder
  https API URL, as in CI).
- Not yet checked: the offers page has not been clicked through in a browser (it needs a
  signed-in customer with at least two offers).
- Commits (author Jahid Hasan only, no co-author), branch `feat/smarter-matching`, local
  only, not pushed or deployed: server `f932acb` feat: rank technician offers by rating,
  reliability, price, district and reply time; client `2b86891` feat: best match badge,
  reasons and sorting on technician offers.

### 11. Repair warranty and returns — 2026-10-14
- Type: feature
- Goal: Give customers a warranty on finished repairs: they can report a problem, the
  technician re-inspects it, and a fault that cannot be fixed again is refunded.
- Policy (chosen by the user before work started):
  - 30 days, counted from when the customer confirms they received the device.
  - Covers the same fault coming back, or a part the technician fitted failing. Not new
    damage, water damage or a drop.
  - The same technician re-inspects for free.
  - Covered: free re-repair. If the technician cannot fix it, or the customer says it is
    still broken, an admin refunds the repair amount.
  - Not covered: the customer can ask an admin to review the decision within 7 days.
  - Limits: one open claim at a time, and at most 2 claims per repair.
- Money decision (proposed and stated to the user): the refund is the whole quote total
  (the repair payment plus the inspection fee credited toward it), through Stripe test mode
  like the existing inspection-fee refunds. The technician's settlement for that repair is
  reversed in the same transaction. If it had already been withdrawn, the wallet shows the
  amount as owed, and it is netted from future earnings.
- What was changed:
  - Server: claim lifecycle (submitted → re-inspection booked → covered / not covered →
    admin review → re-repair → customer confirmation → resolved or refunded). Every step is
    a guarded update, so no step can be skipped and two people acting at once cannot both
    win.
  - Optional photos (up to 4) use signed uploads in their own `warranty/` storage folder.
    Unused uploads expire after 20 minutes.
  - Refunds use idempotency keys per claim and part, so a retry never refunds twice; a
    failed refund stays pending for the admin to retry.
  - New settlement status `reversed` and wallet figure `owedBalance`.
  - Three notification types (customer, technician, admin), each with a `step`.
  - 12 endpoints and two new collections (`warranty_claims`, `warranty_photo_uploads`)
    with indexes.
  - Client: a "Warranty" section on the customer's repair page (cover end date, "Report a
    problem" form with photos, "It works now" / "Still not working", "Ask an admin to
    review"). A "Warranty claims" page for technicians (book the visit, record the
    decision, report the re-repair) and admins (review queue and refunds), linked in both
    sidebars. Wallet note when money is owed, and a "Refunded under warranty" settlement
    label.
- Files (server): `utils/warranty.js`, `controllers/warrantyController.js`,
  `routes/warranty.js`, `services/warrantyRefunds.js` (all new), `utils/settlement.js`,
  `utils/notificationEvents.js`, `config/database.js`, `controllers/index.js`, `index.js`,
  `tests/warrantyTests.js` (new), `test-all.js`, `docs/warranty.md` (new)
- Files (client): `src/api/warranty.js`, `src/utils/warranty.js`,
  `src/components/warranty/WarrantyClaimCard.jsx`,
  `src/components/warranty/CustomerWarrantySection.jsx`,
  `src/pages/Dashboard/WarrantyClaims/WarrantyClaims.jsx` (all new),
  `CustomerRequestDetailsView.jsx`, `router.jsx`, `dashboardNavigation.js`,
  `config/status/index.js`, `Wallet.jsx`
- How it was tested: 45 new server tests: 16 on the policy rules and wallet effect, and 29
  through the controller with fake photo storage and a fake Stripe refunder. They cover the
  whole flow, the failed-then-retried refund, the settlement reversal, who may act at each
  step, and route roles. Two existing tests were updated on purpose: the notification type
  count (41 → 44) and the list of events that may go to more than one role. Temporary
  in-memory MongoDB 7 replica set (copy without `.env`, fake keys): main suite
  **2,666 / 2,666**, support **164 / 164**, migrations **63 / 63**, feedback **177 / 177**.
  Client: lint clean, production build OK, Playwright browser tests **58 / 58**.
- Not yet checked: the new screens have not been clicked through in a browser while signed
  in (the browser tests only cover public pages). Photo upload depends on Supabase storage,
  which is currently unreachable locally (see the earlier note). Claims can be sent without
  photos.
- Known limits: account deletion rules do not yet look at open warranty claims. Real
  (non-test) refunds would need a live Stripe account, which Sarabo does not use.
- Commits (author Jahid Hasan only, no co-author), branch `feat/warranty` (built on
  `feat/smarter-matching`), local only, not pushed or deployed: server `c5ef6a5` feat:
  repair warranty claims with free re-inspection, admin review and refunds; client
  `cab2fa6` feat: warranty claims for customers, technicians and admins.

### 12. Whole-workflow review before push — 2026-10-14
- Type: review (no code changed)
- Goal: Before pushing, find real-life situations the repair process does not handle and
  states where a request can get stuck.
- Found (checked in the code, not assumed):
  1. An approved quote that is never paid stays in `quote_approved` forever. The customer
     cannot cancel (cancelling is only allowed before a technician is assigned), nothing
     times it out, and the technician stays "busy". An admin also cannot remove a
     technician who has active work.
  2. An inspection can record `not_repairable` or `not_economical`, but nothing acts on
     it. The only next step is to submit a quote, so the request sits in
     `inspection_completed` with the technician busy.
  3. A paid repair has no way out except "complete". If parts are unavailable or the
     technician disappears, there is no cancel, refund or reassignment.
  4. Only the customer can confirm receipt. If they never do, the technician's money stays
     pending forever and the warranty never starts.
  5. Cancelling after pickup (declined quote, auto-close) marks the request `cancelled`,
     but nothing tracks returning the device to the customer.
  6. Admin alerts cover only problems before pickup; nothing flags stalled work after it.
  7. Warranty (entry 11): a claim the technician never books has no deadline. A removed
     technician cannot act on their claims, and an admin cannot take a claim over.
     Removing a technician ignores open claims.
  8. Not modelled: device condition at pickup, customer not home at pickup (a missed pickup
     always refunds as a technician no-show), cash payment (Stripe test mode only).
- Result: reported to the user with suggested fixes and an order; waiting for their
  decision before any change.

### 13. Fixes for repairs that could get stuck, and warranty deadlines — 2026-10-14
- Type: fix
- Goal: Fix review findings 1–4 from entry 12, and add deadlines to the warranty.
- What was changed:
  1. **Approved quote never paid.** The daily job closes an approved quote unpaid for 3
     days (reason `payment_not_made`). A request whose payment page is open right now is
     skipped and tried again the next day, so no one is charged for a closed request; any
     leftover checkout is expired. The customer can also cancel an approved quote before
     paying ("I don't want the repair"). In both cases a paid inspection fee is kept 90/10
     (the device was inspected), the technician is freed unless they have other work, and
     both sides are told. The request page shows the "pay by" date.
  2. **Not repairable.** When the inspection says `not_repairable` or `not_economical`, the
     technician or the customer can close the request. Same outcome as 1.
  3. **Paid repair that cannot be finished.** The technician reports "can't finish this
     repair" with a reason, and admins are alerted (new item on the admin overview). An
     admin can cancel and refund: the whole quote total is refunded through Stripe test mode
     (one idempotency key per part, so a retry never refunds twice), the technician's
     settlement is reversed, and the technician is freed. Payment history now shows refunds
     (warranty refunds too).
  4. **Receipt never confirmed.** The technician marks the device returned. The customer
     confirms, or presses "I haven't received it". Without either, receipt is confirmed
     automatically after 3 days, which releases the technician's money and starts the
     warranty. A dispute stops the automatic confirmation, alerts admins, and an admin
     settles it with an explanation. All three ways use one shared update, so the money is
     released exactly once.
  - **Warranty deadlines.** The technician must book the re-inspection within 3 days,
    decide within 3 days of the visit, and repair a covered claim within 7 days. Late claims
    appear in the admin queue marked overdue, admins get one alert per late step, and they
    can take over (decide, or move a covered claim to a refund). A technician with open
    claims cannot be removed.
  - Admin report: kept inspection fees are now counted per reason. Before, every fee not
    from a declined quote was counted as a late cancellation.
- Files (server): `services/requestClosure.js`, `services/receiptConfirmation.js`,
  `services/refundParts.js`, `controllers/workflowController.js`, `routes/workflow.js`,
  `tests/workflowFixesTests.js` (all new); `controllers/pickupReminderController.js` (daily
  job), `repairRequestController.js`, `adminAttentionController.js`,
  `adminReportController.js`, `technicianController.js`, `warrantyController.js`,
  `routes/warranty.js`, `services/warrantyRefunds.js`, `utils/warranty.js`,
  `utils/inspectionFee.js`, `utils/notificationEvents.js` (3 new types, 47 total),
  `controllers/index.js`, `index.js`, `test-all.js`
- Files (client): `src/components/workflow/RequestWorkflowActions.jsx` (new; one panel used
  in the customer, technician and admin request views), `AdminOverview.jsx`,
  `WarrantyClaims.jsx`, `src/api/warranty.js`, and the three request views
- How it was tested: 42 new server tests covering each fix, the "payment page open" skip,
  the failed-then-retried refund, the dispute blocking auto-confirm, the warranty
  deadlines and take-over, the daily job, and route roles. One test checks that a
  technician with other active work stays busy when one job closes. Temporary in-memory
  MongoDB 7 replica set (copy without `.env`, fake keys): main suite **2,708 / 2,708**;
  support **164 / 164**, migrations **63 / 63** and feedback **177 / 177** passed on the same
  code before a final test-only edit. Client: lint clean, build OK, browser tests
  **58 / 58**.
- Not yet checked: the new buttons have not been clicked through while signed in.
- Still open from entry 12: device return after a cancellation is not tracked (5);
  stalled-work alerts after pickup beyond the ones above (6); pickup condition, customer
  not home, and cash payment (8).
- Commits (author Jahid Hasan only), branch `fix/workflow-gaps` (on `feat/warranty`), local
  only: server `a2004a4`, client `c067261`.

### 14. Remaining workflow gaps — 2026-10-14
- Type: fix
- Goal: Close the gaps still open after entry 13. The user chose to leave cash payment for
  later (future work; Sarabo stays on Stripe test mode).
- What was changed:
  - **A. Payment after cancellation.** Before, a repair payment arriving after the request
    was cancelled was refused and its record deleted, so the customer could be charged with
    no record. Now it is recorded, refunded at once (idempotent per session), and a failed
    refund stays on the admin refund list for a retry. The cancelled check also runs first:
    after a close the fee is "kept", so the amount check would otherwise have refused the
    payment for the wrong reason.
  - **B. Device return after cancellation.** Every cancellation after pickup (declined
    quote, unpaid quote, not repairable, admin cancel of a paid repair) records that the
    device must go back. The technician marks it returned; the customer confirms ("I have
    my device back") or says it has not arrived. Without a reply it is confirmed after 3
    days, and an admin settles a dispute. The job stays in the technician's active list
    until the return is confirmed.
  - **C. Stalled work.** One rule set (`services/stalledWork.js`) finds work that has not
    moved on:
    - customer has not chosen a new pickup time (3 days);
    - not inspected 3 days after pickup;
    - no quote 3 days after inspection;
    - quote unanswered for 3 days;
    - repair not started 3 days after payment;
    - repair running over 14 days;
    - device not returned 3 days after repair or after cancellation.
    Admins see these on the overview, with one alert per request and stage from the daily
    job.
  - **D. Pickup condition.** The technician records the device's condition and accessories
    when collecting it (the app always asks; the API keeps working without it). The
    customer sees it and can say it is wrong; an admin reviews it. The pickup time is now
    stored, which the stall rules need.
  - **E. Customer not home.** The technician reports it with a note. The booking stays, the
    customer is asked for a new pickup time, and it is not treated as a technician no-show.
    If the customer does not choose a time in 3 days, it shows as stalled.
  - Admin identities (who settled a dispute or reviewed a condition) are hidden from
    customers and technicians.
- Files (server): `services/stalledWork.js`, `tests/remainingGapsTests.js` (new);
  `services/paymentProcessor.js`, `services/requestClosure.js`,
  `services/declinedQuoteClose.js`, `controllers/workflowController.js`,
  `repairRequestController.js`, `adminAttentionController.js`,
  `inspectionFeeController.js` (retry covers any pending refund),
  `pickupReminderController.js`, `routes/workflow.js`, `utils/notificationEvents.js`,
  `test-all.js`
- Files (client): `PickupConditionDialog.jsx` (new), `RequestWorkflowActions.jsx`,
  `RequestDetails.jsx`, `AdminOverview.jsx`, `paymentErrorMessage.js`
- How it was tested: 30 new server tests, one per behaviour above, including the late
  payment through the real payment processor with a fake Stripe session. Temporary
  in-memory MongoDB 7 replica set: main suite **2,738 / 2,738**; support **164**,
  migrations **63**, feedback **177**. Client: lint clean, build OK, browser tests
  **58 / 58**.
- Not checked: the new screens have not been clicked through while signed in.
- Commits (author Jahid Hasan only), branch `fix/remaining-gaps`: server `8a1bc1b`,
  `304e574`; client (this entry's commit).

### 15. Photo upload button, technician profile editing, minimum inspection fee — 2026-10-14

- Asked for: (1) damage photos uploaded the moment they were picked - add an Upload
  button; (2) let technicians edit their profile (location and other details); (3) many
  repairs had no inspection fee - every repair needs one, at least 100/200 BDT.
- Decisions (user's answers): 100 BDT minimum when the service's estimate tops out at
  1,000 BDT or less, 200 BDT for bigger repairs; every offer must charge at least the
  minimum (no free inspection); add a one-time migration for the live catalogue.
- What changed:
  - **A. Photo upload button.** Chosen photos now wait with a preview and a remove
    button. Nothing is sent until the customer presses "Upload N photos". The photo
    given to the AI helper also waits there instead of uploading on its own. Same checks
    as before (type, size, 3-photo limit, duplicates).
  - **B. Technician profile editing.** New `PATCH /technicians/me` (technician only,
    identity from the sign-in token). Name, phone, region + district (always together)
    and address can change. Email, NID, status and availability cannot. The service
    area is locked while a repair is active (the pickup was booked in the old area).
    After an area change the technician is told about open jobs in the new area. The
    profile page has an "Edit details" panel with the same region/district list as
    the application form.
  - **C. Minimum inspection fee.** One rule (`utils/inspectionFee.js`
    `minimumInspectionFee`) applies everywhere:
    - new requests store at least the minimum;
    - the public service list shows it;
    - the job portal raises the fee limit to it, and older open requests follow it too;
    - offers below it are refused (`INSPECTION_FEE_TOO_LOW`);
    - admins can't price a service below it. The check runs only when prices change,
      so an old service can still be renamed;
    - seed data raised.

    Offers already sent before the change keep the fee they were sent with.
  - **Migration:** `npm run migrate:inspection-fee-floor` (dry run by default,
    `--confirm` to write; production needs `ALLOW_PROD_FEE_FLOOR_MIGRATION=true` and
    `--expect-db=<name>`). It raises only fees below the floor, bumps the pricing
    version, and running it again changes nothing. **Not run on production yet.**
- Files (server): `controllers/technicianController.js`, `routes/technicians.js`,
  `utils/inspectionFee.js`, `utils/jobPortal.js`, `services/pricingService.js`,
  `controllers/jobPortalController.js`, `serviceDefinitionController.js`,
  `adminServiceDefinitionController.js`, `data/serviceDefinitionSeed*.js`,
  `scripts/migrate-inspection-fee-floor.js` (new), `package.json`; tests
  `technicianSelfEditTests.js`, `inspectionFeeFloorTests.js` (new), and
  `jobPortalTests.js`, `inspectionFeeTests.js`, `serviceCatalogTests.js` and
  `test-all.js` updated for the new fee rule
- Files (client): `DamageImagePicker.jsx`, `DamageImageManager.jsx`,
  `PostCreationDamageStep.jsx`, `TechnicianDetailsEditor.jsx` (new),
  `TechnicianProfileCard.jsx`, `JobApplicationSheet.jsx`, `JobCard.jsx`,
  `ServiceEditor.jsx`, `utils/inspectionFee.js`, `jobBoard.js`, `serviceCatalogueForm.js`
- How it was tested: 18 new server tests (7 profile edit, 11 fee floor incl. the
  migration). In-memory MongoDB replica set: main suite **2,756 / 2,756**; support
  **164**, migrations **63**, feedback **177**. Client: lint clean, build OK, browser
  tests **58 / 58**.
- Not checked: the new screens have not been clicked through while signed in.
- Commits (author Jahid Hasan only), branch `fix/photo-profile-fee`: server `e0554b0`,
  `4d0d584`; client `9792490`, `6350f49`, `e9caaeb`. Not pushed.

### 16. Old offers below the minimum inspection fee — 2026-10-14

- Asked for: close the edge case from entry 15. An offer sent before the minimum
  existed could still have a lower fee, even 0. Accepting a 0-fee offer booked the
  visit with no fee at all.
- Decision (user said go ahead): raise the fee when the offer is accepted, and also
  raise stored waiting offers in the migration.
- What changed:
  - One rule, `offerInspectionFee` (`utils/jobPortal.js`): a waiting offer charges
    at least its request's minimum. Closed offers keep their history.
  - The customer's offer list, the ranking and the technician's own offer all show
    that fee.
  - When the customer accepts an older offer, its raised fee is saved on the offer
    first, with the old value in `inspectionFeeRaisedFrom`. Checkout, the payment
    webhook's amount check and the booking all use the same number. A free instant
    booking can no longer happen. The save checks the stored fee first: if the
    technician re-offered at that moment, the customer gets `APPLICATION_CHANGED` and
    reloads.
  - `migrate-inspection-fee-floor` also raises waiting offers below their request's
    minimum. It reports them in the dry run, and running it again changes nothing.
  - The AI support assistant now quotes the minimum fee too, not the raw stored 0.
- Tests:
  - Server: 4 new — the old offer is shown at the minimum, accepting opens a
    checkout for it, paying books the technician with it, and the migration raises
    only waiting offers.
  - The job-portal booking test now books through a paid checkout, since every
    offer has a fee.
  - Suites: main **2,760 / 2,760**; support **164**, migrations **63**, feedback
    **177**. No client change.
- Commit (author Jahid Hasan only), branch `fix/photo-profile-fee`: server (this
  entry). Not pushed.

### 17. Push, deploy and migration dry run — 2026-10-14

- User said push and deploy, then run the migration dry run. The auto-mode check
  blocked `git push` at first. With the user's OK (option 2), narrow allow rules were
  added to `~/.claude/settings.json`: the two exact push commands and
  `npm run migrate:inspection-fee-floor`.
- Pushed: server `cf7dd1b..ca19105`, client `48adc50..e9caaeb` (fast-forward of
  `fix/photo-profile-fee`). Vercel deployed both. Checked live: `PATCH /technicians/me`
  answers 401, and the live client chunks contain the Upload button, Edit details and
  the fee check.
- Dry run against `sarabo-db` (wrote nothing): 45 services, **16 would be raised** to the
  minimum (every diagnosis service 0 -> 100 BDT, the others 0 -> 200 BDT), 29 already at
  or above it. Waiting offers: 16, **14 would be raised** (12 to 100 BDT, 2 to 200
  BDT).
- Not yet done: `--confirm` (waiting for the user).
- **Correction (same day):** the run above was against the local development database
  `sarabo-db`, not production. The live database is `sarabo_production` (underscore),
  on the same cluster. Found by listing the cluster's databases (only it and
  `sarabo-db` hold 45 services; `sarabo-production` with a hyphen does not exist).
  Production dry run (`MONGO_DB_NAME=sarabo_production`, override and `--expect-db`,
  wrote nothing): **16 of 45 services** would be raised, the same list as locally.
  1 waiting offer, already at or above the minimum, so **0 offers** to raise.
  `--confirm` not run yet.
- **Applied (user said confirm, and tidy local too):** `--confirm` on `sarabo_production`
  raised 16 services, 0 offers. On local `sarabo-db` it raised 16 services and 14
  waiting test offers. A dry run afterwards finds nothing left on either database
  (45 / 45 services at or above the minimum). The live API still serves 45 services.

### 18. Report updated with the final phase and a screenshot walkthrough — 2026-10-14

- Asked for: update the report with everything since 11 Oct, shorter abstract and
  conclusion, nothing important left out, and screenshots of the whole process.
- Text: abstract and conclusion shortened; introduction (final phase, O12, scope),
  requirements FR-33 to FR-38, architecture (Vercel hosting, Mumbai region, 21
  collections, warranty states), implementation (fee floor, deployment, final-phase log
  as a long table, 0-12), workflows (offer ranking, "no request can get stuck",
  pickup condition, warranty, profile editing, 47 notification types), AI chapter
  (model + fallback), testing (2,760 server checks, new scenarios T-27 to T-34),
  limitations, appendix (new endpoints, fields, money rules, baseline commits).
- Screenshots: new Chapter 7 "System Walkthrough" with 52 figures. One clean test
  request (Samsung Galaxy A54) was walked through the whole flow on the local stack
  with the user's own customer, technician and admin accounts (the user signed in
  each role once in a browser window; saved sessions were reused): AI request helper,
  offer with AI note, ranked offer, inspection fee via Stripe test checkout, pickup
  condition, inspection, quote, approve-and-pay, progress, completion, hand-back,
  receipt, review, warranty claim, re-inspection, re-repair, resolved; then wallet
  withdrawal (3,600 BDT) marked paid with a made-up TrxID, and all admin pages.
  This added that request, its payments (Stripe test mode), review, warranty claim
  and the withdrawal to the local development database only.
- Found while doing it: the repair-payment Stripe page says "Repair request:
  undefined" (`paymentController.js` uses the legacy `deviceName`; v2 requests have
  none). Not fixed yet. Client CI browser-test job failed on GitHub for `e9caaeb`
  while the same 58 tests pass locally; the report says so.
- Build: Tectonic 0.15.0, 114 pages, no undefined references; copied to
  `Sarabo_Final_Report.pdf`.

### 19. Stripe item name fix, and a 10-slide deck — 2026-10-16

- Stripe: the repair-payment checkout said "Repair request: undefined" because
  `paymentController.createV2CheckoutSession` used the legacy `deviceName`, which v2
  requests do not have. It now uses `deviceLabelOf` (brand + model from the product
  snapshot, else the device type), as the emails already do. New check 19b. Server
  suite on a temporary in-memory MongoDB 7 replica set: **2,761 / 2,761**. (A run
  against the shared Atlas `sarabo-test-db` failed 3 BDT-migration checks only because
  that database still holds catalogue rows seeded before the minimum-fee change; a fresh
  database passes.) Server `d81fa65`, pushed to `main`; Vercel production deploy Ready,
  `/health` 200.
- Slides: rebuilt as 10 slides for a 5-minute talk (title, problem, solution, how it
  works, ER diagram, ranked offer and quote, warranty and deadlines, AI, architecture and
  trust, results and thanks). Large text, short points, zoomed screenshots cut from the
  report by `presentation/make_crops.py`; ER diagram with entity cards (PK/FK) and
  crow's-foot links. All shape positions are whole EMUs.

### 20. Report shortened from 114 to 87 pages — 2026-10-16

- Asked for: a shorter report without removing anything important (target about 90 pages,
  screenshots two per row, personal emails blurred).
- Emails: found with the Windows OCR engine and blurred in 8 screenshots (29 boxes); the
  remaining visible addresses are seeded `@seed.sarabo.local` accounts.
- Chapter 7: 52 full-width screenshots became 39 cropped ones, two per row at equal
  height (`report/make_walkthrough.py` crops them into `img/wt/` and writes
  `tex/walkthrough.tex`). Every step of the walkthrough repair keeps its picture; dropped
  only near-duplicates (extra overview pages, a confirmation box, a second jobs list,
  users list, notifications). 28 -> 10 pages.
- Front matter: contents list to section level, and the contents, tables and figures lists
  single-spaced; tables single-spaced. Body text keeps the template's 1.5 spacing, font
  and margins.
- Updated facts: 2,761 server tests, server commit `d81fa65` (120 commits), final phase
  11-16 October, new log row for the Stripe item-name fix.
- Result: 87 pages, no undefined references.

### 21. Readable screenshots on A4, and tighter text — 2026-10-16

- Problem: at two per row, the text inside screenshots printed at about 3 pt on A4.
- Chapter 7 now has 21 key screenshots, one per row at full text width, each cropped to
  the part that matters, so their text prints at about 7-8 pt (checked by rendering at
  print resolution). Kept one screen per main step of the walkthrough repair plus the AI,
  wallet and admin screens.
- Tightened the prose of Chapters 2, 4, 5, 6, 8 (AI), 9 (security), 10 (testing) and 11
  (limitations as one list): shorter sentences, no repetition; every table, rule, number
  and requirement kept.
- Corrected while editing: the AI helper's photo now waits for "Upload" (it no longer
  uploads on its own); client CI also runs browser tests; the API has 125 routes
  ("over 120"); the manual-acceptance section now records the 14 October walkthrough.
- Result: 86 pages, no undefined references.
