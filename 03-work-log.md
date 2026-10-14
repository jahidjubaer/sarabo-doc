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
