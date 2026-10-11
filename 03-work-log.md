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
