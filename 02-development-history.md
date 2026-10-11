# Development History

Built from the git history of both repositories (client: 156 commits, server: 107
commits), 26 July 2026 – 11 October 2026, by Jahid Hasan. The project started from an
existing parcel-delivery codebase ("zap_shift") and was rebuilt into a repair platform.

| Phase | Dates | What was done |
|---|---|---|
| 1. Foundation & hardening | 26–28 Jul | Imported the base app; secured auth and role routing; secure Stripe checkout and webhook; validated status transitions; public sanitized tracking; cancellation; made assignment, approval and completion transactional; closed authorization holes |
| 2. Admin & notifications | 29 Jul – 4 Aug | Admin repair-request management; in-app notification system (technician, lifecycle, payment); production DB isolation, health monitoring; double-booking prevention |
| 3. Repair domain (v2) | 5–8 Aug | Service taxonomy and catalogue with pricing; technician expertise; v2 repair request schema; eligible-technician matching; damage photo upload; prices in BDT; inspection, quote, payment and repair-progress workflows; safe deletion; verified email |
| 4. Rename to Sarabo | 10–12 Aug | Migrated database, collections, fields, modules, API routes and UI terms from parcel to repair vocabulary; assignment accept/reject; receipt confirmation |
| 5. Money & UI redesign | 13–19 Aug | Technician earnings and 90/10 settlement; wallet and withdrawals; moved photo storage to Supabase; full "service spine" UI redesign (public site, auth, dashboards), accessibility fixes |
| 6. AI support & feedback | 18–24 Sep | Gemini customer-support chat; technician reviews and private reports with admin moderation; product tour; second redesign pass; admin service-catalogue editor; CI on GitHub Actions |
| 7. Operations | 24–25 Sep | Pickup scheduling with slot capacity; region rule for matching; email updates; Playwright browser tests; admin reports; attention list for overdue/missed pickups; in-app reminders; refuse requests no technician can take |
| 8. Job portal & inspection fee | 25 Sep – 2 Oct | Technician offers and customer choice; inspection fee payment, credit, refunds and 90/10 kept-fee split; reject-and-repost; public jobs board; new-job/repost notifications; PDF receipts; one-step approve-and-pay |
| 9. AI helpers & payouts | 2–4 Oct | AI request helper (text + photo); price guide and AI offer note; AI report summary; bKash withdrawals with TrxID; Vercel hosting config |

## Phase 10 — Final-year-project fixes and improvements (from 11 Oct 2026)

Tracked step by step in [03-work-log.md](03-work-log.md).

| Step | Date | What was done |
|---|---|---|
| Review & verification | 11 Oct | Full codebase/docs review; all suites re-run on an isolated database |
| Report & presentation | 11 Oct | Final report (LaTeX, Metropolitan University template) and 10-slide deck |
| Service-area map | 11 Oct | Search goes to the exact sub-area (e.g. Ambarkhana), 226 of 236 sub-areas mapped |
| Removal payout | 11 Oct | Removing a technician queues their whole balance as a bKash withdrawal |
| Homepage hero | 11 Oct | Photo moved off the headline so the text is always readable |
| Final audit & push | 11 Oct | Reviewer and submission date updated; client `428ee11`, server `0d1e758` pushed; CI passed |
